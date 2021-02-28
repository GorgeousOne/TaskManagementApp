import argparse


class Command:
	"""Abstract class for commands"""
	def __init__(self, name, description=""):
		self.name = name
		self.description = description

	def execute(self, str_args):
		pass

	def print_help(self):
		print("Unrecognised command")


class ParentCommand(Command):
	"""Can have other commands as children and will delegate arguments to them"""
	def __init__(self, name, description=""):
		super().__init__(name, description)
		self.children = []

	def add_child(self, command):
		self.children.append(command)

	def execute(self, str_args):
		for child in self.children:
			if child.name == str_args[0]:
				child.execute(str_args[1:])
				return
		self.print_help()

	def print_help(self):
		super().print_help()
		for child in self.children:
			print(child.name, child.description)


class ArgCommand(Command):
	"""Command that actually interprets arguments (aka wrapper for argument parser)"""
	def __init__(self, name, method, description=""):
		super().__init__(name, description)
		self.method = method
		self.parser = argparse.ArgumentParser(description)

	def get_parser(self):
		return self.parser

	def execute(self, str_args):
		self.method(self.parser.parse_args(str_args))

	def print_help(self):
		super().print_help()
		self.parser.print_help()
