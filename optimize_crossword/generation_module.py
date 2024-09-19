from abc import ABC, abstractmethod
from typing import List, Dict

from optimize_crossword.data_structures import Slot, CrosswordSolution


class ICrosswordGenerator(ABC):
    @abstractmethod
    def generate(self, slots: List[Slot], wordlist: Dict[int, List[str]]) -> CrosswordSolution:
        pass


class MIPCrosswordGenerator(ICrosswordGenerator):
    def generate(self, slots: List[Slot], wordlist: Dict[int, List[str]]) -> CrosswordSolution:
        # Implement the MIP crossword generation logic
        # Use the code from previous examples
        # Return a CrosswordSolution instance
        # For brevity, I'll include a simplified version
        import pulp

        slot_word_vars = {}
        prob = pulp.LpProblem("Crossword_Generation", pulp.LpMinimize)

        # Create variables
        for slot in slots:
            slot_id = slot.slot_id
            length = slot.length
            words_of_length = wordlist.get(length, [])
            for w in words_of_length:
                var_name = f"x_{slot_id}_{w}"
                slot_word_vars[(slot_id, w)] = pulp.LpVariable(var_name, cat="Binary")

        # Slot assignment constraints
        for slot in slots:
            slot_id = slot.slot_id
            length = slot.length
            words_of_length = wordlist.get(length, [])
            prob += pulp.lpSum(slot_word_vars[(slot_id, w)] for w in words_of_length) == 1

        # Word uniqueness constraints
        all_words = set(w for words in wordlist.values() for w in words)
        for w in all_words:
            slots_with_length = [slot for slot in slots if slot.length == len(w)]
            prob += pulp.lpSum(slot_word_vars[(slot.slot_id, w)] for slot in slots_with_length if
                               (slot.slot_id, w) in slot_word_vars) <= 1

        # Overlap constraints
        for slot in slots:
            slot_id = slot.slot_id
            for overlap in slot.overlaps:
                other_slot_id = overlap.other_slot_id
                own_index = overlap.own_index
                other_index = overlap.other_index
                if slot_id < other_slot_id:
                    slot_length = slot.length
                    other_slot = next(s for s in slots if s.slot_id == other_slot_id)
                    other_slot_length = other_slot.length
                    words_s = wordlist.get(slot_length, [])
                    words_t = wordlist.get(other_slot_length, [])
                    for w_s in words_s:
                        for w_t in words_t:
                            if w_s[own_index] != w_t[other_index]:
                                key_s = (slot_id, w_s)
                                key_t = (other_slot_id, w_t)
                                if key_s in slot_word_vars and key_t in slot_word_vars:
                                    prob += slot_word_vars[key_s] + slot_word_vars[key_t] <= 1

        # Solve the problem
        prob.solve()

        # Check if a solution was found
        if pulp.LpStatus[prob.status] == "Optimal":
            solution = {}
            for slot in slots:
                slot_id = slot.slot_id
                length = slot.length
                words_of_length = wordlist.get(length, [])
                for w in words_of_length:
                    var = slot_word_vars.get((slot_id, w))
                    if var is not None and pulp.value(var) == 1:
                        solution[slot_id] = w
                        break
            return CrosswordSolution(slots=solution)
        else:
            raise Exception("No valid crossword could be generated.")
