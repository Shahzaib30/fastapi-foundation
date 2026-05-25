from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/")
async def root():
    return {"message": "FastAPI Foundation is running"}


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/greet/{name}")
async def greet(name: str):
    return {"message": f"Hello, {name}!"}
