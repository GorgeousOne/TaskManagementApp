
class EventSource:
	"""Abstract class that can store listeners and send events to them"""
	def __init__(self, event_method_name):
		"""event_method_name: the name of the method that will be called on each listener to get notified"""
		self.listeners = []
		self.event_method_name = event_method_name

	def add_listener(self, listener):
		update_method = getattr(listener, self.event_method_name, None)
		if not callable(update_method):
			raise Exception("Could not add listener missing the " + self.event_method_name + " method.")
		self.listeners.append(listener)

	def remove_listener(self, listener):
		self.listeners.remove(listener)

	def update_listeners(self):
		for listener in self.listeners:
			getattr(listener, self.event_method_name)(self)

	def __getstate__(self):
		"""Removes the listeners bound to the running session from the data to dump"""
		state = self.__dict__.copy()
		del state["listeners"]
		return state

	def __setstate__(self, state):
		self.__dict__.update(state)
		self.listeners = []