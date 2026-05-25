from fastapi import FastAPI, HTTPException, status
import json
from typing import Optional


def load_data():
    with open("me.json", "r", encoding="utf-8") as handle:
        return json.load(handle)


app = FastAPI()


@app.get("/")
async def hello():
    return {"message": "Hello World"}


@app.get("/greet/{name}")
async def greet(name: str):
    return {"message": f"Hello, {name}!"}


@app.get("/about")
async def about():
    return {"message": "This is a simple FastAPI application."}


@app.get("/me")
async def get_me():
    return load_data()


@app.get("/users")
async def get_users(skills: Optional[str] = None):
    data = load_data()
    if not skills:
        return {"users": data}

    skills_list = [skill.strip() for skill in skills.split(",") if skill.strip()]
    return {"users": [user for user in data if any(skill in user.get("technical_stack", []) for skill in skills_list)]}


@app.get("/users/{user_id}")
async def get_user(user_id: str):
    for user in load_data():
        if user.get("id") == user_id:
            return user
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
