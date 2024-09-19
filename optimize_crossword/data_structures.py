from dataclasses import dataclass, field
from typing import List, Dict

@dataclass
class Overlap:
    other_slot_id: int
    own_index: int
    other_index: int

@dataclass
class Slot:
    slot_id: int
    length: int
    overlaps: List[Overlap] = field(default_factory=list)

@dataclass
class CrosswordSolution:
    slots: Dict[int, str]  # Mapping from slot_id to the assigned word


