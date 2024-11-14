import sqlite3

def print_table_data(database_path: str, table_name: str) -> None:
    """
    Prints the contents of the specified table from the SQLite db_and_export.

    :param database_path: Path to the SQLite db_and_export.
    :param table_name: Name of the table to print.
    """
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    print(f"\nContents of the '{table_name}' table:")
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    if rows:
        # Get column names
        columns = [description[0] for description in cursor.description]
        print(" | ".join(columns))
        print("-" * 50)
        for row in rows:
            print(" | ".join(str(value) for value in row))
    else:
        print("The table is empty.")

    connection.close()

def check_database_contents(database_path: str) -> None:
    """
    Checks the contents of all tables in the db_and_export.

    :param database_path: Path to the SQLite db_and_export.
    """
    tables = ['classrooms', 'teachers', 'courses', 'student_groups', 'time_slots']
    for table in tables:
        print_table_data(database_path, table)

# Path to the db_and_export
DATABASE_PATH = 'timetable_database.db'

# Check db_and_export contents
check_database_contents(DATABASE_PATH)
