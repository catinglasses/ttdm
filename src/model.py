from typing import Optional
from datetime import datetime

class Task:
    """Класс задач. Аналог моделей для БД, слой данных."""
    def __init__(self, task_id: int, title: str, description: Optional[str], category: Optional[str], deadline: Optional[datetime], priority: str = "низкий", completed: bool = False):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.category = category
        self.deadline = deadline
        self.priority = priority
        self.completed = completed

    def to_dict(self) -> dict:
        """Преобразование задачи в словарь для сохранения в JSON."""
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "priority": self.priority,
            "completed": self.completed
        }
