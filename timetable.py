#timetable.py

from typing import List, Any
from output_utils import get_random_number
from models import StudySession, StudentGroup, Course, TimeSlot
from data import Data


class Timetable:
    def __init__(self, data: Any = None, fitness_function: str = "combined"):
        if data is None:
            data = Data(fitness_function=fitness_function)
        self.data = data
        self.fitness_function = fitness_function
        self._study_sessions: List[StudySession] = []
        self.study_session_number = 0
        self._fitness = -1.0
        self.conflicts_count = 0
        self.is_fitness_changed = True

    def __str__(self) -> str:
        return "\n".join(str(c) for c in self._study_sessions)

    @property
    def fitness(self) -> float:
        if self.is_fitness_changed:
            self._fitness = self.calculate_fitness()
            self.is_fitness_changed = False
        return self._fitness

    @property
    def study_sessions(self) -> List[StudySession]:
        self.is_fitness_changed = True
        return self._study_sessions

    def initialize(self) -> 'Timetable':
        for group in self.data.groups:
            for course in group.courses:
                required_sessions = self.get_required_sessions(course)
                for _ in range(required_sessions):
                    self._create_study_session(course, group)
        return self

    def get_required_sessions(self, course: Course) -> int:
        if course.course_type == "lection":
            return 2
        elif course.course_type == "lab":
            return 1
        else:
            return 1

    def _create_study_session(self, course: Course, group: StudentGroup) -> None:
        # Створює та додає новий клас (заняття) до розкладу для вказаного курсу та групи студентів.

        # 1. Визначення списку викладачів, які можуть викладати цей курс.
        # Пошук викладачів, які мають кваліфікацію для викладання зазначеного курсу.
        suitable_teachers = [
            teacher for teacher in self.data.teachers
            if teacher.can_teach(course.number)
        ]

        # 2. Перевірка наявності відповідних викладачів.
        # Якщо немає викладачів, які можуть вести курс, виводимо повідомлення і завершуємо функцію.
        if not suitable_teachers:
            print(
                f"Немає підходящих викладачів, які можуть вести курс '{course.name}' ({course.number}) у групі '{group.name}'")
            return

        # 3. Призначення випадкових значень для часу проведення, викладача та аудиторії.
        # Це робиться без перевірки на конфлікти з іншими заняттями.
        time_slot = self._get_random_item(self.data.time_slots)
        teacher = self._get_random_item(suitable_teachers)
        classroom = self._get_random_item(self.data.classrooms)

        # 4. Створення нового об'єкта класу (заняття) і заповнення його даними.
        # Встановлення індексу класу, групи студентів, часу, аудиторії та викладача.
        new_study_session = StudySession(id=self.study_session_number, course=course, student_group=group)
        self.study_session_number += 1
        new_study_session.time_slot = time_slot
        new_study_session.classroom = classroom
        new_study_session.teacher = teacher

        # 5. Додавання нового заняття до загального розкладу (списку занять).
        # Цей клас зберігається у списку _classes, який представляє повний розклад.
        self._study_sessions.append(new_study_session)

    def _calculate_conflicts(self) -> int:
        # Підраховує кількість конфліктів у розкладі, перевіряючи:
        # конфлікти за групами, викладачами, аудиторіями та місткістю аудиторій.

        number_of_conflicts = 0  # Ініціалізація лічильника конфліктів.

        group_timetable = {}  # Словник для відстеження конфліктів за групами.
        teacher_timetable = {}  # Словник для відстеження конфліктів за викладачами.
        classroom_timetable = {}  # Словник для відстеження конфліктів за аудиторіями.

        # Проходимо по кожному заняттю і перевіряємо конфлікти.
        for _study_session in self._study_sessions:
            group_key = (_study_session.student_group.name, _study_session.time_slot.id)  # Унікальний ключ для групи.
            teacher_key = (_study_session.teacher.id, _study_session.time_slot.id)  # Унікальний ключ для викладача.
            classroom_key = (_study_session.classroom.number, _study_session.time_slot.id)  # Унікальний ключ для аудиторії.

            # Перевірка конфліктів для групи: якщо група має заняття у той самий час.
            if group_key in group_timetable:
                number_of_conflicts += 1
            else:
                group_timetable[group_key] = True

            # Перевірка конфліктів для викладача: якщо викладач зайнятий у той самий час.
            if teacher_key in teacher_timetable:
                number_of_conflicts += 1
            else:
                teacher_timetable[teacher_key] = True

            # Перевірка конфліктів для аудиторії: якщо аудиторія зайнята у той самий час.
            if classroom_key in classroom_timetable:
                number_of_conflicts += 1
            else:
                classroom_timetable[classroom_key] = True

            # Перевірка місткості аудиторії: якщо кількість студентів більше місткості аудиторії.
            if _study_session.classroom and _study_session.student_group.num_students > _study_session.classroom.seating_capacity:
                number_of_conflicts += 1

        return number_of_conflicts  # Повертаємо загальну кількість конфліктів.

    def _get_random_item(self, items: List[Any]) -> Any:
        # Вибирає випадковий елемент зі списку переданих об'єктів.
        return items[int(get_random_number() * len(items))]

    def _calculate_gaps_penalty(self) -> int:
        # Обчислює штрафи за наявність «вікон» у розкладі для викладачів та груп.

        gaps_penalty = 0  # Ініціалізація штрафу за вікна

        def time_to_minutes(time_str: str) -> int:
            # Допоміжна функція для перетворення часу у хвилини.
            # Перетворює початковий час заняття у хвилини від початку доби для зручності обчислень.
            start_time = time_str.split(' - ')[0]
            hours, minutes = map(int, start_time.split(':'))
            return hours * 60 + minutes

        # 1. Ініціалізація словників для зберігання розкладів викладачів та студентських груп.
        teacher_daily_timetable = {}
        group_daily_timetable = {}

        # 2. Обробка кожного заняття у розкладі.
        # Для кожного заняття визначаємо час у хвилинах та день тижня,
        # і додаємо цю інформацію до відповідних словників для викладачів і груп.
        for _class in self._study_sessions:
            time_in_minutes = time_to_minutes(_class.time_slot.time)
            day = _class.time_slot.day

            # Додавання часу заняття до розкладу викладача
            teacher = _class.teacher.id
            teacher_daily_timetable.setdefault(teacher, {}).setdefault(day, []).append(time_in_minutes)

            # Додавання часу заняття до розкладу групи
            group = _class.student_group.name
            group_daily_timetable.setdefault(group, {}).setdefault(day, []).append(time_in_minutes)

        # 3. Підрахунок штрафів за «вікна» у розкладі викладачів.
        # Сортуємо заняття по часу і перевіряємо наявність проміжків більше 95 хвилин між заняттями одного дня.
        for timetable in teacher_daily_timetable.values():
            for times in timetable.values():
                times.sort()
                for i in range(len(times) - 1):
                    if times[i + 1] - times[i] > 95:
                        gaps_penalty += 1

        # 4. Підрахунок штрафів за «вікна» у розкладі студентських груп.
        # Аналогічний процес, що й для викладачів, але для розкладу груп.
        for timetable in group_daily_timetable.values():
            for times in timetable.values():
                times.sort()
                for i in range(len(times) - 1):
                    if times[i + 1] - times[i] > 95:
                        gaps_penalty += 1

        # Повертаємо загальний штраф за наявність «вікон» у розкладі.
        return gaps_penalty

    def _calculate_balance_penalty(self) -> float:
        # Розраховує штраф за незбалансованість розкладу протягом тижня.

        # 1. Ініціалізація підрахунку занять для кожного дня тижня.
        day_counts = {day: 0 for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]}

        # 2. Підрахунок кількості занять для кожного дня, заснований на розкладі.
        for _class in self._study_sessions:
            day_counts[_class.time_slot.day] += 1

        # 3. Знаходження максимального та мінімального значення кількості занять за тиждень.
        counts = list(day_counts.values())
        max_count = max(counts)
        min_count = min(counts)

        # Якщо занять немає (max_count == 0), повертаємо 0, щоб уникнути ділення на нуль.
        if max_count == 0:
            return 0.0

        # 4. Розрахунок штрафу за незбалансованість, нормалізуючи різницю між максимумом і мінімумом.
        balance_penalty = (max_count - min_count) / max_count
        return balance_penalty

    def calculate_fitness(self) -> float:
        # Розраховує фітнес розкладу, щоб оцінити його оптимальність.

        # 1. Оновлюємо кількість конфліктів у розкладі та обчислюємо штраф за "вікна".
        number_of_conflicts = self._calculate_conflicts()
        gaps_penalty = self._calculate_gaps_penalty()

        # 2. Вибір метрики для розрахунку фітнесу.
        # Якщо функція приспособленості встановлена як "conflicts", обчислюємо фітнес лише на основі конфліктів.
        if self.data.fitness_function == "conflicts":
            self.conflicts_count = number_of_conflicts
            return 1 / (1.0 * (number_of_conflicts + 1))

        # Якщо функція фітнесу "gaps", то враховуємо тільки "вікна".
        elif self.data.fitness_function == "gaps":
            return 1 / (1.0 * (gaps_penalty + 1))

        # Якщо використовується комбінована функція фітнесу, враховуємо всі параметри.
        elif self.data.fitness_function == "combined":
            balance_penalty = self._calculate_balance_penalty()
            self.conflicts_count = number_of_conflicts + gaps_penalty

            # Розрахунок загального фітнесу з урахуванням різних штрафів.
            fitness = 1 / (1.0 * (self.conflicts_count + 1))
            fitness -= gaps_penalty * 0.01
            fitness -= balance_penalty * 0.1

            return fitness

    def _calculate_conflicts_fitness(self) -> float:
        # Розраховує "фітнес" на основі кількості конфліктів у розкладі.

        number_of_conflicts = 0  # Ініціалізація лічильника конфліктів.

        # 1. Ініціалізація структур для перевірки конфліктів для груп, викладачів та аудиторій.
        group_timetable = {}
        teacher_timetable = {}
        classroom_timetable = {}

        # 2. Проходимо по кожному заняттю і перевіряємо конфлікти за групою, викладачем та аудиторією.
        for _class in self._study_sessions:
            group_key = (_class.student_group.name, _class.time_slot.id)
            teacher_key = (_class.teacher.id, _class.time_slot.id)
            classroom_key = (_class.classroom.number, _class.time_slot.id)

            # Перевірка конфліктів для групи: якщо ключ вже існує, додаємо конфлікт.
            if group_key in group_timetable:
                number_of_conflicts += 1
            else:
                group_timetable[group_key] = True

            # Перевірка конфліктів для викладача.
            if teacher_key in teacher_timetable:
                number_of_conflicts += 1
            else:
                teacher_timetable[teacher_key] = True

            # Перевірка конфліктів для аудиторії.
            if classroom_key in classroom_timetable:
                number_of_conflicts += 1
            else:
                classroom_timetable[classroom_key] = True

            # Перевірка на відповідність місткості аудиторії.
            if _class.classroom and _class.student_group.num_students > _class.classroom.seating_capacity:
                number_of_conflicts += 1

        # Зберігаємо кількість конфліктів і повертаємо фітнес значення.
        self.conflicts_count = number_of_conflicts
        return 1 / (1.0 * (self.conflicts_count + 1))

    def _calculate_gaps_fitness(self) -> float:
        # Розраховує "фітнес" на основі кількості "вікон" (пробілів між заняттями) у розкладі.
        # Використовується для мінімізації непотрібних перерв між заняттями.

        gaps_penalty = self._calculate_gaps_penalty()  # Отримуємо штраф за "вікна".
        return 1 / (1.0 * (gaps_penalty + 1))  # Розраховуємо фітнес, де чим менший штраф, тим вище значення фітнесу.

    def _calculate_combined_fitness(self) -> float:
        # Розраховує комбіновану функцію "фітнесу", яка враховує кількість конфліктів,
        # "вікна", збалансованість занять за днями.

        number_of_conflicts = 0  # Ініціалізація лічильника конфліктів.
        gaps_penalty = self._calculate_gaps_penalty()  # Штраф за "вікна".
        balance_penalty = self._calculate_balance_penalty()  # Штраф за незбалансованість занять.

        group_timetable = {}  # Словник для перевірки конфліктів за групою.
        teacher_timetable = {}  # Словник для перевірки конфліктів за викладачем.
        classroom_timetable = {}  # Словник для перевірки конфліктів за аудиторією.

        # Проходимо по кожному заняттю в розкладі та перевіряємо конфлікти.
        for _study_session in self._study_sessions:
            group_key = (_study_session.student_group.name, _study_session.time_slot.id)  # Унікальний ключ для групи і часу.
            teacher_key = (_study_session.teacher.id, _study_session.time_slot.id)  # Унікальний ключ для викладача і часу.
            classroom_key = (_study_session.classroom.number, _study_session.time_slot.id)  # Унікальний ключ для аудиторії і часу.

            # Перевірка конфліктів для групи.
            if group_key in group_timetable:
                number_of_conflicts += 1
            else:
                group_timetable[group_key] = True

            # Перевірка конфліктів для викладача.
            if teacher_key in teacher_timetable:
                number_of_conflicts += 1
            else:
                teacher_timetable[teacher_key] = True

            # Перевірка конфліктів для аудиторії.
            if classroom_key in classroom_timetable:
                number_of_conflicts += 1
            else:
                classroom_timetable[classroom_key] = True

            # Перевірка на відповідність місткості аудиторії.
            if _study_session.classroom and _study_session.student_group.num_students > _study_session.classroom.seating_capacity:
                number_of_conflicts += 1

        self.conflicts_count = number_of_conflicts  # Зберігаємо кількість конфліктів.

        # Комбінована функція фітнесу: розраховуємо загальний фітнес з урахуванням усіх штрафів.
        fitness = 1 / (1.0 * (self.conflicts_count + 1))  # Основний фітнес на основі кількості конфліктів.
        fitness -= gaps_penalty * 0.01  # Враховуємо штраф за "вікна".
        fitness -= balance_penalty * 0.1  # Враховуємо штраф за незбалансованість.

        return fitness
