# 🕵️‍♂️ Multi-Agent Deep Researcher

A production-ready, stateful **Multi-Agent Collaboration Workflow** designed using **LangGraph**, **Groq (Llama 3.1 8B)**, and **SerpAPI**. This architecture simulates an enterprise research team featuring an autonomous coordination loop between a **Planner, Researcher, Writer, and Critic**. The system is fully decoupled, leveraging **Redis** as a state checkpointer to ensure persistent session caching, fault-tolerant retries, and asynchronous thread tracking.

---

## 🏗️ System Architecture & Multi-Agent Collaboration

The workflow operates as a stateful cyclic graph, passing a shared `ResearchState` object across specialized node agents. If a report fails to pass the quality assurance guardrails set by the Critic, the state is autonomously routed back to the Writer for iterative refinement.

```text
       [START]
          │
          ▼
   👨‍💼 Planner Node (Breaks query into 3 precise target topics)
          │
          ▼
   🕵️‍♂️ Researcher Node (Executes parallel web scraping via SerpAPI)
          │
          ▼
 ┌──► ✍️ Writer Node (Compiles unstructured payload into markdown report)
 │        │
 │        ▼
 │ 🧐 Critic Node (Performs deterministic/semantic review evaluation)
 │        │
 └────────┴──► [Condition: Approved OR Max Revisions (>=2)?]
                  │
                  ├──► [YES] ──► [END] (Persisted to memory)
                  └──► [NO]  ──► (Loop back to Writer with feedback)
```

### Advanced Architectural Engineering
1. **State Isolation & Append Channels (`ResearchState`):** The data scraped by the researcher is accumulated safely using `operator.add` to prevent race conditions or partial document data loss between pipeline iterations.
2. **Persistent Session Layer (Redis Checkpointer):** Every state transition, agent decision, and intermediate payload is dynamically stored in a localized Redis container instance using `RedisSaver`. If a network failure occurs midway through research compilation, the thread context remains securely intact.
3. **Infinite Loop Mitigation:** The Critic tracks a `revision_count` parameter. If a report requires excessive iterations, the router automatically intervenes at the second attempt, forcing an elegant fallback termination to protect API token consumption.

---

## 🛠️ Tech Stack & Infrastructure

* **Multi-Agent Orchestration:** LangGraph & LangChain Custom StateGraph Engine
* **LLM Core Intelligence:** Groq API Node Platform (`llama-3.1-8b-instant`)
* **State Management & Caching:** Redis Engine (`RedisSaver` checkpointer tracking runtime states)
* **External Web Search Provider:** SerpAPI Wrapper Utilities (Google Search Data Extraction)
* **Application Framework:** Streamlit (Custom interface with automated execution handling and decoupled thread configs)

---

## 📂 Detailed Code Architecture Breakdown

```text
MULTI_AGENT_RESEARCHER/
│
├── src/
│   ├── agents.py                 # Concrete implementations of the 4 specialized agent workflows
│   ├── app.py                    # Streamlit presentation and thread runtime layer
│   ├── graph.py                  # LangGraph architecture mapping, edge logic, and Redis saver setup
│   └── state.py                  # TypedDict data schema structure for core memory sharing
│
├── docker-compose.yml           # Pre-configured container setup for the persistent Redis layer
├── .env                         # Sensitive runtime configuration tokens (Git-ignored)
├── requirements.txt             # Verified python package deployment manifest
└── README.md                    # In-depth technical repository breakdown documentation
```

### Structural Overview
* **`src/state.py`**: Declares the structure of `ResearchState`. Tracks user input, generated sub-plans, accumulative string lists for collected data, active draft versions, and qualitative critic evaluations.
* **`src/agents.py`**: Handles prompts and runtime executions for individual team members. The Researcher orchestrates data scraping loops via SerpAPI, while the Critic employs zero-shot evaluation syntax to output binary keywords ("Approved") alongside descriptive optimization reports.
* **`src/graph.py`**: Chains conditional route edges (`critic_router`) to control agent pathways. Configures index setups across the Redis connection client.
* **`src/app.py`**: Dynamically generates unique thread identifiers based on the input search string to cleanly compartmentalize and persist historical multi-user search requests inside Redis.

---

## 🚀 Deployment & Installation Guide

### 1. Prerequisites
Ensure you have **Docker Desktop** and **Python 3.10+** operational on your native machine.

### 2. Configure Environment Secrets
Create a `.env` file in your root folder layout and specify your service provider keys:
```env
GROQ_API_KEY=your_groq_api_key_here
SERPAPI_API_KEY=your_serpapi_api_key_here
```

### 3. Initialize the Redis Checkpointer Container
Boot up the isolated backend storage broker instance:
```bash
docker compose up -d
```
*This service exposes active port `6379` to interface directly with the LangGraph state machine runtime.*

### 4. Setup Python Environment & Dependencies
Initialize a clean environment sandbox and pull down required packages:
```bash
python -m venv venv
source venv/bin/activate  # On Windows terminal interfaces use: venv\Scripts\activate
pip install -r requirements.txt
```

### 5. Launch the Deep Research Interface
Boot up the presentation application layer:
```bash
streamlit run src/app.py
```

---

## 📊 Multi-User Execution Isolation
The system natively supports asynchronous multi-user isolation. When a prompt query is parsed via the UI layout, the script slices a localized `thread_id` slug:
```python
thread_id = query[:10].replace(" ", "_")
config = {"configurable": {"thread_id": thread_id}}
```
This enables the Redis checkpointer to cleanly separate data states across different search themes, ensuring high-concurrency safety.