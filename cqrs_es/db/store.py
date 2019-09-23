from abc import ABC, abstractmethod
from typing import List, Any

class Store:
    @abstractmethod
    def save(self, events: List[Any]):
        pass

    @abstractmethod
    def get_by_id(self, id):
        pass
