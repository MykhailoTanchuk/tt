#data.py

from typing import List
from models import StudySession, Course, Teacher, TimeSlot, Classroom, StudentGroup
from user_data.extract_data import load_classrooms_from_csv,load_groups_from_csv,load_courses_from_csv,load_teachers_from_csv,load_time_slots_from_csv

class Data:
    def __init__(self, fitness_function: str = "conflicts"):
        self.fitness_function = fitness_function
        self.classrooms: List[Classroom] = []
        self.teachers: List[Teacher] = []
        self.courses: List[Course] = []
        self.groups: List[StudentGroup] = []
        self.time_slots: List[TimeSlot] = []
        self.number_of_classes: int = 0

        self.initialize()

    def initialize(self):
        self.classrooms = load_classrooms_from_csv('user_data/classrooms.csv')
        self.teachers = load_teachers_from_csv('user_data/teachers.csv')
        self.courses = load_courses_from_csv('user_data/courses.csv')
        self.groups = load_groups_from_csv('user_data/groups.csv', self.courses)
        self.time_slots = load_time_slots_from_csv('user_data/time_slots.csv')
        self.number_of_classes = sum(len(group.courses) for group in self.groups)

    def create_classrooms(self) -> List[Classroom]:
        return [
            Classroom(number="301", seating_capacity=30),
            Classroom(number="302", seating_capacity=40),
            Classroom(number="303", seating_capacity=35),
            Classroom(number="304", seating_capacity=50),
            Classroom(number="201", seating_capacity=120),
            Classroom(number="202", seating_capacity=100),
            Classroom(number="203", seating_capacity=120),
            Classroom(number="204", seating_capacity=50),
            Classroom(number="401", seating_capacity=30),
            Classroom(number="402", seating_capacity=40),
            Classroom(number="403", seating_capacity=35),
            Classroom(number="404", seating_capacity=50)
        ]

    def create_time_slots(self) -> List[TimeSlot]:
        times = ["08:40 - 10:15", "10:35 - 12:10", "12:20 - 13:55"]
        days = ["Monday", "Tuesday", "Wednesday", "Thursday"]

        time_slots = []
        slot_id = 1
        for day in days:
            for time in times:
                time_slots.append(TimeSlot(id=f"MT{slot_id}", time=time, day=day))
                slot_id += 1

        return time_slots

    def create_teachers(self) -> List[Teacher]:
        return [
            Teacher(id=1, name="Мащенко", courses=[1], max_hours_per_week=16),
            Teacher(id=2, name="Пашко", courses=[3, 14], max_hours_per_week=20),
            Teacher(id=3, name="Тарануха", courses=[4, 10, 11], max_hours_per_week=30),
            Teacher(id=4, name="Ткаченко", courses=[6, 18], max_hours_per_week=20),
            Teacher(id=5, name="Красовська", courses=[8], max_hours_per_week=12),
            Teacher(id=6, name="Вергунова", courses=[9], max_hours_per_week=16),
            Teacher(id=7, name="Шишацька", courses=[15], max_hours_per_week=16),
            Teacher(id=8, name="Криволап", courses=[7, 19], max_hours_per_week=20),
            Teacher(id=9, name="Зинтар", courses=[2], max_hours_per_week=12),
            Teacher(id=10, name="Свистунов", courses=[7], max_hours_per_week=12),
            Teacher(id=11, name="Крак", courses=[16, 21, 22], max_hours_per_week=28),
            Teacher(id=12, name="Чернега", courses=[5], max_hours_per_week=12),
            Teacher(id=13, name="Злотник", courses=[5], max_hours_per_week=12),
            Teacher(id=14, name="Коваль", courses=[17], max_hours_per_week=16),
            Teacher(id=15, name="Бобиль", courses=[12, 13], max_hours_per_week=20),
            Teacher(id=16, name="Дорошенко", courses=[20], max_hours_per_week=16),
            Teacher(id=17, name="Галавай", courses=[19], max_hours_per_week=12),
            Teacher(id=18, name="Мисечко", courses=[25, 5], max_hours_per_week=20),
            Teacher(id=19, name="Башук", courses=[25], max_hours_per_week=16),
            Teacher(id=20, name="Коробова", courses=[2], max_hours_per_week=12),
            Teacher(id=21, name="Башняков", courses=[2], max_hours_per_week=12),
            Teacher(id=22, name="Терещенко", courses=[7], max_hours_per_week=16),
            Teacher(id=23, name="Федорус", courses=[5], max_hours_per_week=12)
        ]

    def create_courses(self) -> List[Course]:
        return [
            Course(number=1, name="ТПР", max_number_of_students=100, course_type="лекция"),
            Course(number=2, name="ТПР", max_number_of_students=30, course_type="практика"),

            Course(number=3, name="СтатМод", max_number_of_students=100, course_type="лекция"),

            Course(number=4, name="ІнтСис", max_number_of_students=100, course_type="лекция"),
            Course(number=5, name="ІнтСис", max_number_of_students=30, course_type="практика"),

            Course(number=6, name="ІТ", max_number_of_students=100, course_type="лекция"),
            Course(number=7, name="ІТ", max_number_of_students=30, course_type="практика"),

            Course(number=8, name="Англ", max_number_of_students=100, course_type="лекция"),

            Course(number=9, name="СклАлг", max_number_of_students=100, course_type="лекция"),

            Course(number=10, name="Лінгв", max_number_of_students=50, course_type="лекция"),
            Course(number=11, name="Лінгв", max_number_of_students=30, course_type="практика"),

            Course(number=12, name="НейрМер", max_number_of_students=50, course_type="лекция"),
            Course(number=13, name="НейрМер", max_number_of_students=30, course_type="практика"),


            Course(number=14, name="ІнтОбрДаних", max_number_of_students=30, course_type="лекция"),

            Course(number=15, name="УпрІТПроект", max_number_of_students=50, course_type="лекция"),

            Course(number=16, name="РозробкаПЗ", max_number_of_students=100, course_type="лекция"),
            Course(number=17, name="РозробкаПЗ", max_number_of_students=30, course_type="практика"),

            Course(number=18, name="МобПЗ", max_number_of_students=50, course_type="лекция"),
            Course(number=19, name="МобПЗ", max_number_of_students=30, course_type="практика"),

            Course(number=20, name="ПаралелОбч", max_number_of_students=50, course_type="лекция"),

            Course(number=21, name="ПроблемиШІ", max_number_of_students=50, course_type="лекция"),
            Course(number=22, name="ПроблемиШІ", max_number_of_students=30, course_type="практика"),

            Course(number=23, name="ПаралелОбч", max_number_of_students=50, course_type="лекция"),

            Course(number=24, name="ІнфСист", max_number_of_students=50, course_type="лекция"),
            Course(number=25, name="ІнфСист", max_number_of_students=30, course_type="практика"),
        ]

    def create_groups(self) -> List[StudentGroup]:
        return [
            StudentGroup(id=1, name="МІ-41-1", num_students=9,
                         courses=[self.courses[0], self.courses[1], self.courses[2], self.courses[3], self.courses[4],
                                  self.courses[5], self.courses[6], self.courses[7], self.courses[8], self.courses[9],
                                  self.courses[10], self.courses[11], self.courses[12]]),
            StudentGroup(id=2, name="МІ-41-2", num_students=9,
                         courses=[self.courses[0], self.courses[1], self.courses[2], self.courses[3], self.courses[4],
                                  self.courses[5], self.courses[6], self.courses[7], self.courses[8], self.courses[9],
                                  self.courses[10], self.courses[11], self.courses[12]]),


            StudentGroup(id=3, name="МІ-42-1", num_students=9,
                         courses=[self.courses[0], self.courses[1], self.courses[2], self.courses[3], self.courses[4],
                                  self.courses[5], self.courses[6], self.courses[7], self.courses[8], self.courses[9],
                                  self.courses[10], self.courses[11], self.courses[12]]),
            StudentGroup(id=4, name="МІ-42-2", num_students=9,
                         courses=[self.courses[0], self.courses[1], self.courses[2], self.courses[3], self.courses[4],
                                  self.courses[5], self.courses[6], self.courses[7], self.courses[8], self.courses[9],
                                  self.courses[10], self.courses[11], self.courses[12]]),


            StudentGroup(id=5, name="ТТП-41-1", num_students=10,
                         courses=[self.courses[0], self.courses[2], self.courses[3], self.courses[5], self.courses[7],
                                  self.courses[14], self.courses[17], self.courses[6], self.courses[1],
                                  self.courses[24], self.courses[19], self.courses[18]]),
            StudentGroup(id=6, name="ТТП-41-2", num_students=10,
                         courses=[self.courses[0], self.courses[2], self.courses[3], self.courses[5], self.courses[7],
                                  self.courses[14], self.courses[17], self.courses[6], self.courses[1],
                                  self.courses[24], self.courses[19], self.courses[18]]),


            StudentGroup(id=7, name="ТТП-42-1", num_students=10,
                         courses=[self.courses[0], self.courses[2], self.courses[3], self.courses[5], self.courses[7],
                                  self.courses[14], self.courses[17], self.courses[6], self.courses[1],
                                  self.courses[24], self.courses[19], self.courses[18]]),
            StudentGroup(id=8, name="ТТП-42-2", num_students=10,
                         courses=[self.courses[0], self.courses[2], self.courses[3], self.courses[5], self.courses[7],
                                  self.courses[14], self.courses[17], self.courses[6], self.courses[1],
                                  self.courses[24], self.courses[19], self.courses[18]]),


            StudentGroup(id=9, name="ТК-41-1", num_students=10,
                         courses=[self.courses[0], self.courses[2], self.courses[5], self.courses[7], self.courses[13],
                                  self.courses[15], self.courses[6], self.courses[5], self.courses[16],
                                  self.courses[20], self.courses[21], self.courses[1], self.courses[3]]),
            StudentGroup(id=10, name="ТК-41-2", num_students=9,
                         courses=[self.courses[0], self.courses[2], self.courses[5], self.courses[7], self.courses[13],
                                  self.courses[15], self.courses[6], self.courses[5], self.courses[16],
                                  self.courses[20], self.courses[21], self.courses[1], self.courses[3]])
        ]

    def get_study_sessions(self) -> List[StudySession]:
        study_sessions = []
        for course in self.courses:
            for group in self.groups:
                if course in group.courses:
                    study_sessions.append(StudySession(id=len(study_sessions), course=course, student_group=group))
        return study_sessions
