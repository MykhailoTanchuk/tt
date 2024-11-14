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

    def __str__(self) -> str:
        return f"Instructor: {self.name} (ID: {self.id}, Max hours: {self._max_hours_per_week})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Teacher):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)
