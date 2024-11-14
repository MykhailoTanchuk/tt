import csv
from models import Classroom, Teacher, Course, StudentGroup, TimeSlot
from typing import List


def load_classrooms_from_csv(file_path: str) -> List[Classroom]:
    classrooms = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            classrooms.append(Classroom(number=row['number'], seating_capacity=int(row['seating_capacity'])))
    return classrooms


def load_teachers_from_csv(file_path: str) -> List[Teacher]:
    teachers = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            course_ids = list(map(int, row['courses'].split(',')))
            teachers.append(Teacher(
                id=int(row['id']),
                name=row['name'],
                courses=course_ids,
                max_hours_per_week=int(row['max_hours_per_week'])
            ))
    return teachers


def load_courses_from_csv(file_path: str) -> List[Course]:
    courses = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            courses.append(Course(
                number=int(row['number']),
                name=row['name'],
                max_number_of_students=int(row['max_number_of_students']),
                course_type=row['course_type']
            ))
    return courses


def load_groups_from_csv(file_path: str, courses: List[Course]) -> List[StudentGroup]:
    groups = []
    course_dict = {course.number: course for course in courses}
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            course_ids = list(map(int, row['courses'].split(',')))
            group_courses = [course_dict[course_id] for course_id in course_ids]
            groups.append(StudentGroup(
                id=int(row['id']),
                name=row['name'],
                num_students=int(row['num_students']),
                courses=group_courses
            ))
    return groups


def load_time_slots_from_csv(file_path: str) -> List[TimeSlot]:
    time_slots = []
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            time_slots.append(TimeSlot(
                id=row['id'],
                time=row['time'],
                day=row['day']
            ))
    return time_slots