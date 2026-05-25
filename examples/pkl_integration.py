from fastapi import FastAPI, HTTPException
import joblib
from contextlib import asynccontextmanager


model = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    model = joblib.load("project_classifier.pkl")
    print("Model loaded successfully")
    yield
    print("Shutting down application")
    model = None


app = FastAPI(lifespan=lifespan)


@app.post("/classify")
async def classify_project(description: str):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    prediction = model.predict([description])
    return {"project_type": prediction[0]}
