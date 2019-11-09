from hir.Literal import Literal

class InvalidTypeFloatLiteralError(Exception):
	def __init__(self, value):
		self.value = value
	def __repr__(self):
		return 'Invalid type: (%s) for integer literal, expected: (%s)' % (value, str(type(int)))

class FloatLiteral(Literal):
	"""Represents a Float literal lexical token.
Subclasses Literal type. Sets the given character
value to a __slots__ entry 'value'."""
	__slots__ = ['value']
	def __init__(self, value):
		"""Initializes a Ansi C Float Literal object. Tests
if given character is of type python <float>. Sets the
__slots__.value parameter"""
		if not isinstance(value, float):
			raise InvalidTypeFloatLiteralError(str(type(value)))
		self.initialize()
		Literal.__init__(self)
		self.value = value
	def __repr__(self):
		return str(self.value)
	__str__ = __repr__
	def items(self):
		"""Returns items dict when called from hir.etstate. 
Adds __slots__ entry "value" to items dict.
Recurses into base classes and collects items from hir.here too."""
		items = {}
		items['value'] = self.value
		for k in FloatLiteral.__bases__:
			if hasattr(k, 'items'):
				supitems = k.items(self)
				for k,v in list(supitems.items()):
					items[k] = v
		return dict(items)
	def __getstate__(self):
		"""Returns current state for 'pickling' or 'copy'. 
Adds __slots__ entry "value" to items dict."""
		return dict(self.items())
	def __setstate__(self, statedict):
		"""Blindly sets state from hir. given statedict"""
		for k,v in list(statedict.items()):
			setattr(self, k, v)


def FloatLiteralTest():
	l = FloatLiteral(1.25)
	return l

if __name__ == '__main__':
	print(FloatLiteralTest())

