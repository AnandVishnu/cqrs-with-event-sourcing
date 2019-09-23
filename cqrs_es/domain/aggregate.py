from typing import List
from cqrs_es.events import Event, EventDescriptor

class Aggregate:
    def __init__(self):
        self.__changes__ = []

    def load_from_history(self, evts:List[EventDescriptor]):
        self.apply_changes([x.event_data for x in evts], False)

    def apply_changes(self, events, is_new=True):
        for event in events:
            self.apply(event)
            if is_new:
                self.__changes__.append(event)

    def apply(self, event, is_new):
        raise NotImplementedError('Must implement apply method')

    def get_uncommitted_changes(self):
        return self.__changes__

    def clear_uncommitted_changes(self):
        self.__changes__.clear()
