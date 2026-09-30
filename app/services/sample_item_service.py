from typing import Optional
from app.models.task import Task
from app.repositories.task_repository import TaskRepository
from app.services.exceptions import ValidationError

VALID_STATES = {"pending", "in_progress", "completed"}
VALID_PRIORITIES = {"low", "medium", "high"}
MAX_TITLE_LENGTH = 100

class TaskService:
    """Business logic layer for tasks."""

    def __init__(self, repository: TaskRepository) -> None:
        self.repository = repository

    def create_task(self, data: dict, user_id: int) -> Task:
        title = data.get("title", "").strip()
        if not title:
            raise ValidationError("El título no puede estar vacío.")  # US-0001 AC-2
        if len(title) > MAX_TITLE_LENGTH:
            raise ValidationError(f"El título no puede superar {MAX_TITLE_LENGTH} caracteres.")  # US-0001 AC-2

        state = data.get("state", "pending")
        if state not in VALID_STATES:
            raise ValidationError(f"Estado inválido. Valores permitidos: {', '.join(VALID_STATES)}.")  # US-0001 AC-3

        priority = data.get("priority", "medium")
        if priority not in VALID_PRIORITIES:
            raise ValidationError(f"Prioridad inválida. Valores permitidos: {', '.join(VALID_PRIORITIES)}.")  # US-0001 AC-4

        task = Task(
            title=title,
            state=state,
            priority=priority,
            user_id=user_id  # US-0001 AC-5
        )
        created_task = self.repository.create(task)
        return created_task  # US-0001 AC-6
