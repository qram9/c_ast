from Specifier import Specifier

class ArraySpecifierException(Exception):
	def __init__(self, value):
		self.value = value

class InvalidTypeDimensionsError(ArraySpecifierException):
	"""Exception, raised when Invalid type (non-list) for dimensions 
is specified"""
	def __repr__(self):
		return 'Invalid Type: (%s) for Dimensions, expected list' %(value)
	__str__ = __repr__

class InvalidValueDimensionError(ArraySpecifierException):
	"""Exception, raised when the contents of 
specified dimensions are not integers"""
	def __repr__(self):
		return 'Invalid Value: (%s) for dimension value' %(value)
	__str__ = __repr__

class InvalidIndexDimensionsError(ArraySpecifierException): pass
		
class ArraySpecifier(Specifier):
	"""Represents an Array Specifier part of an array 
declaration in C. Initialized with a list 
containing dimensions. for ex: For A[10][20], the
contents of dimensions will be the list [10,20]""" 
	__slots__ = ['dimensions']

	def __init__(self, dimensions):
		"""Initialize an array specifier with a list
of ints for dimensions"""
		self.dimensions = []
		if not dimensions:
			raise InvalidTypeDimensionsError(str(type(dimensions)))
		for k in dimensions:
			if not isinstance(k, int):
				raise InvalidValueDimensionError(str(type(k)))
			self.dimensions.append(k)

	def getNumDimensions(self):
		"""Returns the number of dimensions
in the dimensions list specifier"""
		return self.dimensions.size()
	def getDimension(self, n):
		"""Returns a specified dimension"""
		try:
			return self.dimensions[n]
		except IndexError:
			raise InvalidIndexDimensionsError, "%d %d" %(len(self.dimensions), n)

	def setDimension(self, n, val):
		"""Sets a specified dimension to given value"""
		self.dimensions[n] = val

	def __repr__(self):
		"""Returns a string representation of the contents 
of the array specifier object. Currently the returned 
string is in AnsiC. For example [1][2][3].
Change this function to return different 
a representation."""
		retval = ''
		for k in self.dimensions:
			retval += '['
			retval += str(k)
			retval += ']'
		return retval
	__str__ = __repr__

	def items(self):
		"""Returns the 'dimensions' list of ints"""
		items = {}
		items['dimensions'] = self.dimensions
		for k in ArraySpecifier.__bases__:
			if hasattr(k, 'items'):
				supitems = k.items(self)
				for k,v in supitems.items():
					items[k] = v
		return dict(items)
	def __getstate__(self):
		"""Returns the 'dimensions' list of ints. Calls items directly"""
		return self.items()
	def __setstate__(self, statedict):
		"""Blindly sets the state of this object, using a statedict"""
		for k,v in statedict.items():
			setattr(self, k, v)

def ArraySpecifierTest():
	k = ArraySpecifier([1,2,4])
	return k

if __name__ == '__main__':
	ArraySpecifierTest()
	
