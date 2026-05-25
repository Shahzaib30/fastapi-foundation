from fastapi import APIRouter, HTTPException

from app.core.config import ME_FILE
from app.schemas import UserProfile
from app.services.json_store import load_json_file

router = APIRouter(tags=["Users"])


@router.get("/me")
async def get_me():
    data = load_json_file(ME_FILE, default=[])
    return data


@router.get("/users")
async def list_users(skills: str | None = None):
    data = load_json_file(ME_FILE, default=[])
    if not skills:
        return {"users": data}

    skills_list = [skill.strip() for skill in skills.split(",") if skill.strip()]
    filtered = [
        user
        for user in data
        if any(skill in user.get("technical_stack", []) for skill in skills_list)
    ]
    return {"users": filtered}


@router.get("/users/{user_id}", response_model=UserProfile)
async def get_user(user_id: str):
    data = load_json_file(ME_FILE, default=[])
    for user in data:
        if user.get("id") == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")
