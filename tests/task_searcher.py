import pytest

from src.model import Task
from src.services import TaskSearcher

@pytest.fixture
def sample_tasks():
    return [
        Task(task_id=1, title="Task One", description="First task description", category="Category A", deadline=None, completed=False),
        Task(task_id=2, title="Task Two", description="Second task description", category="Category B", deadline=None, completed=True),
        Task(task_id=3, title="Another Entry", description="Third entry description", category="Category A", deadline=None, completed=False),
        Task(task_id=4, title="task one more", description="Fourth task description", category="Category C", deadline=None, completed=True),
    ]

def test_search_by_keyword_in_title(sample_tasks):
    results = TaskSearcher.search(sample_tasks, keyword="task", category=None, completed=None)
    
    assert len(results) == 3
    assert results[0].title == "Task One"
    assert results[1].title == "Task Two"
    assert results[2].title == "task one more"

def test_search_by_keyword_in_description(sample_tasks):
    results = TaskSearcher.search(sample_tasks, keyword="third", category=None, completed=None)
    
    assert len(results) == 1
    assert results[0].title == "Another Entry"

def test_search_by_category(sample_tasks):
    results = TaskSearcher.search(sample_tasks, keyword=None, category="Category A", completed=None)
    
    assert len(results) == 2
    assert results[0].title == "Task One"
    assert results[1].title == "Another Entry"

def test_search_by_completed_status(sample_tasks):
    results = TaskSearcher.search(sample_tasks, keyword=None, category=None, completed=True)
    
    assert len(results) == 2
    assert all(task.completed for task in results)

def test_combined_search(sample_tasks):
    results = TaskSearcher.search(sample_tasks, keyword="task", category="Category A", completed=None)
    
    assert len(results) == 1
    assert results[0].title == "Task One"

def test_no_results(sample_tasks):
    results = TaskSearcher.search(sample_tasks, keyword="Nonexistent", category=None, completed=None)
    
    assert len(results) == 0

def test_search_with_none_values(sample_tasks):
    results = TaskSearcher.search(sample_tasks, keyword=None, category=None, completed=None)
    
    assert len(results) == len(sample_tasks)
