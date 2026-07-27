import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.redis import RedisSaver
from redis import Redis
from state import ResearchState
from agents import planner_node, researcher_node, writer_node, critic_node, critic_router

load_dotenv()

def build_graph():
    workflow = StateGraph(ResearchState)

    workflow.add_node("planner", planner_node)
    workflow.add_node("researcher", researcher_node)
    workflow.add_node("writer", writer_node)
    workflow.add_node("critic", critic_node)

    workflow.add_edge(START, "planner")
    workflow.add_edge("planner", "researcher")
    workflow.add_edge("researcher", "writer")
    workflow.add_edge("writer", "critic")
    workflow.add_conditional_edges("critic", critic_router)

    # Redis connection is env-driven so the app and docker-compose agree
    redis_client = Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", 6379)),
    )
    checkpointer = RedisSaver(redis_client=redis_client)
    
    # ده علشان يبني indexes جوه الداتا بيز
    checkpointer.setup()
    
    # بنعمل Compile وبنديله الـ Checkpointer عشان يحفظ كل خطوة أوتوماتيك
    research_agent = workflow.compile(checkpointer=checkpointer)
    return research_agent

# بنجهز الـ Agent عشان نستخدمه في أي مكان تاني
research_agent = build_graph()