from .store import Store
from typing import List, Any

class InMemoryStore(Store):
    def __init__(self):
        self.db.view = {}


    def save(self, events: List[Any]):
        pass

    def get_by_id(self, id):
        pass

