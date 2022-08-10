class Event:
    def __init__(self):
        self.listeners = []

    def add_listener(self, listener):
        """Shortcut for using += to add a listener."""
        self.listeners.append(listener)
        return self

    def post_event(self, *args, **kwargs):
        for listener in self.listeners:
            listener(*args, **kwargs)
