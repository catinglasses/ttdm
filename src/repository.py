import os
import json
from datetime import datetime

from .model import Task
from .utils import NoResultFound

class TaskRepository:
    """Класс для работы с хранилищем задач. Манипуляции объектом класса Task реализуются здесь. Слой доступа к данным (Data access layer)."""
    def __init__(self, filename):
        self.filename = filename
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        """Загрузка задач из файла JSON."""
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as file:
                task_data = json.load(file)
                for data in task_data:
                    data["deadline"] = datetime.fromisoformat(data["deadline"]) if data["deadline"] else None
                    new_task = Task(**data)
                    self.tasks.append(new_task)

    def save_tasks(self):
        """Сохранение задач в файл JSON."""
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([task.to_dict() for task in self.tasks], file, ensure_ascii=False)

    def add_task(self, new_task: Task):
        """Добавление новой задачи (транзакция)."""
        self.tasks.append(new_task)
        self.save_tasks()

    def delete_task(self, task_id: int) -> bool:
        """Удаление задачи по ID (транзакция)."""
        for task in self.tasks:
            if task.task_id == task_id:
                self.tasks.remove(task)
                self.save_tasks()
                return True
        return False

    def get_task(self, task_id: int) -> Task:
        """Получение задачи по ID. Если задача не найдена, то выбрасывает NoResultFound."""
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        raise NoResultFound(task_id)

    def get_tasks_by_category(self, category: str) -> list[Task]:
        """Получить список задач по категории"""
        return [task for task in self.tasks if task.category and task.category.lower() == category.lower()]

    def view_tasks(self) -> list[Task]:
        """Возвращает список всех задач."""
        return self.tasks
