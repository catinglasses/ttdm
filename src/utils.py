class NoResultFound(Exception):
    """Исключение, если задача не найдена."""
    def __init__(self, task_id: int):
        super().__init__(f"Задача с ID {task_id} не найдена.")
        self.task_id = task_id

class ValidationError(Exception):
    """Кастомный класс для обработки ошибок валидации."""
    def __init__(self, message):
        super().__init__(message)

class InputValidator:
    """Утилита для валидации данных на вход"""
    @staticmethod
    def validate_not_empty(input_value, field_name="Input"):
        """Проверка наличия данных на вход (input not empty). Вызывает ValidationError.
        Args:
            input_value: Значение на валидацию;
            field_name: Название валидируемого поля (для обработки ошибок).
        """
        if not input_value or (isinstance(input_value, str) and input_value.strip() == ""):
            raise ValidationError(f"{field_name} не может быть пустым.")
