import time
import hashlib
from typing import Optional
from datetime import datetime

from .model import Task
from .utils import NoResultFound
from .repository import TaskRepository

class TaskSearcher:
    """Класс для поиска задач. 
    Функции, связанные с поиском объектов класса Task, реализуются здесь.
    Слой бизнес-логики (Service layer)."""
    @staticmethod
    def search(tasks: list[Task], keyword: Optional[str], category: Optional[str], completed: Optional[bool]) -> list[Task]:
        results = tasks

        if keyword:
            keyword = keyword.lower()
            results = [
                t for t in results if keyword in t.title.lower() or (t.description and keyword in t.description.lower())
                ]
        if category:
            results = [
                t for t in results if t.category and t.category.lower() == category.lower()
            ]
        if completed is not None:
            results = [
                t for t in results if t.completed == completed
            ]

        return results

class TaskManager:
    """Основной класс приложения. Все основные операции над объектами Task производятся здесь. Слой бизнес-логики (Service layer)."""
    last_timestamp = None
    counter = 0

    def __init__(self, filename: str, searcher: TaskSearcher):
        self.repository = TaskRepository(filename)
        self.searcher = searcher

    def generate_task_id(self) -> int:
        """Создание уникальных ID для задач, используя временные меток (в секундах) и счетчик.
        Для создания ID они конвертируются в число системы исчисления основой в 36."""
        current_timestamp = int(time.time() * 1000)

        if current_timestamp == TaskManager.last_timestamp:
            TaskManager.counter += 1
            if TaskManager.counter > 99: # Ограничиваем счетчик до числа двойной разрядности (0-99)
                TaskManager.counter = 0
            else:
                TaskManager.last_timestamp = current_timestamp
                TaskManager.counter = 0

        combined_input = f"{current_timestamp}-{TaskManager.counter}".encode('utf-8')

        hash_object = hashlib.sha256(combined_input)
        hex_dig = hash_object.hexdigest()

        task_id = int(hex_dig[:8], 16)

        return task_id

    def add_task(self, title: str, *args, **kwargs):
        """Добавление новой задачи. Принимает на вход название задачи и необязательные переменные."""
        task_id = self.generate_task_id()
        description = kwargs.get("description", None)
        category = kwargs.get("category", None)
        deadline_str = kwargs.get("deadline", None)
        priority = kwargs.get("priority", "низкий")

        deadline = datetime.strptime(deadline_str, "%Y-%m-%d") if deadline_str else None

        new_task = Task(task_id, title, description, category, deadline, priority)
        
        self.repository.add_task(new_task)
        print(f"Задача {title} добавлена c ID {task_id}.\n")

    def delete_task(self, task_id: int) -> bool:
        """Удаление задачи по ID."""
        return self.repository.delete_task(task_id)

    def view_tasks(self) -> list[Task]:
        """Просмотр всех задач."""
        return self.repository.view_tasks()

    def view_tasks_by_category(self, category: str) -> list[Task]:
        return self.repository.get_tasks_by_category(category)

    def change_status(self, task_id: int, status: bool):
        """Изменение статуса задачи на выполненную или не выполненную."""
        try:
            task = self.repository.get_task(task_id)
            
            if task.completed == status:
                print(f'Задача уже имеет статус "{"Выполнена" if status else "Не выполнена"}".')
                return
            
            task.completed = status
            self.repository.save_tasks()
            print(f'Статус задачи "{task.title}" обновлен: "{"Выполнена" if status else "Не выполнена"}"')
        
        except NoResultFound as e:
            print(e)

    def edit_task(self, task_id: int, **kwargs):
        """Редактирование существующей задачи."""
        task_to_edit = self.repository.get_task(task_id)

        for key, value in kwargs.items():
            if value is not None:
                setattr(task_to_edit, key, value)
        
        self.repository.save_tasks()
