from typing import Set

class Solution:
    def __init__(self,
                 id: str, 
                 requirements: Set[str],
                 capabilities: Set[str],
                 cs_type: str):
        self.id = id
        self.requirements = frozenset(requirements)
        self.capabilities = frozenset(capabilities)
        self.cs_type = cs_type

    def __str__(self):
        return f"Solution(id={self.id}, requirements={self.requirements}, capabilities={self.capabilities}, cs_type={self.cs_type})"

    def __hash__(self) -> int:
        id_hash = hash(self.id)
        reqs_hash = hash(self.requirements)
        caps_hash = hash(self.capabilities)
        cs_type_hash = hash(self.cs_type)
        return hash(id_hash + reqs_hash + caps_hash + cs_type_hash)

    def __eq__(self, other) -> bool:
        return self.cs_type == other.cs_type and \
            self.requirements == other.requirements and \
            self.capabilities == other.capabilities and \
            self.id == other.id
