from __future__ import annotations

from typing import List
from uuid import UUID

from fastapi import APIRouter, HTTPException
from openai import OpenAI

from app.core.config import DEVELOPERS_FILE, OLLAMA_API_KEY, OLLAMA_BASE_URL, OLLAMA_MODEL
from app.schemas import DeveloperCreate, DeveloperRecord, DeveloperSummary, DeveloperUpdate, ProposalRequest, ProposalResponse
from app.services.json_store import load_json_file, save_json_file

router = APIRouter(prefix="/developers", tags=["Developers"])

client = OpenAI(base_url=OLLAMA_BASE_URL, api_key=OLLAMA_API_KEY)


def _load_developers() -> list[dict]:
    return load_json_file(DEVELOPERS_FILE, default=[])


def _save_developers(payload: list[dict]) -> None:
    save_json_file(DEVELOPERS_FILE, payload)


@router.get("/", response_model=List[DeveloperRecord])
async def all_developers():
    return _load_developers()


@router.post("/", response_model=List[DeveloperSummary])
async def create_developer(developers: List[DeveloperCreate]):
    data = _load_developers()
    summaries: list[DeveloperSummary] = []

    for developer in developers:
        total_budget = sum(project.budget for project in developer.current_projects)
        data.append(developer.model_dump(mode="json"))
        summaries.append(
            DeveloperSummary(
                message=f"Developer {developer.name} has {len(developer.current_projects)} projects with a total budget of {total_budget}.",
                project_count=len(developer.current_projects),
                total_value=total_budget,
            )
        )

    _save_developers(data)
    return summaries


@router.put("/{dev_id}", response_model=DeveloperRecord)
async def update_developer(dev_id: UUID, updated_developer: DeveloperUpdate):
    data = _load_developers()

    for index, developer in enumerate(data):
        if developer["id"] == str(dev_id):
            new_dev_dict = updated_developer.model_dump(mode="json")
            new_dev_dict["id"] = str(dev_id)
            data[index] = new_dev_dict
            _save_developers(data)
            return new_dev_dict

    raise HTTPException(status_code=404, detail="Developer not found")


@router.delete("/{dev_id}", status_code=204)
async def delete_developer(dev_id: UUID):
    data = _load_developers()
    new_data = [developer for developer in data if developer["id"] != str(dev_id)]
    if len(new_data) == len(data):
        raise HTTPException(status_code=404, detail="Developer not found")

    _save_developers(new_data)
    return None


@router.post("/{dev_id}/generate_proposal", response_model=ProposalResponse)
async def generate_proposal(dev_id: UUID, payload: ProposalRequest):
    data = _load_developers()
    developer = next((dev for dev in data if dev["id"] == str(dev_id)), None)
    if not developer:
        raise HTTPException(status_code=404, detail="Developer not found")

    prompt = (
        f"Generate a project proposal for a developer with the following profile:\n"
        f"Name: {developer['name']}\n"
        f"Email: {developer['email']}\n"
        f"Skills: {', '.join(developer.get('skills', []))}\n"
        f"Current Projects: {', '.join([project['title'] for project in developer.get('current_projects', [])])}\n\n"
        f"Project Goal: {payload.project_goal}\n\nProposal:"
    )

    response = client.chat.completions.create(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that generates project proposals based on developer profiles and project goals.",
            },
            {"role": "user", "content": prompt},
        ],
    )
    return {
        "developer": developer["name"],
        "proposal": response.choices[0].message.content,
    }
