import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.utilities import SerpAPIWrapper
from langchain_core.messages import HumanMessage
from langgraph.graph import END
from state import ResearchState

load_dotenv()

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
search = SerpAPIWrapper()

#2- First Agent (Planner)
def planner_node(state: ResearchState):
    print("👨‍💼 Planner: Creating a research plan...")
    prompt = f"""You are a research planner. Your task is to break down the following topic into 3 precise and concise research questions suitable for Google search.
    Topic: {state['query']}
    Return only the questions, each on a separate line, without any numbering or introductions."""
    
    response= llm.invoke([HumanMessage(content=prompt)])
    plan = [q.strip() for q in response.content.split('\n') if q.strip()]
    return {"plan": plan, "revision_count": state.get("revision_count", 0)}

#3- Sec Agent (Researcher)
def researcher_node(state: ResearchState):
    print(f"🕵️‍♂️ Researcher: Searching across {len(state['plan'])} topics...")
    gathered_data = []

    for q in state['plan']:
        print(f"   - Searching for: {q}")
        try:
            result = search.run(q)
            gathered_data.append(f"Search results for '{q}':\n{result}")
        except Exception as e:
            gathered_data.append(f"Error while searching for '{q}'")
                     
    return {"research_data": gathered_data}

#4- Third Agent (Writer)
def writer_node(state: ResearchState):
    print("✍️ Writer: Generating the report...")
    data_str = "\n\n".join(state['research_data'])

    prompt = f"""You are a professional report writer. Based on the following information, write a comprehensive and well-structured report on the requested topic.
    Requested topic: {state['query']}
    Available information: {data_str}

    Reviewer notes (if any): {state.get('feedback', 'No previous feedback')}
    """
    
    response= llm.invoke([HumanMessage(content=prompt)])
    return {"draft": response.content}

#5- Fourth Agent (Critic)
def critic_node(state: ResearchState):
    print("🧐 Critic: Reviewing the report...")

    prompt = f"""You are a strict quality reviewer. Read the following report and ensure it fully and accurately answers the original question.
    Original question: {state['query']}
    Report: {state['draft']}

    If the report is excellent and complete, write only the word "Approved" at the beginning of your response.
    If it needs revision, clearly provide feedback for the writer to improve it."""
    
    response = llm.invoke([HumanMessage(content=prompt)])
    feedback = response.content.strip()
    
    new_count = state.get("revision_count", 0) + 1
    
    # نستخدم in عشان لو الموديل حط نقطة أو مسافة جنب الكلمة
    if "Approved" in feedback or "approved" in feedback.lower() or "مقبول" in feedback or new_count >= 2:
        return {"feedback": "Approved", "revision_count": new_count}
    else:
        print("   ❌ The critic rejected the report and requested revisions!")
        return {"feedback": feedback, "revision_count": new_count}

# بنعمل شرط للمراجع: لو التقرير مقبول يقفل. لو مرفوض نرجع للكاتب تاني
def critic_router(state: ResearchState):
    if state.get("revision_count", 0) >= 2 or "مقبول" in state["feedback"] or "Approved" in state["feedback"]:
        return END
    else:
        return "writer"  # يرجع للكاتب يعدل