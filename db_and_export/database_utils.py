import sqlite3
from models import Classroom, Teacher, Course, StudentGroup, TimeSlot
from timetable import Timetable
from data import Data


def import_data_from_db(database_path: str) -> Data:
    """
    Imports data from an external db_and_export and creates a Data object.

    :param database_path: Path to the SQLite db_and_export.
    :return: Data object with imported data.
    """
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    # Import classrooms
    classrooms = [
        Classroom(number=row[0], seating_capacity=row[1])
        for row in cursor.execute("SELECT number, seating_capacity FROM classrooms")
    ]

    # Import teachers with consideration of max_hours_per_week
    teachers = [
        Teacher(
            id=row[0],
            name=row[1],
            courses=[int(course) for course in row[2].split(',')],
            max_hours_per_week=row[3]
        )
        for row in cursor.execute("SELECT id, name, courses, max_hours_per_week FROM teachers")
    ]

    # Import courses
    courses = [
        Course(number=row[0], name=row[1], max_number_of_students=row[2], course_type=row[3], hours_per_week = row[4])
        for row in cursor.execute("SELECT number, name, max_students, course_type, hours_per_week FROM courses")
    ]

    # Import student groups
    groups = [
        StudentGroup(id=row[0], name=row[1], num_students=row[2],
                     courses=[courses[int(course_num) - 1] for course_num in row[3].split(',')])
        for row in cursor.execute("SELECT id, name, num_students, courses FROM student_groups")
    ]

    # Import available time slots
    time_slots = [
        TimeSlot(id=row[0], time=row[1], day=row[2])
        for row in cursor.execute("SELECT id, time, day FROM time_slots")
    ]

    connection.close()

    # Create a Data object with imported data
    data = Data()
    data.classrooms = classrooms
    data.teachers = teachers
    data.courses = courses
    data.groups = groups
    data.time_slots = time_slots
    data.number_of_classes = sum(len(group.courses) for group in data.groups)

    return data


def export_data_to_db(data: Data, database_path: str) -> None:
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    # Clear tables before populating
    cursor.execute("DELETE FROM classrooms")
    cursor.execute("DELETE FROM teachers")
    cursor.execute("DELETE FROM courses")
    cursor.execute("DELETE FROM student_groups")
    cursor.execute("DELETE FROM time_slots")

    # Export classrooms
    for classroom in data.classrooms:
        cursor.execute(
            "INSERT INTO classrooms (number, seating_capacity) VALUES (?, ?)",
            (classroom.number, classroom.seating_capacity)
        )

    # Export teachers with consideration of max_hours_per_week
    for teacher in data.teachers:
        courses_str = ",".join(str(course) for course in teacher.courses)
        cursor.execute(
            "INSERT INTO teachers (id, name, courses, max_hours_per_week) VALUES (?, ?, ?, ?)",
            (teacher.id, teacher.name, courses_str, teacher.max_hours_per_week)
        )

    # Export courses with hours_per_week
    for course in data.courses:
        cursor.execute(
            "INSERT INTO courses (number, name, max_students, course_type, hours_per_week) VALUES (?, ?, ?, ?, ?)",
            (course.number, course.name, course.max_number_of_students, course.course_type, course.hours_per_week)
        )

    # Export student groups
    for group in data.groups:
        courses_str = ",".join(str(course.number) for course in group.courses)
        cursor.execute(
            "INSERT INTO student_groups (id, name, num_students, courses) VALUES (?, ?, ?, ?)",
            (group.id, group.name, group.num_students, courses_str)
        )

    # Export available time slots
    for time_slot in data.time_slots:
        cursor.execute(
            "INSERT INTO time_slots (id, time, day) VALUES (?, ?, ?)",
            (time_slot.id, time_slot.time, time_slot.day)
        )

    connection.commit()
    connection.close()
    print(f"Data exported to {database_path}")


def export_timetable_to_txt(timetable: Timetable, file_path: str) -> None:
    """
    Exports the timetable to a text file in a readable format.

    :param timetable: Timetable object with the timetable.
    :param file_path: Path to the file where the timetable will be saved.
    """
    # Mapping for sorting days of the week
    day_order = {
        "Monday": 1,
        "Tuesday": 2,
        "Wednesday": 3,
        "Thursday": 4,
        "Friday": 5
    }

    # Sort classes by group, day of the week, and time
    sorted_classes = sorted(
        timetable.study_sessions,
        key=lambda c: (c.student_group.name, day_order.get(c.time_slot.day, 0), c.time_slot.time)
    )

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write("Timetable:\n")
        file.write("Class # | Group | Course | Classroom | Teacher | Day | Time\n")
        file.write("-" * 80 + "\n")

        # Variables to track the current group and day for readability
        current_group = None
        current_day = None

        for class_number, _class in enumerate(sorted_classes, 1):
            group_name = _class.student_group.name
            day = _class.time_slot.day

            # Add spacing between different groups for better readability
            if group_name != current_group:
                file.write("\n")  # New line before a new group
                current_group = group_name

            # Add additional spacing when the day of the week changes
            if day != current_day:
                file.write(f"\n{day}\n")  # Print day of the week only once for each day
                current_day = day

            # Write data about each class
            file.write(
                f"{class_number} | {_class.student_group.name} | {_class.course.name} "
                f"({_class.course.number}) | {_class.classroom.number} "
                f"({_class.classroom.seating_capacity}) | {_class.teacher.name} "
                f"({_class.teacher.id}) | {_class.time_slot.day} | {_class.time_slot.time}\n"
            )

        file.write("-" * 80 + "\n")
        file.write(f"Fitness: {timetable.fitness}\n")
        file.write(f"Number of conflicts: {timetable.conflicts_count}\n")

    print(f"Schedule exported to {file_path}")


def create_database_schema(database_path: str) -> None:
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS classrooms (
        number TEXT PRIMARY KEY,
        seating_capacity INTEGER
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY,
        name TEXT,
        courses TEXT, -- List of course numbers that can be taught, separated by commas
        max_hours_per_week INTEGER -- Maximum number of teaching hours per week
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS courses (
        number INTEGER PRIMARY KEY,
        name TEXT,
        max_students INTEGER,
        course_type TEXT, -- lecture or practical
        hours_per_week INTEGER -- Number of hours per week for each course
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS student_groups (
        id INTEGER PRIMARY KEY,
        name TEXT,
        num_students INTEGER,
        courses TEXT -- List of course numbers for the group, separated by commas
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS time_slots (
        id TEXT PRIMARY KEY,
        time TEXT,
        day TEXT
    )
    ''')

    connection.commit()
    connection.close()
    print(f"Database schema created at {database_path}")

