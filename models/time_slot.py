#time_slot.py

class TimeSlot:
    def __init__(self, id: str, time: str, day: str):
        self.id = id
        self.time = time
        self.day = day

    def __str__(self) -> str:
        return f"{self.day} {self.time}"
