from Specifier import Specifier
"""This file holds all data types that are
usable with variables in this HIR. Some 
regular types like Int, Char, Short and 
some unusual types like Int8, Int16, etc are
provided. An UserSpecifiedBitType is also
available. Using this class, the user can 
instantiate datatype objects with a specified
bitwidth. 

In order to add a type to a variable
use the 'specifiers' defined towards the end of this 
file. For example, specifiers.inT references the
object of class Int. 

TODO: Specifiers will lead to 
problems when cloning and pickling, leading to confusion 
while comparing two and objects. Because cloning creates 
a duplicate object with a different python id, a comparison
between 2 objects of the same class Int will return False.
I plan to use Classes instead of objects to specify the
dependency cleanly.  This file will be updated soon with 
that change"""
# Type specifiers
class Int(Specifier):
	'Unsized signed int'
	def __str__(self):
		return 'int'

class Uint(Specifier):
	'Unsized unsigned int'
	def __str__(self):
		return 'uint'

class Int8(Specifier):
	'8 bit signed int'
	def __str__(self):
		return 'int8'

class Int16(Specifier):
	'16 bit signed int'
	def __str__(self):
		return 'int16'

class Int32(Specifier):
	'32 bit signed int'
	def __str__(self):
		return 'int'

class Uint8(Specifier):
	'8 bit unsigned int'
	def __str__(self):
		return 'uint8'

class Uint16(Specifier):
	'16 bit unsigned int'
	def __str__(self):
		return 'uint16'

class Uint32(Specifier):
	'32 bit unsigned int'
	def __str__(self):
		return "uint32"

class Char(Specifier):
	'char'
	def __str__(self):
		return "char"

class Uchar(Specifier):
	'unsigned char'
	def __str__(self):
		return "uchar"

class Global(Specifier):
	'global qualifier'
	def __str__(self):
		return 'global'

class Specifiers(object):
	__slots__ = ['types', 
								'spec', 
								'UserSpecifiedBittypeList', 
								'int8', 'int16', 'int32', 
								'uint8', 'uint16', 'uint32', 
								'inT', 'shorT', 'chaR', 'uchaR', 
								'Global']
	def __init__(self):
		int8 = Int8()
		self.types = {}
		self.types['Int8'] = int8
		int16 = Int16()
		self.types['Int16'] = int16
		self.types['Short'] = int16
		int_type = Int()
		self.types['Int'] = int_type
		int32 = Int32()
		self.types['Int32'] = int32
		uint8 = Uint8()
		self.types['Uint8'] = uint8
		uint16 = Uint16()
		self.types['Uint16'] = uint16
		uint32 = Uint32()
		self.types['Uint32'] = uint32
		char = Char()
		self.types['Char'] = char
		uchar = Uchar()
		self.types['Uchar'] = uchar
		self.types['UserSpecifiedBittypeList'] = []
		self.spec = {}
		glob = Global()
		self.spec['Global'] = glob

class UsertypeFactory(type):
	def __call__(self, *args, **kwargs):
		'''Create a new instance'''
		obj = type.__call__(self, *args)
		for name in kwargs:
			setattr(obj, name, kwargs[name])
		return obj

# TODO, later
class UserSpecifiedBittype(Specifier):
	'''UserSpecifiedBittype customizes 
native types, int, uint 
according to user specified sizes. 
Uses metaclass User as a class factory'''
	__metaclass__ = UsertypeFactory
	__slots__ = ['nativetype', 'size']
	def __str__(self):
		return '%s:%d' % (self.nativetype.__name__, self.size)
	def __getstate__(self):
		items = {}
		for name in UserSpecifiedBittype.__slots__:
			items[name] = getattr(self,name)
		return dict(items)
	def __setstate__(self, statedict):
		for k,v in statedict.items():
			setattr(self, k, v)

specifiers = Specifiers()
specifiers.int8 = specifiers.types['Int8']
specifiers.int16 = specifiers.types['Int16']
specifiers.shorT = specifiers.types['Short']
specifiers.int32 = specifiers.types['Int32']
specifiers.inT = specifiers.int32
specifiers.uint8 = specifiers.types['Uint8']
specifiers.uint16 = specifiers.types['Uint16']
specifiers.uint32 = specifiers.types['Uint32']
specifiers.chaR = specifiers.types['Char']
specifiers.uchaR = specifiers.types['Uchar']
specifiers.UserSpecifiedBittypeList \
= specifiers.types['UserSpecifiedBittypeList']
specifiers.UserSpecifiedBittypeList.append(UserSpecifiedBittype(size=1,nativetype=Int))
specifiers.Global = specifiers.spec['Global']

if __name__ == "__main__":
	for k,v in specifiers.types.items():
		print k, '==', v.__doc__
		if (type(v) == list):
			print k, '->', ['%s' % elem for elem in v]
			print 'type(', k, ') = ', ['%s' % type(elem) for elem in v]
		else:
			print k, '->', v
			print 'type(', k, ') = ', type(v)

