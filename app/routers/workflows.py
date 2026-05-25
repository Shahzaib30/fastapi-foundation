from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.schemas import ProposalRequest, WorkflowProposalResponse
from app.services.workflows import build_proposal_graph

router = APIRouter(prefix="/workflows", tags=["Workflows"])

proposal_graph = build_proposal_graph()


@router.post("/proposal", response_model=WorkflowProposalResponse)
async def generate_proposal_workflow(payload: ProposalRequest):
    try:
        result = proposal_graph.invoke({"project_goal": payload.project_goal})
        return {
            "draft": result.get("draft", ""),
            "critique": result.get("critique", ""),
            "final_output": result.get("final_output", ""),
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
