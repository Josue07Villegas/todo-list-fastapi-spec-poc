from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, validator
from typing import Optional
from app.services.sample_item_service import TaskService
from app.dependencies import get_current_user, get_task_service

router = APIRouter()

class TaskCreateRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    state: Optional[str] = None
    priority: Optional[str] = None

    @validator("state")
    def validate_state(cls, v):
        valid_states = {"pending", "in_progress", "completed"}
        if v is not None and v not in valid_states:
            raise ValueError(f"Estado inválido. Valores permitidos: {', '.join(valid_states)}.")
        return v

    @validator("priority")
    def validate_priority(cls, v):
        valid_priorities = {"low", "medium", "high"}
        if v is not None and v not in valid_priorities:
            raise ValueError(f"Prioridad inválida. Valores permitidos: {', '.join(valid_priorities)}.")
        return v

@router.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(
    task_data: TaskCreateRequest,
    current_user=Depends(get_current_user),
    service: TaskService = Depends(get_task_service),
):
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")  # US-0001 AC-1

    try:
        created_task = service.create_task(task_data.dict(exclude_unset=True), user_id=current_user.id)
    except Exception as e:
        # Assuming ValidationError or similar
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e))  # US-0001 AC-7

    return created_task  # US-0001 AC-6
