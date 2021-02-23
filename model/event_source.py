
class EventSource:
    def __init__(self, event_method_name):
        self._listeners = []
        self._event_method_name = event_method_name

    def add_listener(self, listener):
        update_method = getattr(listener, self._event_method_name, None)
        if not callable(update_method):
            raise Exception("Could not add listener missing the " + self._event_method_name + " method.")
        self._listeners.append(listener)

    def remove_listener(self, listener):
        self._listeners.remove(listener)

    def update_listeners(self):
        for listener in self._listeners:
            getattr(listener, self._event_method_name)(self)
