#genetic_algorithm.py
from copy import deepcopy
from random import shuffle
from typing import Any

from output_utils import get_random_number
from population import Population
from timetable import Timetable
from models.time_slot import TimeSlot


class GenAlg:
    def __init__(self, data: Any,
                 num_elite_timetables: int,
                 crossover_rate: float,
                 mutation_rate: float,
                 tournament_size: int,
                 fitness_function: str = "conflicts",
                 predation_rate: float = 0.2):  # Частка популяції, яку видаляють під час "хижого" відбору
        self.data = data
        self.num_elite_timetables = num_elite_timetables
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.tournament_size = tournament_size
        self.fitness_function = fitness_function

        # Параметр для "хижого" підходу
        self.predation_rate = predation_rate

    def evolve(self, population: Population, generation_number: int) -> Population:
        """Виконує одну ітерацію еволюції популяції."""
        # Створюємо нову популяцію шляхом мутації та кросовера
        new_population = self.mutate_population(self.crossover_population(population))

        # Застосовуємо "хижий" підхід до нової популяції
        self.apply_predation(new_population)

        #Додаємо "дощ" кожні 7 поколінь для підвищення різноманітності популяції
        if generation_number % 7 == 0:
            self.apply_rain(new_population, rain_rate=0.1)  # Використовуємо коефіцієнт "дощу" у 10%

        # Гарантуємо стабільний розмір популяції
        self._ensure_population_stability(new_population, len(population.timetables))
        return new_population

    def crossover_population(self, population: Population) -> Population:
        """Виконує кросовер для створення нової популяції."""
        new_population = Population(size=len(population.timetables), data=self.data)

        # Зберігаємо елітні розклади (найкращі) без змін
        for idx in range(self.num_elite_timetables):
            new_population.timetables[idx] = deepcopy(population.timetables[idx])

        # Виконуємо кросовер для решти розкладів
        for idx in range(self.num_elite_timetables, len(population.timetables)):
            if self.crossover_rate > get_random_number():
                # Вибираємо двох батьків за допомогою турнірного відбору
                parent1 = self.select_tournament_population(population).sort_by_fitness().timetables[0]
                parent2 = self.select_tournament_population(population).sort_by_fitness().timetables[1]
                # Створюємо новий розклад на основі батьківських розкладів
                new_population.timetables[idx] = self.crossover_timetable(parent1, parent2)
            else:
                new_population.timetables[idx] = deepcopy(population.timetables[idx])

        return new_population

    def crossover_timetable(self, timetable1: Timetable, timetable2: Timetable) -> Timetable:
        """Створює новий розклад шляхом кросовера двох батьківських розкладів."""
        min_study_session_count = min(len(timetable1.study_sessions), len(timetable2.study_sessions))
        new_timetable = Timetable(data=self.data, fitness_function=self.fitness_function)

        # Випадково вибираємо заняття від кожного з батьків
        for idx in range(min_study_session_count):
            new_study_session = (
                deepcopy(timetable1.study_sessions[idx])
                if get_random_number() > 0.5
                else deepcopy(timetable2.study_sessions[idx])
            )
            new_timetable.study_sessions.append(new_study_session)

        # Додаємо решту занять з обох батьківських розкладів
        for idx in range(min_study_session_count, len(timetable1.study_sessions)):
            new_timetable.study_sessions.append(deepcopy(timetable1.study_sessions[idx]))

        for idx in range(min_study_session_count, len(timetable2.study_sessions)):
            new_timetable.study_sessions.append(deepcopy(timetable2.study_sessions[idx]))

        return new_timetable

    def mutate_population(self, population: Population) -> Population:
        """Виконує мутацію для популяції."""
        new_population = Population(size=len(population.timetables), data=self.data)

        # Зберігаємо елітні розклади без змін
        for idx in range(self.num_elite_timetables):
            new_population.timetables[idx] = deepcopy(population.timetables[idx])

        # Мутуємо решту розкладів
        for idx in range(self.num_elite_timetables, len(population.timetables)):
            new_population.timetables[idx] = self.mutate_timetable(population.timetables[idx])

        return new_population

    def mutate_timetable(self, timetable: Timetable) -> Timetable:
        """Виконує нетривіальну мутацію для одного розкладу."""
        mutated_timetable = deepcopy(timetable)

        if self.mutation_rate > get_random_number():
            # Випадково обираємо тип мутації
            mutation_type = get_random_number()
            if mutation_type < 0.33:
                # Swap Mutation - обмін часових слотів між заняттями
                mutated_timetable = self.swap_mutation(mutated_timetable)
            elif mutation_type < 0.66:
                # Inversion Mutation - інвертування порядку занять
                mutated_timetable = self.inversion_mutation(mutated_timetable)
            else:
                # Scramble Mutation - перемішування часових слотів
                mutated_timetable = self.scramble_mutation(mutated_timetable)

        return mutated_timetable

    def swap_mutation(self, timetable: Timetable) -> Timetable:
        """Обмін часових слотів двох випадкових занять."""
        idx1 = int(get_random_number() * len(timetable.study_sessions))
        idx2 = int(get_random_number() * len(timetable.study_sessions))

        study_session1 = timetable.study_sessions[idx1]
        study_session2 = timetable.study_sessions[idx2]

        # Обмінюємо time_slot між двома заняттями
        study_session1.time_slot, study_session2.time_slot = study_session2.time_slot, study_session1.time_slot

        # Оновлюємо розклад
        timetable.study_sessions[idx1] = study_session1
        timetable.study_sessions[idx2] = study_session2

        return timetable

    def inversion_mutation(self, timetable: Timetable) -> Timetable:
        """Інвертує порядок проведення серії занять для випадкової групи студентів."""
        # Вибираємо випадкову групу студентів із доступних
        group = self._get_random_item(self.data.groups)

        # Знаходимо всі заняття цієї групи у поточному розкладі
        group_study_sessions = [cls for cls in timetable.study_sessions if cls.student_group.id == group.id]

        # Перевіряємо, чи кількість занять групи більша за 2, інакше інверсія недоцільна
        if len(group_study_sessions) > 2:
            # Вибираємо випадковий індекс для початку та кінця інверсії
            idx_start = int(get_random_number() * (len(group_study_sessions) - 1))
            idx_end = int(get_random_number() * (len(group_study_sessions) - idx_start)) + idx_start

            # Створюємо список індексів занять, що підлягають інверсії
            timetable_indices = [timetable.study_sessions.index(group_study_sessions[i]) for i in range(idx_start, idx_end + 1)]

            # Створюємо інвертований список занять
            inverted_study_sessions = list(reversed([timetable.study_sessions[i] for i in timetable_indices]))

            # Оновлюємо розклад, замінюючи заняття на інвертовані
            for i, idx in enumerate(timetable_indices):
                timetable.study_sessions[idx] = inverted_study_sessions[i]

        return timetable

    def scramble_mutation(self, timetable: Timetable) -> Timetable:
        """Перемішує часові слоти кількох випадкових занять у розкладі."""
        # Вибираємо випадкову кількість занять для перемішування (до половини від усіх занять)
        num_study_sessions_to_scramble = int(get_random_number() * len(timetable.study_sessions) / 2) + 1
        indices = [int(get_random_number() * len(timetable.study_sessions)) for _ in range(num_study_sessions_to_scramble)]

        # Вибираємо випадкові заняття для перемішування
        study_sessions_to_scramble = [timetable.study_sessions[i] for i in indices]

        # Збираємо time_slot для цих занять та перемішуємо
        time_slots = [cls.time_slot for cls in study_sessions_to_scramble]
        shuffle(time_slots)  # Перемішуємо часи проведення занять

        # Присвоюємо перемішані часові слоти назад обраним заняттям
        for i, idx in enumerate(indices):
            timetable.study_sessions[idx].time_slot = time_slots[i]

        return timetable

    def apply_rain(self, population: Population, rain_rate: float = 0.1) -> None:
        """Застосовує метод "дощу" для підвищення різноманітності популяції."""
        num_to_replace = int(len(population.timetables) * rain_rate)

        for _ in range(num_to_replace):
            # Заміна найслабших особин на нові випадкові розклади
            new_timetable = Timetable(data=self.data, fitness_function=self.fitness_function).initialize()
            population.timetables[-1] = new_timetable
            population.sort_by_fitness()  # Пересортування для збереження кращих особин на початку

    def apply_predation(self, population: Population) -> None:
        """Застосовує 'хижий' відбір, видаляючи слабких та розмножуючи сильних особин."""
        num_timetables = len(population.timetables)
        num_to_remove = int(num_timetables * self.predation_rate)

        # Сортуємо популяцію за рівнем пристосованості
        population.sort_by_fitness()

        # Видаляємо слабких особин
        weakest_indices = list(range(num_timetables - num_to_remove, num_timetables))
        for idx in reversed(weakest_indices):
            del population.timetables[idx]

        # Розмножуємо сильних особин
        best_timetables = population.timetables[:num_to_remove]
        new_timetables = []

        for timetable in best_timetables:
            # Клонуємо та мутуємо розклад
            cloned_timetable = deepcopy(timetable)
            mutated_timetable = self.aggressive_mutate_timetable(cloned_timetable)
            new_timetables.append(mutated_timetable)

        # Додаємо нових особин до популяції
        population.timetables.extend(new_timetables)

    def aggressive_mutate_timetable(self, timetable: Timetable) -> Timetable:
        """Виконує більш агресивну мутацію для даного розкладу."""
        mutated_timetable = deepcopy(timetable)

        for idx in range(len(mutated_timetable.study_sessions)):
            # Збільшуємо ймовірність мутації
            if (self.mutation_rate * 2) > get_random_number():
                study_session_to_mutate = mutated_timetable.study_sessions[idx]

                # З більшою ймовірністю змінюємо викладача або аудиторію
                mutation_choice = get_random_number()
                if mutation_choice < 0.5:
                    # Міняємо викладача на іншого, здатного вести цей курс
                    suitable_teachers = [
                        teacher for teacher in self.data.teachers
                        if teacher.can_teach(study_session_to_mutate.course.number)
                    ]
                    if suitable_teachers:
                        study_session_to_mutate.teacher = self._get_random_item(suitable_teachers)
                else:
                    # Міняємо аудиторію на випадкову
                    study_session_to_mutate.classroom = self._get_random_item(self.data.classrooms)

                # З ймовірністю 30% змінюємо час заняття
                if get_random_number() < 0.3:
                    study_session_to_mutate.time_slot = self._get_random_item(self.data.time_slots)

                # Оновлюємо розклад
                mutated_timetable.study_sessions[idx] = study_session_to_mutate

        return mutated_timetable

    def _get_valid_time_slot(self, timetable: Timetable) -> TimeSlot:
        """Повертає випадковий час, перевіряючи його доступність."""
        available_times = deepcopy(self.data.time_slots)
        shuffle(available_times)

        # Пошук вільного часу, який не зайнятий в поточному розкладі
        for time in available_times:
            if not any(cls.time_slot.id == time.id for cls in timetable.study_sessions):
                return time
        return self._get_random_item(self.data.time_slots)

    def _get_random_item(self, items: list) -> Any:
        """Вибирає випадковий елемент зі списку."""
        return items[int(get_random_number() * len(items))]

    def select_tournament_population(self, population: Population) -> Population:
        """Вибирає популяцію для турніру."""
        tournament_population = Population(size=self.tournament_size, data=self.data)
        for idx in range(self.tournament_size):
            random_index = int(get_random_number() * len(population.timetables))
            tournament_population.timetables[idx] = population.timetables[random_index]
        return tournament_population

    def _ensure_population_stability(self, population: Population, expected_size: int) -> None:
        """Перевіряє та гарантує стабільність розміру популяції."""
        current_size = len(population.timetables)
        if current_size != expected_size:
            # Якщо розмір не збігається, коригуємо популяцію
            if current_size > expected_size:
                # Видаляємо зайві розклади
                population.timetables = population.timetables[:expected_size]
            else:
                # Додаємо нові випадкові розклади
                for _ in range(expected_size - current_size):
                    new_timetable = Timetable(data=self.data, fitness_function=self.fitness_function).initialize()
                    population.timetables.append(new_timetable)


# fitness time кожен заняття на тиждень  - має знаходитись різниця скільки є розкладів і скільки може бути
# мутації - додати ще 2  ( прибрати будь яке заняття , додати будь яке заняття в розклад ( будь який предмет і тд і засунути в розклад))