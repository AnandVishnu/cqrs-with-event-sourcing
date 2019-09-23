from cqrs_es.command import Command
from cqrs_es.events import Event


class Bus:
    def __init__(self, market):
        self.command_map = {}
        self.event_map = {}
        self.market = market


    def register_commands(self, types, action):
        for type in types:
            self.register_command(type, action)

    def register_command(self, type, action):
        self.command_map[type] = action

    def register_events(self, types, action):
        for type in types:
            self.register_event(type, action)

    def register_event(self, type, action):
        if type not in self.event_map:
            self.event_map[type] = []

        self.event_map[type].append(action)

    def send_command(self, cmd:Command):
        cmd_name = cmd.name
        handler = self.command_map[cmd_name]
        return handler(cmd)

    def publish_event(self, evt: Event):
        event_name = evt.name
        handlers = self.event_map[event_name]
        for handler in handlers:
            handler(evt)



