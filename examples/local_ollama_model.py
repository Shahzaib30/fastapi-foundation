from openai import OpenAI
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
from uuid import UUID
from pydantic import BaseModel, Field, EmailStr
from typing import List


client = OpenAI(base_url="http://localhost:11434/v1/", api_key="ollama")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProjectModel(BaseModel):
    title: str = Field(...)
    client_name: str = Field(...)
    budget: float = Field(..., gt=0)
    is_completed: bool = Field(default=False)


class DeveloperModel(BaseModel):
    id: UUID = Field(...)
    name: str = Field(...)
    email: EmailStr = Field(...)
    skills: List[str] = Field(...)
    current_projects: List[ProjectModel]


data_file = "developers.json"


def load_data():
    try:
        with open(data_file, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except (json.JSONDecodeError, FileNotFoundError):
        return []


def save_data(data):
    with open(data_file, "w", encoding="utf-8") as handle:
        json.dump(data, handle)


@app.post("/developers/")
async def create_developer(developers: List[DeveloperModel]):
    data = load_data()
    for developer in developers:
        data.append(developer.model_dump(mode="json"))
    save_data(data)
    return {"message": "Developers added successfully", "developers": developers}


@app.get("/developers/", response_model=List[DeveloperModel])
async def all_developers():
    return load_data()


@app.put("/developers/{dev_id}", response_model=DeveloperModel)
async def update_developer(dev_id: UUID, updated_developer: DeveloperModel):
    data = load_data()
    for index, dev in enumerate(data):
        if dev["id"] == str(dev_id):
            data[index] = updated_developer.model_dump(mode="json")
            save_data(data)
            return updated_developer
    raise HTTPException(status_code=404, detail="Developer not found")


@app.delete("/developers/{dev_id}", status_code=204)
async def delete_developer(dev_id: UUID):
    data = load_data()
    new_data = [dev for dev in data if dev["id"] != str(dev_id)]
    if len(new_data) == len(data):
        raise HTTPException(status_code=404, detail="Developer not found")

    save_data(new_data)
    return None


@app.post("/developers/{dev_id}/generate_proposal")
async def generate_proposal(dev_id: UUID, project_goal: str):
    data = load_data()
    dev = next((dev for dev in data if dev["id"] == str(dev_id)), None)
    if not dev:
        raise HTTPException(status_code=404, detail="Developer not found")

    prompt = (
        f"Generate a project proposal for a developer with the following profile:\nName: {dev['name']}\n"
        f"Email: {dev['email']}\nSkills: {', '.join(dev['skills'])}\n"
        f"Current Projects: {', '.join([proj['title'] for proj in dev['current_projects']])}\n\nProject Goal: {project_goal}\n\nProposal:"
    )

    response = client.chat.completions.create(
        model="qwen2.5-coder:7b",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that generates project proposals based on developer profiles and project goals."},
            {"role": "user", "content": prompt},
        ],
    )
    return {"developer": dev["name"], "proposal": response.choices[0].message.content}
