from typing import List, Dict

from optimize_crossword.data_structures import Slot, CrosswordSolution


def generate_crossword(slots: List[Slot], wordlist: Dict[int, List[str]], generator: ICrosswordGenerator) -> CrosswordSolution:
    if not validate_slots(slots):
        raise ValueError("Invalid slots definition.")
    solution = generator.generate(slots, wordlist)
    return solution
