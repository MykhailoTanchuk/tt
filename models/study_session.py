#study_session.py

from models.course import Course
from models.student_group import StudentGroup

class StudySession:
    def __init__(self, id: int, course: Course, student_group: StudentGroup):
        self.id = id
        self.course = course
        self.student_group = student_group
        self.classroom = None
        self.teacher = None
        self.time_slot = None

    def __str__(self) -> str:
        return (f"[{self.course.name}, Group: {self.student_group.name}, "
                f"Classroom: {self.classroom}, Teacher: {self.teacher}, "
                f"Time Slot: {self.time_slot}]")
