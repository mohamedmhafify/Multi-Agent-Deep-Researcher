"""
Multi-Agent Deep Researcher — Live Newsroom
A Planner, Researcher, Writer and Critic working in sequence, traced in the open.

Author: Mohamed Mostafa Hassan Afify
"""

import os
import time

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Multi-Agent Deep Researcher",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════
#  THEME  (no blank lines inside <style>: a blank line ends the raw-HTML
#  block in Markdown and silently truncates the CSS)
# ══════════════════════════════════════════════════════════════════════
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,400&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
:root{
  --ink:#0A0C10; --panel:#11141B; --line:#1C212B;
  --gold:#C9A96A; --gold-bright:#E4C88A; --gold-dim:rgba(201,169,106,.22);
  --parchment:#E8E6E1; --muted:#8A8F9A;
  --plan:#4589FF; --research:#8B7BD8; --write:#C9A96A; --critic:#D45B4E; --ok:#2E9B8F;
}
.stApp{ background:var(--ink); color:var(--parchment); }
html,body,[class*="css"]{ font-family:'Inter',system-ui,sans-serif; }
header[data-testid="stHeader"]{ background:transparent !important; }
[data-testid="stDecoration"], footer{ display:none !important; }
[data-testid="stToolbarActions"], [data-testid="stStatusWidget"], [data-testid="stMainMenu"]{ display:none !important; }
[data-testid="stExpandSidebarButton"], [data-testid="stSidebarCollapseButton"]{ display:flex !important; visibility:visible !important; }
[data-testid="stExpandSidebarButton"] button, [data-testid="stSidebarCollapseButton"] button{ color:var(--gold) !important; }
.block-container{ padding-top:2.2rem; padding-bottom:3rem; max-width:1250px; }
.masthead{ text-align:center; padding:.5rem 0 1.4rem; }
.masthead .kicker{ font-family:'JetBrains Mono',monospace; font-size:.7rem; letter-spacing:.3em; color:var(--gold); text-transform:uppercase; margin-bottom:.9rem; }
.masthead .title{ font-family:'Cormorant Garamond',serif; font-weight:300; font-size:clamp(2.3rem,5vw,3.5rem); line-height:1.05; color:var(--parchment); margin:0 0 .3rem; }
.masthead .title em{ font-style:italic; color:var(--gold); }
.masthead .tagline{ font-family:'JetBrains Mono',monospace; font-size:.7rem; letter-spacing:.26em; text-transform:uppercase; color:var(--muted); margin-bottom:.8rem; }
.masthead .sub{ color:var(--muted); font-size:.94rem; font-weight:300; max-width:62ch; margin:0 auto; }
.rule{ height:1px; background:var(--gold-dim); border:0; margin:1.4rem 0; }
.strip{ display:flex; border-top:1px solid var(--gold-dim); border-bottom:1px solid var(--gold-dim); padding:1rem 0; margin:1.3rem 0 1.6rem; }
.strip .cell{ flex:1; text-align:center; }
.strip .n{ font-family:'JetBrains Mono',monospace; font-size:1.45rem; font-weight:500; color:var(--gold); font-variant-numeric:tabular-nums; display:block; line-height:1.1; }
.strip .l{ font-size:.65rem; letter-spacing:.15em; text-transform:uppercase; color:var(--muted); margin-top:.4rem; display:block; }
.agent{ background:var(--panel); border:1px solid var(--line); border-left:3px solid var(--gold); border-radius:8px; padding:1rem 1.2rem; margin:.7rem 0; }
.agent.plan{ border-left-color:var(--plan); }
.agent.research{ border-left-color:var(--research); }
.agent.write{ border-left-color:var(--write); }
.agent.critic{ border-left-color:var(--critic); }
.agent.approved{ border-left-color:var(--ok); }
.agent .hd{ display:flex; align-items:center; gap:.7rem; margin-bottom:.45rem; }
.agent .badge{ font-family:'JetBrains Mono',monospace; font-size:.63rem; letter-spacing:.12em; color:var(--ink); padding:.16rem .55rem; border-radius:3px; font-weight:600; }
.agent.plan .badge{ background:var(--plan); color:#fff; }
.agent.research .badge{ background:var(--research); color:#fff; }
.agent.write .badge{ background:var(--write); }
.agent.critic .badge{ background:var(--critic); color:#fff; }
.agent.approved .badge{ background:var(--ok); color:#fff; }
.agent .who{ font-size:.95rem; font-weight:500; color:var(--parchment); }
.agent .body{ font-size:.87rem; color:var(--muted); line-height:1.65; }
.agent .body b{ color:var(--parchment); font-weight:500; }
.qlist{ margin:.6rem 0 0; padding-left:0; list-style:none; }
.qlist li{ font-size:.86rem; color:var(--parchment); padding:.32rem 0 .32rem .9rem; border-left:1px solid var(--gold-dim); margin-bottom:.25rem; }
.loopcard{ background:linear-gradient(90deg,rgba(201,169,106,.10),transparent); border:1px solid var(--gold-dim); border-radius:8px; padding:.9rem 1.2rem; margin:.7rem 0; }
.loopcard .t{ font-family:'JetBrains Mono',monospace; font-size:.68rem; letter-spacing:.16em; color:var(--gold); text-transform:uppercase; }
.loopcard .d{ font-size:.87rem; color:var(--parchment); margin-top:.35rem; }
.report{ background:var(--panel); border:1px solid var(--gold-dim); border-radius:10px; padding:1.6rem 1.8rem; margin-top:.4rem; }
.report .lbl{ font-family:'JetBrains Mono',monospace; font-size:.65rem; letter-spacing:.2em; color:var(--gold); text-transform:uppercase; margin-bottom:.9rem; }
.sec-h{ display:flex; align-items:baseline; gap:.8rem; margin:1.7rem 0 .8rem; }
.sec-h .num{ font-family:'JetBrains Mono',monospace; font-size:.67rem; color:var(--gold); letter-spacing:.14em; }
.sec-h .t{ font-family:'Cormorant Garamond',serif; font-size:1.5rem; font-weight:400; color:var(--parchment); }
[data-testid="stSidebar"]{ background:#080A0E; border-right:1px solid var(--line); }
[data-testid="stSidebar"] .sb-mark{ font-family:'JetBrains Mono',monospace; font-size:.71rem; letter-spacing:.22em; color:var(--gold); padding:.4rem 0 .2rem; }
[data-testid="stSidebar"] .sb-name{ font-family:'Cormorant Garamond',serif; font-size:1.3rem; color:var(--parchment); line-height:1.2; }
[data-testid="stSidebar"] .sb-sec{ font-family:'JetBrains Mono',monospace; font-size:.63rem; letter-spacing:.18em; text-transform:uppercase; color:var(--gold); margin:1.3rem 0 .3rem; padding-top:1rem; border-top:1px solid var(--line); }
[data-testid="stSidebar"] label{ color:var(--muted) !important; font-size:.81rem !important; }
.stTextInput input, .stTextArea textarea{ background:var(--panel) !important; color:var(--parchment) !important; border:1px solid var(--line) !important; border-radius:6px !important; font-size:.94rem !important; }
.stTextInput input:focus{ border-color:var(--gold) !important; box-shadow:none !important; }
.stFormSubmitButton>button, .stButton>button{ background:transparent; color:var(--parchment); border:1px solid var(--gold-dim); border-radius:6px; font-size:.85rem; letter-spacing:.04em; padding:.5rem 1.1rem; transition:.25s; width:100%; }
.stFormSubmitButton>button:hover, .stButton>button:hover{ border-color:var(--gold); color:var(--gold-bright); background:rgba(201,169,106,.06); }
.stFormSubmitButton>button[kind="primaryFormSubmit"], .stButton>button[kind="primary"]{ background:var(--gold); color:var(--ink); border-color:var(--gold); font-weight:600; }
[data-testid="stForm"]{ border:none !important; padding:0 !important; }
.streamlit-expanderHeader{ background:var(--panel) !important; color:var(--muted) !important; border:1px solid var(--line) !important; border-radius:6px !important; font-size:.81rem !important; }
[data-testid="stExpanderDetails"]{ background:var(--panel); border:1px solid var(--line); border-top:none; border-radius:0 0 6px 6px; }
code{ color:var(--gold-bright) !important; background:rgba(201,169,106,.08) !important; }
hr{ border-color:var(--line); }
.pill{ display:inline-flex; align-items:center; gap:.45rem; font-family:'JetBrains Mono',monospace; font-size:.67rem; letter-spacing:.06em; padding:.35rem .7rem; border-radius:4px; border:1px solid var(--line); }
.pill .dot{ width:6px; height:6px; border-radius:50%; }
.pill.ok{ color:var(--ok); } .pill.ok .dot{ background:var(--ok); }
.pill.bad{ color:var(--critic); } .pill.bad .dot{ background:var(--critic); }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
#  PROJECT IMPORTS
# ══════════════════════════════════════════════════════════════════════
IMPORT_ERROR = None
try:
    from graph import research_agent
    from redis import Redis
except Exception as exc:                     # pragma: no cover
    IMPORT_ERROR = exc


@st.cache_data(ttl=300, show_spinner=False)
def serpapi_status() -> tuple:
    """Presence of the key proves nothing — an invalid key fails silently and the
    Writer then fabricates the whole report. Spend one cheap call to be sure."""
    key = os.getenv("SERPAPI_API_KEY")
    if not key:
        return False, "missing"
    try:
        import requests
        r = requests.get("https://serpapi.com/account",
                         params={"api_key": key}, timeout=6)
        if r.status_code == 401:
            return False, "invalid key"
        if r.status_code != 200:
            return False, f"HTTP {r.status_code}"
        left = r.json().get("total_searches_left")
        return True, (f"{left:,} searches left" if left is not None else "valid")
    except Exception as exc:
        return False, type(exc).__name__


@st.cache_data(ttl=10, show_spinner=False)
def redis_status(host: str, port: int) -> tuple:
    """(ok, detail). `ok` is False if Redis is up but lacks the search module,
    because LangGraph's checkpointer needs RediSearch (FT.* commands).

    Cached for 10s: the probe pays a full socket timeout when Redis is down, and
    Streamlit re-runs the sidebar on every interaction — without the cache each
    button press would stall for seconds.
    """
    try:
        r = Redis(host=host, port=port, socket_connect_timeout=1.5)
        r.ping()
    except Exception as exc:
        return False, type(exc).__name__
    try:
        r.execute_command("FT._LIST")
    except Exception:
        return False, "no RediSearch"
    try:
        return True, f"{len(r.keys('checkpoint*')):,} checkpoints"
    except Exception:
        return True, "connected"


def wipe_checkpoints(host: str, port: int) -> tuple:
    """Delete every saved graph state.

    Redis here is a checkpointer, not a vector store: it holds the plan, research
    and drafts for each thread_id. Clearing it forces the four agents to run from
    scratch instead of resuming a thread that already finished.
    """
    try:
        r = Redis(host=host, port=port, socket_connect_timeout=3)
        r.ping()
        keys = [k for pat in ("checkpoint*", "*checkpoint*", "writes*")
                for k in r.keys(pat)]
        keys = list({k for k in keys})
        if keys:
            r.delete(*keys)
        return True, len(keys)
    except Exception as exc:
        return False, f"{type(exc).__name__}: {exc}"


AGENTS = {
    "planner":    ("PLANNER",    "plan",     "Breaking the topic into searchable questions"),
    "researcher": ("RESEARCHER", "research", "Running each question through live web search"),
    "writer":     ("WRITER",     "write",    "Drafting the report from the gathered material"),
    "critic":     ("CRITIC",     "critic",   "Reviewing the draft against the original question"),
}


# ══════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown('<div class="sb-mark">M.AFIFY</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-name">Control panel</div>', unsafe_allow_html=True)

    st.markdown('<div class="sb-sec">Review policy</div>', unsafe_allow_html=True)
    max_revisions = st.slider(
        "Maximum revisions", 1, 5, int(os.getenv("MAX_REVISIONS", 2)),
        help="How many times the Critic may send the draft back before the report is accepted as-is.",
    )
    os.environ["MAX_REVISIONS"] = str(max_revisions)

    st.markdown('<div class="sb-sec">Infrastructure</div>', unsafe_allow_html=True)
    redis_host = st.text_input("Redis host", os.getenv("REDIS_HOST", "localhost"))
    redis_port = int(st.text_input("Redis port", os.getenv("REDIS_PORT", "6379")) or 6379)

    if IMPORT_ERROR is None:
        up, detail = redis_status(redis_host, redis_port)
        st.markdown(f'<span class="pill {"ok" if up else "bad"}"><span class="dot"></span>'
                    f'REDIS · {detail}</span>', unsafe_allow_html=True)
    serp_ok, serp_detail = serpapi_status()
    groq_ok = bool(os.getenv("GROQ_API_KEY"))
    st.markdown(f'<span class="pill {"ok" if serp_ok else "bad"}" style="margin-top:.5rem">'
                f'<span class="dot"></span>SERPAPI · {serp_detail}</span>',
                unsafe_allow_html=True)
    if not serp_ok:
        st.caption("Without live search the Writer has nothing to work from and will "
                   "invent the report. Fix the key before trusting any output.")
    st.markdown(f'<span class="pill {"ok" if groq_ok else "bad"}" style="margin-top:.5rem">'
                f'<span class="dot"></span>GROQ KEY · {"loaded" if groq_ok else "missing"}</span>',
                unsafe_allow_html=True)

    st.markdown('<div class="sb-sec">Session</div>', unsafe_allow_html=True)
    if st.button("Reset session log"):
        st.session_state.runs = []
        st.rerun()
    st.caption("Clears the run log on this page. Saved graph states are kept.")

    st.markdown('<div class="sb-sec">Danger zone</div>', unsafe_allow_html=True)
    if not st.session_state.get("confirm_wipe"):
        if st.button("Wipe saved states"):
            st.session_state.confirm_wipe = True
            st.rerun()
        st.caption("Deletes every Redis checkpoint so a repeated topic runs the four "
                   "agents again instead of resuming a finished thread.")
    else:
        st.warning("Delete every saved graph state?")
        c1, c2 = st.columns(2)
        if c1.button("Yes, wipe"):
            ok, info = wipe_checkpoints(redis_host, redis_port)
            st.session_state.confirm_wipe = False
            st.session_state.wipe_msg = (
                (f"Deleted {info:,} keys. Every topic now starts cold."
                 if info else "No saved states were found — already clean.")
                if ok else f"Could not wipe — {info}")
            st.rerun()
        if c2.button("Cancel"):
            st.session_state.confirm_wipe = False
            st.rerun()
    if st.session_state.get("wipe_msg"):
        st.caption(st.session_state.pop("wipe_msg"))


# ══════════════════════════════════════════════════════════════════════
#  MASTHEAD
# ══════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="masthead">
  <div class="kicker">LangGraph &nbsp;·&nbsp; SerpAPI &nbsp;·&nbsp; Redis</div>
  <div class="title">Multi-Agent <em>Researcher</em></div>
  <div class="tagline">Plan · Research · Write · Critique</div>
  <p class="sub">Four agents share one task. The Critic reads the draft and can send it
  straight back to the Writer — the loop runs until the report holds up, or the revision
  budget runs out.</p>
</div>
""", unsafe_allow_html=True)

if IMPORT_ERROR is not None:
    msg = str(IMPORT_ERROR)
    if "FT._LIST" in msg or "unknown command" in msg.lower():
        st.error("Redis is running, but it is not Redis Stack.")
        st.markdown(
            "LangGraph's checkpointer builds its indexes with RediSearch (`FT.*`) commands, "
            "which the plain `redis:7` image does not ship. Swap the container:\n\n"
            "```bash\n"
            "docker compose down\n"
            "docker rm -f redis          # free port 6379 from the plain image\n"
            "docker compose up -d        # brings up redis/redis-stack\n"
            "docker exec -it redis-stack redis-cli FT._LIST   # should print an empty list\n"
            "```"
        )
    else:
        st.error(f"Project modules could not be loaded — {type(IMPORT_ERROR).__name__}: {IMPORT_ERROR}")
        st.caption("Check that graph.py, agents.py and state.py are importable and Redis is reachable.")
    st.stop()

if "runs" not in st.session_state:
    st.session_state.runs = []

total_runs = len(st.session_state.runs)
total_rev = sum(r["revisions"] for r in st.session_state.runs)
avg_s = (sum(r["secs"] for r in st.session_state.runs) / total_runs) if total_runs else 0
st.markdown(f"""
<div class="strip">
  <div class="cell"><span class="n">{total_runs}</span><span class="l">Reports produced</span></div>
  <div class="cell"><span class="n">{total_rev}</span><span class="l">Revisions demanded</span></div>
  <div class="cell"><span class="n">{avg_s:.0f}<span style="font-size:.85rem">s</span></span><span class="l">Avg run time</span></div>
  <div class="cell"><span class="n">{max_revisions}</span><span class="l">Revision budget</span></div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════
#  QUERY
# ══════════════════════════════════════════════════════════════════════
st.markdown('<div class="sec-h"><span class="num">01</span><span class="t">Commission a report</span></div>',
            unsafe_allow_html=True)

EXAMPLES = [
    "The state of agentic AI in 2026",
    "How vector databases handle billion-scale search",
    "What changed in EU AI regulation this year",
]
cols = st.columns(len(EXAMPLES))
for col, ex in zip(cols, EXAMPLES):
    if col.button(ex, key=f"ex_{ex[:18]}"):
        st.session_state.prefill = ex

with st.form("topic_form"):
    topic = st.text_input(
        "Topic",
        value=st.session_state.pop("prefill", ""),
        placeholder="Give the team a topic — they will plan, research, write and review it.",
        label_visibility="collapsed",
    )
    run = st.form_submit_button("Brief the team  →", type="primary")


# ══════════════════════════════════════════════════════════════════════
#  RUN
# ══════════════════════════════════════════════════════════════════════
if run:
    if not topic.strip():
        st.warning("Enter a topic to brief the team.")
        st.stop()

    st.markdown('<div class="sec-h"><span class="num">02</span><span class="t">The newsroom</span></div>',
                unsafe_allow_html=True)

    trace = st.container()
    plan, searches, revisions, drafts = [], 0, 0, []
    final_report, last_feedback = "", ""
    writer_passes = 0
    started = time.perf_counter()

    # A stable thread id per topic+budget so Redis checkpoints don't collide
    thread_id = f"{abs(hash(topic)) % 10**10}-{max_revisions}"
    config = {"configurable": {"thread_id": thread_id}}

    try:
        with st.spinner("The team is working…"):
            for update in research_agent.stream(
                {"query": topic, "research_data": [], "revision_count": 0},
                config=config, stream_mode="updates",
            ):
                for node, payload in update.items():
                    label, css, blurb = AGENTS.get(node, (node.upper(), "", ""))

                    # ---------- planner ----------
                    if node == "planner":
                        plan = payload.get("plan", [])
                        items = "".join(f"<li>{q}</li>" for q in plan)
                        with trace:
                            st.markdown(f"""
                            <div class="agent plan">
                              <div class="hd"><span class="badge">{label}</span>
                                <span class="who">Broke the topic into {len(plan)} questions</span></div>
                              <div class="body">{blurb}</div>
                              <ul class="qlist">{items}</ul>
                            </div>""", unsafe_allow_html=True)

                    # ---------- researcher ----------
                    elif node == "researcher":
                        data = payload.get("research_data", [])
                        searches = len(data)
                        chars = sum(len(d) for d in data)
                        failed = sum(1 for d in data if "SEARCH FAILED" in d)
                        with trace:
                            st.markdown(f"""
                            <div class="agent research">
                              <div class="hd"><span class="badge">{label}</span>
                                <span class="who">Ran {searches} searches, gathered {chars:,} characters</span></div>
                              <div class="body">{blurb}</div>
                            </div>""", unsafe_allow_html=True)
                            if failed:
                                st.error(f"{failed} of {searches} searches failed — the report "
                                         f"below is not grounded in live sources.")
                                st.caption("Check SERPAPI_API_KEY. The agents will still run, "
                                           "but the Writer has little or nothing to cite.")
                            with st.expander("Raw search results"):
                                for d in data:
                                    st.text(d[:1500] + ("…" if len(d) > 1500 else ""))

                    # ---------- writer ----------
                    elif node == "writer":
                        draft = payload.get("draft", "")
                        drafts.append(draft)
                        writer_passes += 1
                        words = len(draft.split())
                        title = ("Wrote the first draft" if writer_passes == 1
                                 else f"Rewrote the draft (pass {writer_passes})")
                        with trace:
                            st.markdown(f"""
                            <div class="agent write">
                              <div class="hd"><span class="badge">{label}</span>
                                <span class="who">{title} — {words:,} words</span></div>
                              <div class="body">{blurb}</div>
                            </div>""", unsafe_allow_html=True)
                            with st.expander(f"Draft {writer_passes}"):
                                st.markdown(draft)

                    # ---------- critic ----------
                    elif node == "critic":
                        fb = (payload.get("feedback") or "").strip()
                        last_feedback = fb
                        approved = fb.lower().startswith("approved")
                        with trace:
                            st.markdown(f"""
                            <div class="agent {'approved' if approved else 'critic'}">
                              <div class="hd"><span class="badge">{label}</span>
                                <span class="who">{'Approved the report' if approved else 'Sent it back for revision'}</span></div>
                              <div class="body">{blurb}</div>
                            </div>""", unsafe_allow_html=True)
                            if not approved and fb:
                                revisions += 1
                                with st.expander("What the Critic asked for"):
                                    st.markdown(fb)
                                st.markdown(f"""
                                <div class="loopcard">
                                  <div class="t">↺ Revision {revisions} of {max_revisions}</div>
                                  <div class="d">The draft goes back to the Writer. This edge is what
                                  separates a pipeline from a loop.</div>
                                </div>""", unsafe_allow_html=True)

        elapsed = time.perf_counter() - started
        final_report = drafts[-1] if drafts else ""
        st.session_state.runs.append({"topic": topic, "secs": elapsed,
                                      "revisions": revisions, "searches": searches})

        # ---------- report ----------
        st.markdown('<div class="sec-h"><span class="num">03</span><span class="t">The report</span></div>',
                    unsafe_allow_html=True)
        if final_report:
            st.markdown('<div class="report"><div class="lbl">Final draft</div>', unsafe_allow_html=True)
            st.markdown(final_report)
            st.markdown('</div>', unsafe_allow_html=True)
            st.download_button("Download as Markdown", final_report,
                               file_name=f"report-{thread_id}.md", mime="text/markdown")
        else:
            st.info("The graph finished without producing a draft — review the trace above.")

        st.markdown(f"""
        <div class="strip" style="margin-top:1.5rem">
          <div class="cell"><span class="n">{len(plan)}</span><span class="l">Questions planned</span></div>
          <div class="cell"><span class="n">{searches}</span><span class="l">Searches run</span></div>
          <div class="cell"><span class="n">{revisions}</span><span class="l">Revisions demanded</span></div>
          <div class="cell"><span class="n">{elapsed:.0f}<span style="font-size:.85rem">s</span></span><span class="l">Total time</span></div>
        </div>""", unsafe_allow_html=True)

        if revisions:
            st.caption(f"The Writer produced {writer_passes} drafts because the Critic rejected "
                       f"{revisions}. Without that loop you would be reading draft one.")

    except Exception as exc:
        st.error(f"The run failed — {type(exc).__name__}: {exc}")
        st.caption("Check that Redis is reachable and that SERPAPI_API_KEY and GROQ_API_KEY are set.")


# ══════════════════════════════════════════════════════════════════════
#  HISTORY
# ══════════════════════════════════════════════════════════════════════
if st.session_state.runs:
    st.markdown('<hr class="rule">', unsafe_allow_html=True)
    with st.expander(f"Session history — {len(st.session_state.runs)} report(s)"):
        for i, r in enumerate(reversed(st.session_state.runs), 1):
            st.markdown(
                f"**{i}.** {r['topic']}  \n"
                f"<span style='color:#8A8F9A;font-size:.8rem;font-family:JetBrains Mono,monospace'>"
                f"{r['searches']} searches · {r['revisions']} revisions · {r['secs']:.0f}s</span>",
                unsafe_allow_html=True)

st.markdown(
    "<div style='text-align:center;color:#8A8F9A;font-family:JetBrains Mono,monospace;"
    "font-size:.65rem;letter-spacing:.12em;margin-top:2.4rem'>"
    "MULTI-AGENT DEEP RESEARCHER · MOHAMED MOSTAFA HASSAN AFIFY</div>",
    unsafe_allow_html=True)