from cqrs_es.bus import Bus
from cqrs_es.events import Event, EventDescriptor
from typing import List


class EventStore:
    def __init__(self, bus : Bus):
        self.bus = bus
        self.event_db = {}

    def save_events(self, aggregate_id, events: List[Event], expected_version):
        if not aggregate_id in self.event_db:
            self.event_db[aggregate_id] = []
        elif self.event_db[aggregate_id][-1].version != expected_version:
            raise Exception("Concurrency Issues")
        i = expected_version
        agg_list = self.event_db[aggregate_id]
        for _event_ in events:
            i = i +1
            event_dis = EventDescriptor(_event_, i)
            agg_list.append(event_dis)
            self.bus.publish_event(_event_)

        return self.event_db[aggregate_id]

    def get_events_for_aggregate(self, aggregate_id):
        return self.event_db[aggregate_id]