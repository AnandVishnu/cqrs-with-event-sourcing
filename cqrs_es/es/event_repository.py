from .event_store import EventStore
from cqrs_es.bus import Bus
from cqrs_es.domain.aggregate import Aggregate
from typing import Type

class Repository():
    def __init__(self, store:EventStore, bus: Bus, aggregate: Type[Aggregate]):
        self.store = store
        self.bus = bus
        self.aggregate = aggregate

    def save_event(self, aggregate:Aggregate, expected_version:int):
        result = self.store.save_events(aggregate.id, aggregate.get_uncommitted_changes(), expected_version)
        aggregate.clear_uncommitted_changes()

    def create_instance(self) -> Aggregate:
        return self.aggregate()

    def get_by_id(self, aggregate_id):
        agg_instance = self.create_instance()
        events = self.store.get_events_for_aggregate(aggregate_id)
        agg_instance.load_from_history(events)
        return agg_instance

    def replay_history(self, aggregate_id):
        return self.get_by_id(aggregate_id)


