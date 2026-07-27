import os

from dotenv import load_dotenv
from langchain_community.utilities import SerpAPIWrapper
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from langgraph.graph import END

from state import ResearchState

load_dotenv()

MODEL_NAME = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")

llm = ChatGroq(model=MODEL_NAME, temperature=0)
search = SerpAPIWrapper()


def _max_revisions() -> int:
    """Read at call time so the control in the UI changes real behaviour."""
    try:
        return max(1, int(os.getenv("MAX_REVISIONS", 2)))
    except ValueError:
        return 2


def _results_per_query() -> int:
    try:
        return max(1, int(os.getenv("RESULTS_PER_QUERY", 5)))
    except ValueError:
        return 5


# ──────────────────────────────────────────────────────────────
# 1 · Planner
# ──────────────────────────────────────────────────────────────
def planner_node(state: ResearchState):
    prompt = f"""You are a research planner. Break the following topic into 3 precise,
self-contained questions suitable for a web search engine.

Topic: {state['query']}

Return only the questions, one per line, with no numbering or preamble."""

    response = llm.invoke([HumanMessage(content=prompt)])
    plan = [q.strip(" -\u2022\t") for q in response.content.split("\n") if q.strip()][:3]
    return {"plan": plan, "revision_count": state.get("revision_count", 0)}


# ──────────────────────────────────────────────────────────────
# 2 · Researcher
#
# SerpAPIWrapper.run() returns one condensed snippet per query -- roughly 300
# characters. That is not enough for a Writer to work from, so it fills the gap
# by inventing content and fake citations. Pulling the structured results gives
# real titles, URLs and snippets to write from.
# ──────────────────────────────────────────────────────────────
def researcher_node(state: ResearchState):
    gathered = []
    per_query = _results_per_query()

    for q in state["plan"]:
        try:
            raw = search.results(q)
        except Exception as exc:
            gathered.append(
                f"### Query: {q}\nSEARCH FAILED ({type(exc).__name__}: {exc}). "
                f"Write the report from the other queries and state this gap explicitly."
            )
            continue

        parts = [f"### Query: {q}"]

        answer = (raw.get("answer_box") or {})
        if answer.get("answer") or answer.get("snippet"):
            parts.append(f"[Featured answer] {answer.get('answer') or answer.get('snippet')}")

        organic = (raw.get("organic_results") or [])[:per_query]
        for i, r in enumerate(organic, 1):
            parts.append(
                f"[{i}] {r.get('title', 'Untitled')}\n"
                f"URL: {r.get('link', '')}\n"
                f"{r.get('snippet', '')}"
            )

        if not organic and not answer:
            parts.append("No results returned for this query.")

        gathered.append("\n\n".join(parts))

    return {"research_data": gathered}


# ──────────────────────────────────────────────────────────────
# 3 · Writer
# ──────────────────────────────────────────────────────────────
def writer_node(state: ResearchState):
    data_str = "\n\n".join(state["research_data"])
    feedback = state.get("feedback")
    revising = bool(feedback) and feedback != "Approved"

    revision_block = ""
    if revising:
        revision_block = f"""
REVISION NOTES FROM THE REVIEWER
{feedback}

Address every point above. These notes are instructions for you -- they must NOT
appear anywhere in the report itself."""

    prompt = f"""You are a professional report writer. Write a clear, well-structured
report on the topic below, using only the research material provided.

TOPIC
{state['query']}

RESEARCH MATERIAL
{data_str}
{revision_block}

RULES
- Use only facts present in the research material. Do not add figures, studies or
  statistics from your own knowledge.
- Never invent a citation, an author or a paper title. If you have no source for a
  claim, do not make the claim.
- CITATIONS: every numbered marker such as (1) or [2] you use in the body MUST have a
  matching entry in a "References" section at the end, and every entry must carry the
  real URL from the research material. A numbered marker with no matching reference is
  a defect. If you would rather not keep a numbered list, name the source inline
  instead, e.g. "(IBM — https://...)".
- End the report with the "References" section whenever you cited anything.
- If the material is too thin to answer part of the topic, say so in one short line
  under a "Gaps" heading rather than filling it in.
- Output the report only. No preamble, no reviewer notes, no self-assessment,
  no rating, no note about what you revised."""

    response = llm.invoke([HumanMessage(content=prompt)])
    return {"draft": response.content}


# ──────────────────────────────────────────────────────────────
# 4 · Critic
#
# "You are a strict reviewer" with no bar means the model always finds something,
# so the first draft is rejected every single time and the loop stops being a
# judgement. A rubric with an explicit pass condition makes approval reachable.
# ──────────────────────────────────────────────────────────────
def critic_node(state: ResearchState):
    prompt = f"""You are a quality reviewer. Judge the report against the checklist and
nothing else. Do not invent additional standards.

ORIGINAL TOPIC
{state['query']}

REPORT
{state['draft']}

CHECKLIST
1. Does it answer the topic directly, rather than circling it?
2. Is it organised into clear sections?
3. Are claims traceable to the research, with real URLs where cited?
4. Is it free of invented citations, fake authors and placeholder references?
   Every numbered marker such as (1) must have a matching entry in a References
   section carrying a real URL. Markers with no reference list = fail this item.
5. Is it free of reviewer notes, ratings and self-assessment?

If all five pass, reply with exactly: Approved
A report does not need to be exhaustive to pass -- it needs to be accurate and
answer the question.

If any item fails, list only the failing items and what to change. Be specific and
brief. Do not rewrite the report yourself."""

    response = llm.invoke([HumanMessage(content=prompt)])
    feedback = response.content.strip()

    new_count = state.get("revision_count", 0) + 1
    budget = _max_revisions()

    # Anchor on the FIRST word. A substring test also matches "Not approved",
    # which silently turns every rejection into an approval.
    verdict = feedback.lstrip("*# \n\t").lower()
    approved = verdict.startswith("approved") or verdict.startswith("\u0645\u0642\u0628\u0648\u0644")

    if approved or new_count >= budget:
        return {"feedback": "Approved", "revision_count": new_count}
    return {"feedback": feedback, "revision_count": new_count}


def critic_router(state: ResearchState):
    """Approved or out of budget -> stop. Otherwise back to the Writer."""
    if state.get("revision_count", 0) >= _max_revisions():
        return END
    verdict = (state.get("feedback") or "").lstrip("*# \n\t").lower()
    if verdict.startswith("approved") or verdict.startswith("\u0645\u0642\u0628\u0648\u0644"):
        return END
    return "writer"