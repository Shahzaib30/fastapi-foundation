from __future__ import annotations

from typing import TypedDict

from langchain_core.messages import HumanMessage
from langchain_ollama import ChatOllama
from langgraph.graph import END, StateGraph

from app.core.config import OLLAMA_MODEL, OLLAMA_BASE_URL


class ProposalState(TypedDict, total=False):
    project_goal: str
    draft: str
    critique: str
    final_output: str


def build_llm() -> ChatOllama:
    return ChatOllama(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL)


def build_proposal_graph():
    llm = build_llm()

    def draft_node(state: ProposalState) -> ProposalState:
        prompt = f"Project Goal: {state['project_goal']}\n\nDraft a proposal for this project."
        response = llm.invoke([HumanMessage(content=prompt)])
        return {"draft": response.content}

    def critique_node(state: ProposalState) -> ProposalState:
        prompt = (
            f"Draft: {state['draft']}\n\nCritique the above draft and tell me if it is good or bad, why, and how to improve it."
        )
        response = llm.invoke([HumanMessage(content=prompt)])
        return {"critique": response.content}

    def finalize_node(state: ProposalState) -> ProposalState:
        prompt = (
            f"Draft: {state['draft']}\nCritique: {state['critique']}\n\nBased on the draft and critique, finalize the proposal."
        )
        response = llm.invoke([HumanMessage(content=prompt)])
        return {"final_output": response.content}

    workflow = StateGraph(ProposalState)
    workflow.add_node("draft", draft_node)
    workflow.add_node("critique", critique_node)
    workflow.add_node("finalize", finalize_node)
    workflow.set_entry_point("draft")
    workflow.add_edge("draft", "critique")
    workflow.add_edge("critique", "finalize")
    workflow.add_edge("finalize", END)
    return workflow.compile()
