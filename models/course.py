class Course:
    def __init__(self, number: int, name: str, max_number_of_students: int, course_type: str, hours_per_week: int):
        if not isinstance(number, int) or number <= 0:
            raise ValueError("Course number must be a positive integer.")
        if not name or not isinstance(name, str):
            raise ValueError("Course name must be a non-empty string.")
        if not isinstance(max_number_of_students, int) or max_number_of_students <= 0:
            raise ValueError("Max number of students must be a positive integer.")
        if course_type not in ["lecture", "lab"]:
            raise ValueError("Course type must be 'lection' or 'lab'.")
        if not isinstance(hours_per_week, int) or hours_per_week <= 0:
            raise ValueError("Hours per week must be a positive integer.")

        self._number = number
        self._name = name
        self._max_number_of_students = max_number_of_students
        self._course_type = course_type
        self._hours_per_week = hours_per_week

    @property
    def hours_per_week(self) -> int:
        return self._hours_per_week

    @property
    def number(self) -> int:
        return self._number

    @property
    def name(self) -> str:
        return self._name

    @property
    def max_number_of_students(self) -> int:
        return self._max_number_of_students

    @property
    def course_type(self) -> str:
        return self._course_type

    def __str__(self) -> str:
        return f"{self.name} ({self.course_type}, Max students: {self.max_number_of_students})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Course):
            return False
        return self.number == other.number and self.name == other.name

    def __hash__(self) -> int:
        return hash((self.number, self.name))
