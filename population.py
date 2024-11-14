#population.py

from typing import List, Any
from timetable import Timetable

class Population:
    def __init__(self, size: int, data: Any):
        if size <= 0:
            raise ValueError("Population size must be a positive integer.")
        self.timetables: List[Timetable] = [Timetable(data).initialize() for _ in range(size)]

    def __str__(self) -> str:
        return "\n".join(str(timetable) for timetable in self.timetables)

    def sort_by_fitness(self) -> 'Population':
        self.timetables.sort(key=lambda timetable: timetable.fitness, reverse=True)
        return self
