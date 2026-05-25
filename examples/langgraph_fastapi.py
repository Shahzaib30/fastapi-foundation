from typing import TypedDict
from uuid import UUID

from fastapi import FastAPI
from langgraph.graph import END, StateGraph
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage


app = FastAPI()
llm = ChatOllama(model="qwen2.5-coder:7b", base_url="http://localhost:11434")


class AgentState(TypedDict):
    project_goal: str
    draft: str
    critique: str
    good_or_bad: str
    final_output: str
    step_count: int


def draft_node(state: AgentState) -> AgentState:
    prompt = f"Project Goal: {state['project_goal']}\n\nDraft a proposal for this project."
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"draft": response.content}


def critique_node(state: AgentState) -> AgentState:
    prompt = f"Draft: {state['draft']}\n\nCritique the above draft and tell me is it good or bad and why and how to improve it."
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"critique": response.content, "good_or_bad": "good" if "good" in response.content.lower() else "bad"}


def finalize_node(state: AgentState) -> AgentState:
    prompt = f"Draft: {state['draft']}\nCritique: {state['critique']}\nGood or Bad: {state['good_or_bad']}\n\nBased on the draft and critique, finalize the proposal."
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"final_output": response.content}


def conditional_transition(state: AgentState) -> str:
    if state.get("step_count", 0) >= 3:
        return "finalize"
    return "finalize" if state.get("good_or_bad") == "good" else "draft"


workflow = StateGraph(AgentState)
workflow.add_node("draft", draft_node)
workflow.add_node("critique", critique_node)
workflow.add_node("finalize", finalize_node)
workflow.set_entry_point("draft")
workflow.add_edge("draft", "critique")
workflow.add_conditional_edges("critique", conditional_transition, {"finalize": "finalize", "draft": "draft"})
workflow.add_edge("finalize", END)
app_graph = workflow.compile()


@app.get("/status")
async def status():
    return {"status": "ok"}


@app.post("/generate-proposal/{dev_id}")
async def generate_proposal(dev_id: UUID, description: str):
    result = app_graph.invoke({"project_goal": description})
    return {"proposal": result["final_output"]}
