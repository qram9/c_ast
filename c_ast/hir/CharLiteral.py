from Literal import Literal

class InvalidTypeCharLiteralError(Exception):
	def __init__(self, value):
		self.value = value
	def __repr__(self):
		return 'Invalid type: (%s) for integer literal, expected: (%s)' % (value, str(type(int)))

class CharLiteral(Literal):
	"""Represents a character literal lexical token.
Subclasses Literal type. Sets the given character
value to a __slots__ entry 'value'."""
	__slots__ = ['value']
	def __init__(self, value):
		"""Initializes a Ansi C CharLiteral object. Tests
if given character is of type python <str>. Sets the
__slots__.value parameter"""
		if not isinstance(value, str):
			raise InvalidTypeCharLiteralError(str(type(value)))
		self.initialize()
		Literal.__init__(self)
		self.value = value
	def __repr__(self):
		"""Returns the AnsiC CharLiteral with a single quote 
around it. self.value __slots__ entry is used for this"""
		return "'" + str(self.value) + "'"
	__str__ = __repr__

	def items(self):
		"""Returns items dict when called from setstate. 
Adds __slots__ entry "value" to items dict.
Recurses into base classes and collects items from there too."""
		items = {}
		items['value'] = self.value
		for k in CharLiteral.__bases__:
			if hasattr(k, 'items'):
				supitems = k.items(self)
				for k,v in supitems.items():
					items[k] = v
		return dict(items)
	def __getstate__(self):
		"""Returns current state for 'pickling' or 'copy'. 
Adds __slots__ entry "value" to items dict."""
		return self.items()
	def __setstate__(self, statedict):
		"""Blindly sets state from a given statedict"""
		for k,v in statedict.items():
			setattr(self, k, v)

def CharLiteralTest():
	l = CharLiteral('a')
	return l

if __name__ == '__main__':
	print CharLiteralTest()

