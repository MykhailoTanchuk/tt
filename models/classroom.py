#classroom.py

class Classroom:
    def __init__(self, number: str, seating_capacity: int):
        if not number or not isinstance(number, str):
            raise ValueError("Room number must be a non-empty string.")
        if not isinstance(seating_capacity, int) or seating_capacity <= 0:
            raise ValueError("Seating capacity must be a positive integer.")

        self._number = number
        self._seating_capacity = seating_capacity

    @property
    def number(self) -> str:
        return self._number

    @property
    def seating_capacity(self) -> int:
        return self._seating_capacity

    def __str__(self) -> str:
        return f"Classroom {self.number} (Capacity: {self.seating_capacity})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, Classroom):
            return False
        return self.number == other.number

    def __hash__(self) -> int:
        return hash(self.number)
