
from fastapi import APIRouter

router = APIRouter()

@router.get("/health", tags=["Health"])
def health_check():
    """
    A simple endpoint to check if the API is running.
    """
    return {"status": "Healthy"}
