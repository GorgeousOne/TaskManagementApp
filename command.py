import argparse


class Command:
	"""An abstract class for commands"""
	def __init__(self, name, description=""):
		self.name = name
		self.description = description

	def execute(self, str_args):
		pass

	def print_help(self):
		print("Unrecognised command")


class ParentCommand(Command):
	"""A command that has other commands as children and will delegate arguments to them"""
	def __init__(self, name, description=""):
		super().__init__(name, description)
		self.children = []

	def add_child(self, command):
		self.children.append(command)

	def execute(self, str_args):
		if len(str_args) == 0:
			self.print_help()
			return

		for child in self.children:
			if child.name == str_args[0]:
				child.execute(str_args[1:])
				return
		self.print_help()

	def print_help(self):
		print("sub commands:")
		for child in self.children:
			print(("  " + child.name).ljust(23), child.description)


class ArgCommand(Command):
	"""A command that interprets arguments with an ArgumentParser"""
	def __init__(self, name, method, description=""):
		super().__init__(name, description)
		self.method = method
		self.parser = argparse.ArgumentParser(description)

	def get_parser(self):
		return self.parser

	def execute(self, str_args):
		if not self.method(self.parser.parse_args(str_args)):
			self.parser.print_help()

	def print_help(self):
		self.parser.print_help()
