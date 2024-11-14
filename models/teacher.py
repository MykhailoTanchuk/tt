from typing import List


class Teacher:
    def __init__(self, id: int, name: str, courses: List[int], max_hours_per_week: int):
        if not isinstance(id, int) or id <= 0:
            raise ValueError("ID викладача має бути додатним цілим числом.")
        if not name or not isinstance(name, str):
            raise ValueError("Ім'я викладача має бути непорожнім рядком.")
        if not isinstance(courses, list) or not all(isinstance(c, int) for c in courses):
            raise ValueError("Курси мають бути списком номерів курсів.")
        if not isinstance(max_hours_per_week, int) or max_hours_per_week <= 0:
            raise ValueError("Максимальна кількість годин на тиждень має бути додатним числом.")

        self._id = id
        self._name = name
        self._courses = courses
        self._max_hours_per_week = max_hours_per_week
        self._current_hours = 0  # Поточна кількість годин, яку викладач вже набрав

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def courses(self) -> List[int]:
        return self._courses

    @property
    def max_hours_per_week(self) -> int:
        return self._max_hours_per_week

    @property
    def current_hours(self) -> int:
        return self._current_hours

    def can_teach(self, course_number: int, additional_hours: int = 0) -> bool:
        """
        Перевіряє, чи може викладач вести даний курс за його номером і поточним навантаженням.

        :param course_number: Номер курсу.
        :param additional_hours: Додаткова кількість годин, яку потрібно додати.
        :return: True, якщо викладач може вести курс з урахуванням додаткових годин.
        """
        return (course_number in self._courses and
                self._current_hours + additional_hours <= self._max_hours_per_week)

    def add_hours(self, hours: int) -> None:
        """
        Додає години до поточного навантаження викладача.

        :param hours: Кількість годин для додавання.
        """
        self._current_hours += hours

    def reset_hours(self) -> None:
        """Скидає поточне навантаження по годинах до нуля (наприклад, на початку нового навчального циклу)."""
        self._current_hours = 0

    def __str__(self) -> str:
        return f"Instructor: {self.name} (ID: {self.id}, Max hours: {self._max_hours_per_week}, Current hours: {self._current_hours})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Teacher):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
