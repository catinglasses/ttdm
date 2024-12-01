import pytest

from src.model import Task
from src.services import TaskManager
from src.utils import ValidationError

@pytest.fixture
def task_manager(tmp_path):
    """Создаем фикстуру с объектом TaskManager для тестирования"""
    test_file = tmp_path / "test_tasks.json"
    manager = TaskManager(str(test_file), None) # None, т.к. мы не используем TaskSearcher => нет нужды его передавать
    return manager

def test_add_task(task_manager):
    task_title = "Test Task"
    task_description = "This is a test task"
    task_category = "Testing"
    task_deadline = None
    task_priority = "низкий"

    task_manager.add_task(task_title, description=task_description, category=task_category, deadline=task_deadline, priority=task_priority)

    assert len(task_manager.repository.tasks) == 1

def test_view_tasks(task_manager):
    task_manager.add_task("task1", "description1", "category a")
    task_manager.add_task("task2", "description2", "category b")

    tasks = task_manager.repository.tasks

    assert len(tasks) == 2
    assert tasks[0].title == 'task1'
    assert tasks[1].title == 'task2'

def test_view_tasks_by_category(task_manager):
    task_manager.add_task("task A", category="category X")
    task_manager.add_task("task B", category="category Y")
    task_manager.add_task("task C", category="category X")

    tasks_x = task_manager.view_tasks_by_category("category X")

    assert len(tasks_x) == 2
    assert tasks_x[0].title == "task A"
    assert tasks_x[1].title == "task C"

def test_change_status(task_manager):
    task_manager.add_task("task A[old]", "empty", "NaN")

    assert task_manager.repository.tasks[0].completed is False

    task_manager.change_status(task_manager.repository.tasks[0].task_id, True)

    assert task_manager.repository.tasks[0].completed is True

def test_delete_task(task_manager):
    task_manager.add_task("to_delete", "will be deleted", "delete category")

    assert len(task_manager.repository.tasks) == 1

    deleted_task_id = task_manager.repository.tasks[0].task_id
    task_manager.delete_task(deleted_task_id)

    assert len(task_manager.repository.tasks) == 0
