class Error(Exception):
	"""General error class"""

	def __init__(self, msg):
		self.msg = msg

	def __str__(self):
		return str(self.msg)

class InputError(Error):
	"""You got the wrong input there buddy"""
	pass

class UnknownInstructionError(Error):
	"""What in the world is that supposed to mean?"""
	pass

class UnknownLabelError(Error):
	"""Nope, that's not a function!"""
	pass

class EmptyStackError(Error):
	"""Brah, your stack is empty!"""
	pass

class ArgumentError(Error):
	"""Dude, use the right arguments, aight?"""
	pass