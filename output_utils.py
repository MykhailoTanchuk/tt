import json
from random import random
from typing import Any
from tabulate import tabulate


def get_random_number() -> float:
    """Returns a random number in the range [0, 1)."""
    return random()


def print_msg(msg: Any) -> None:
    """Prints a message with separators for improved readability."""
    if isinstance(msg, dict):
        msg = json.dumps(msg, indent=2)

    print("\n" + "*" * 50)
    print(msg)
    print("*" * 50)


def print_data(data: Any) -> None:
    """Prints input data in a readable format."""
    print_msg("Information about input data")

    # Display courses
    print_msg("Available Courses")
    for course in data.courses:
        print(f"Course Number: {course.number}, Name: {course.name}, "
              f"Max Students: {course.max_number_of_students}, Type: {course.course_type}")

    # Display classrooms
    print_msg("Available Classrooms")
    for classroom in data.classrooms:
        print(f"Classroom Number: {classroom.number}, Max Capacity: {classroom.seating_capacity}")

    # Display teachers
    print_msg("Available Teachers")
    for teacher in data.teachers:
        course_list = ", ".join(str(course) for course in teacher.courses)
        print(f"ID: {teacher.id}, Name: {teacher.name}, Courses: [{course_list}]")

    # Display available time slots
    print_msg("Available Time Slots")
    for time_slot in data.time_slots:
        print(f"ID: {time_slot.id}, Meeting Time: {time_slot.time}")


def print_population_timetables(population: Any, generation_number: int) -> None:
    """Prints all timetables in the population with generation information."""
    print_msg(f"Generation Number: {generation_number}")

    # Create a table of timetables with characteristics of each timetable
    timetables = [
        [idx, str(timetable), timetable.fitness, timetable.conflicts_count]
        for idx, timetable in enumerate(population.timetables)
    ]

    headers = [
        "Timetables Number",
        "Study Sessions [course, group, classroom, teacher, time slot]",
        "Fitness",
        "Conflicts"
    ]

    print(tabulate(timetables, headers=headers))


def print_timetable_as_table(data: Any, timetable: Any, generation: int) -> None:
    """Prints the timetable as a table, sorted by group, day of the week, and time."""

    # Mapping for sorting days of the week
    day_order = {
        "Monday": 1,
        "Tuesday": 2,
        "Wednesday": 3,
        "Thursday": 4,
        "Friday": 5
    }

    # Sort study_sessions by group, day of the week, and time
    sorted_study_sessions = sorted(
        timetable.study_sessions,
        key=lambda c: (c.student_group.name, day_order.get(c.time_slot.day, 0), c.time_slot.time)
    )

    headers = [
        "St. Session Number", "Group", "Course (number)", "Classroom (capacity)",
        "Teacher (ID)", "Day", "Time"
    ]

    table_data = []
    # Prepare data for the table
    for study_session_number, _study_session in enumerate(sorted_study_sessions, 1):
        table_data.append([
            study_session_number,
            _study_session.student_group.name,
            f"{_study_session.course.name} ({_study_session.course.number})",
            f"{_study_session.classroom.number} ({_study_session.classroom.seating_capacity})",
            f"{_study_session.teacher.name} ({_study_session.teacher.id})",
            _study_session.time_slot.day,
            _study_session.time_slot.time
        ])

    # Print the schedule table
    print(tabulate(table_data, headers=headers))

    # Message about finding an optimal solution
    if timetable.fitness == 1.0:
        print_msg(f"Solution found in generation {generation + 1}")
