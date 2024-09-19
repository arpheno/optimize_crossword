class IOutputHandler(ABC):
    @abstractmethod
    def output(self, solution: CrosswordSolution, slots: List[Slot]):
        pass

class PrintOutputHandler(IOutputHandler):
    def output(self, solution: CrosswordSolution, slots: List[Slot]):
        print("Crossword Solution:")
        for slot in slots:
            word = solution.slots.get(slot.slot_id)
            print(f"Slot {slot.slot_id} (Length {slot.length}): {word}")

class HTTPOutputHandler(IOutputHandler):
    def __init__(self, url: str):
        self.url = url

    def output(self, solution: CrosswordSolution, slots: List[Slot]):
        import requests
        data = {
            'solution': {str(slot_id): word for slot_id, word in solution.slots.items()}
        }
        response = requests.post(self.url, json=data)
        if response.status_code == 200:
            print("Solution successfully sent to server.")
        else:
            print(f"Failed to send solution. Status code: {response.status_code}")
