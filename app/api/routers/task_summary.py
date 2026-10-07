from fastapi import APIRouter, Depends
from typing import Dict

from app.services import task_service

router = APIRouter()

async def get_current_user() -> Dict:
    """
    Dependency to get the current authenticated user.
    This should be replaced or overridden by the actual authentication mechanism.
    """
    # Placeholder implementation; in production, this would extract user info from JWT or session
    raise NotImplementedError("Authentication dependency not implemented")

@router.get("/summary", response_model=Dict[str, int])
async def get_task_summary_endpoint(current_user: Dict = Depends(get_current_user)) -> Dict[str, int]:
    """
    GET /summary endpoint to return a summary of the user's tasks.
    Returns JSON with 'total' and 'pending' task counts.

    US-0001 AC-1: Uses findAll(userId) via service layer to count tasks.
    US-0001 AC-2: Returns JSON with 'total' and 'pending'.
    US-0001 AC-4 and AC-5: Returns correct counts even if zero or some tasks.
    """
    user_id = current_user["id"]
    summary = await task_service.get_task_summary(user_id)  # US-0001 AC-1
    # Ensure keys 'total' and 'pending' exist in summary
    total = summary.get("total", 0)
    pending = summary.get("pending", 0)
    return {"total": total, "pending": pending}  # US-0001 AC-2
