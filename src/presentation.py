from datetime import datetime

from .services import TaskSearcher, TaskManager
from .utils import NoResultFound, InputValidator, ValidationError

class TaskCLI:
    """Класс для взаимодействия пользователя и программы через командную строку. Слой представления (Presentation layer)."""
    def __init__(self):
        filename = "tasks.json"
        searcher = TaskSearcher()
        
        self.manager = TaskManager(filename, searcher)

    def get_non_empty_input(self, prompt: str, field_name: str):
        """Метод для обеспечения ввода данных поля {field_name} пользователем."""
        while True:
            try:
                value = input(prompt)
                InputValidator.validate_not_empty(value, field_name)
                return value
            except ValidationError as e:
                print(f"Ошибка: {e} Пожалуйста, попробуйте снова.")

    def view_tasks_by_category(self):
        """Просмотр задач по категории"""
        category = self.get_non_empty_input("Введите категорию для просмотра задач:  ", "Категория")
        tasks = self.manager.view_tasks_by_category(category)

        if not tasks:
            print(f"Нет задач в категории {category}.")
            return
        
        print(f"\nЗадачи в категории {category}:")
        for task in tasks:
            data = f"ID: {task.task_id} | Название: {task.title} | Статус: {"Выполнена" if task.completed else "Не выполнена"}\n"\
                    f"Приоритет: {task.priority} | Срок сдачи: {task.deadline.isoformat() if task.deadline else "Нет срока"}\n"\
                    f"Описание: {task.description if task.description else "Нет описания"}\n"
            print(data)

    def run(self):
        while True:
            print("\nМеню:")
            print("1. Просмотреть все задачи")
            print("2. Добавить задачу")
            print("3. Изменить задачу")
            print("4. Изменить статус задачи")
            print("5. Удалить задачу")
            print("6. Поиск задач")
            print("7. Просмотр задач по категории")
            print("\n0. Выход")

            choice = input("\nВыберите действие (0-7):    ")

            if choice == "1":
                print("\nСписок задач:")
                tasks = self.manager.view_tasks()
                for task in tasks:
                    status = "Выполнена" if task.completed else "Не выполнена"
                    deadline_str = task.deadline.isoformat() if task.deadline else "Нет срока"
                    data = f"ID: {task.task_id} | Название: {task.title} | Категория: {task.category if task.category else "Не указанаё"}\n"\
                            f"Статус: {status} | Приоритет: {task.priority} | Срок сдачи: {deadline_str}\n" 
                    print(data)

            elif choice == "2":
                title = self.get_non_empty_input("Введите заголовок задачи:  ", "Название")
                description = input("Введите описание задачи (или оставьте пустым):  ") or None
                category = input("Введите категорию задачи (или оставьте пустым):  ") or None
                deadline_str = input("Введите срок выполнения задачи (YYYY-MM-DD или оставьте пустым):  ") or None
                priority = input("Введите приоритет задачи (низкий/средний/высокий):  ") or "низкий"

                self.manager.add_task(title, description=description, category=category, deadline=deadline_str, priority=priority)

            elif choice == "3":
                try:
                    task_id = int(self.get_non_empty_input("Введите ID задачи для изменения:  ", "ID"))
                    title = input("Введите новый заголовок (или оставьте пустым для пропуска):  ")
                    description = input("Введите новое описание (или оставьте пустым для пропуска):  ") or None
                    category = input("Введите новую категорию (или оставьте пустым для пропуска):  ") or None
                    deadline_str = input("Введите новый срок выполнения (YYYY-MM-DD или оставьте пустым для пропуска):  ") or None
                    priority_input = input("Введите новый приоритет (низкий/средний/высокий или оставьте пустым для пропуска):  ") or None

                    updates_cleaned_filtered = {
                        "title": title,
                        "description": description,
                        "category": category,
                        "deadline": datetime.strptime(deadline_str, "%Y-%m-%d") if deadline_str else None,
                        "priority": priority_input
                    }

                    updates_cleaned_filtered = {k: v for k, v in updates_cleaned_filtered.items() if v is not None}

                    self.manager.edit_task(task_id=task_id, **updates_cleaned_filtered)
                except NoResultFound as e:
                    print(e)

            elif choice == "4":
                try:
                    task_id = int(self.get_non_empty_input("Введите ID задачи для изменения ее статуса:  ", "ID"))
                    new_status = bool(input("Введите любой символ, чтобы отметить задачу выполненной (или оставьте пустым для пропуска):  "))
                    self.manager.change_status(task_id, new_status)
                except NoResultFound as e:
                    print(e)

            elif choice == "5":
                try:
                    task_id = int(self.get_non_empty_input("Введите ID задачи для удаления: ", "ID"))
                    success = self.manager.delete_task(task_id)
                    if success:
                        print(f"Задача с ID {task_id} была успешно удалена.")
                    else:
                        print(f"Задача с ID {task_id} не найдена.")
                except NoResultFound as e:
                    print(e)

            elif choice == "6":
                keyword = input("Введите ключевое слово для поиска (или оставьте пустым): ") or None
                category_search = input("Введите категорию для поиска (или оставьте пустым): ") or None
                completed_search_str = input("Искать выполненные задачи? (да/нет): ").strip().lower()
                completed_search = True if completed_search_str == 'да' else False if completed_search_str == 'нет' else None
                
                results = self.manager.searcher.search(self.manager.view_tasks(), keyword=keyword,
                                                        category=category_search, completed=completed_search)
                
                print("\nРезультаты поиска:")
                for result in results:
                    status_text = "Выполнена" if result.completed else "Не выполнена"
                    data = f"ID: {result.task_id} | Название: {result.title} | Категория: {result.category if result.category else "Не указана"}\n"\
                        f"Статус: {status_text} | Приоритет: {result.priority} | Срок сдачи: {result.deadline.isoformat() if result.deadline else "Нет срока"}\n"\
                            f"Описание: {result.description if result.description else "Нет описания"}\n"

                    
                    print(data)

            elif choice == "7":
                self.view_tasks_by_category()
            
            elif choice == "0":
                print("Завершение программы...")
                break

            else:
                print("Действие не найдено. Укажите действие (0-7):  ")
                self.run()
