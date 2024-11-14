from models.course import Course
from typing import List


class StudentGroup:
    def __init__(self, id: int, name: str, num_students: int, courses: List[Course]):
        if not isinstance(id, int) or id <= 0:
            raise ValueError("Group ID must be a positive integer.")
        if not name or not isinstance(name, str):
            raise ValueError("Group name must be a non-empty string.")
        if not isinstance(num_students, int) or num_students <= 0:
            raise ValueError("Number of students must be a positive integer.")
        if not isinstance(courses, list) or not all(isinstance(course, Course) for course in courses):
            raise ValueError("Courses must be a list of Course objects.")

        self.id = id
        self.name = name
        self.num_students = num_students
        self.courses = courses

    def __str__(self):
        return f"Group {self.name} (Students: {self.num_students})"
