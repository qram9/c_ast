"""This file holds all data types that are
usable with variables in this HIR. Some
regular types like Int, Char, Short and 
some unusual types like Int8, Int16, etc are
provided. In order to add a type to a variable
use the 'specifiers' defined towards the end of this 
file. For example, specifiers.inT references the
object of class Int."""

from hir.Specifier import Specifier

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


class Long(Specifier):
    'long type'

    def __str__(self):
        return 'long'


class Float(Specifier):
    'float type'

    def __str__(self):
        return 'float'


class Double(Specifier):
    'double type'

    def __str__(self):
        return 'double'


class Global(Specifier):
    'global qualifier'

    def __str__(self):
        return 'global'


class Volatile(Specifier):
    'Volatile qualifier'

    def __str__(self):
        return 'volatile'


class Restrict(Specifier):
    'Restrict specifier'

    def __str__(self):
        return 'restrict'


class Extern(Specifier):
    'Extern qualifier'

    def __str__(self):
        return 'extern'


class Inline(Specifier):
    'Inline qualifier'

    def __str__(self):
        return 'inline'


class Void(Specifier):
    'void qualifier'

    def __str__(self):
        return 'void'


class Auto(Specifier):
    'auto qualifier'

    def __str__(self):
        return 'auto'


class Const(Specifier):
    'const qualifier'

    def __str__(self):
        return 'const'


class Register(Specifier):
    'register qualifier'

    def __str__(self):
        return 'register'


class Static(Specifier):
    'static qualifier'

    def __str__(self):
        return 'static'


class Reference(Specifier):
    '& qualifier'

    def __str__(self):
        return '&'


class Byte(Specifier):
    'byte type'

    def __str__(self):
        return 'byte'


class Signed(Specifier):
    'signed type'

    def __str__(self):
        return 'signed'


class Unsigned(Specifier):
    'unsigned type'

    def __str__(self):
        return 'unsigned'


class Specifiers(object):
    __slots__ = ('types',
                 'spec',
                 'UserSpecifiedBittypeList',
                 'int8', 'int16', 'int32',
                 'uint8', 'uint16', 'uint32',
                 'inT', 'shorT', 'chaR', 'uchaR',
                 'lonG', 'signeD', 'unsigneD',
                 'floaT', 'doublE', 'voiD', 'consT',
                 'volatilE', 'autO', 'registeR', 'restricT',
                 'statiC', 'exterN', 'inlinE', 'referencE',
                 'bytE', 'Global')

    def __init__(self):
        self.types = {}
        self.types['Int8'] = Int8()
        int16 = Int16()
        self.types['Int16'] = int16
        self.types['Short'] = int16
        self.types['Int'] = Int()
        self.types['Int32'] = Int32()
        self.types['Uint8'] = Uint8()
        self.types['Uint16'] = Uint16()
        self.types['Uint32'] = Uint32()
        self.types['Char'] = Char()
        self.types['Uchar'] = Uchar()
        self.types['UserSpecifiedBittypeList'] = []
        self.types['Float'] = Float()
        self.types['Double'] = Double()
        self.types['Byte'] = Byte()
        self.types['Long'] = Long()

        self.spec = {}
        self.spec['Global'] = Global()
        self.spec['Volatile'] = Volatile()
        self.spec['Static'] = Static()
        self.spec['Extern'] = Extern()
        self.spec['Inline'] = Inline()
        self.spec['Void'] = Void()
        self.spec['Auto'] = Auto()
        self.spec['Const'] = Const()
        self.spec['Reference'] = Reference()
        self.spec['Register'] = Register()
        self.spec['Restrict'] = Restrict()
        self.spec['Signed'] = Signed()
        self.spec['Unsigned'] = Unsigned()

# class UsertypeFactory(type):
#     def __call__(self, *args, **kwargs):
#         '''Create a new instance'''
#         obj = type.__call__(self, *args)
#         for name in kwargs:
#             setattr(obj, name, kwargs[name])
#         return obj
#
# # TODO, later
# class UserSpecifiedBittype(Specifier, metaclass=UsertypeFactory):
#     '''UserSpecifiedBittype customizes
# native types, int, uint
# according to user specified sizes.
# Uses metaclass User as a class factory'''
#     __slots__ = ['nativetype', 'sz']
#     def __init__(self, sz, nativetype):
#         self.nativetype = nativetype
#         self.sz = sz
#     def __str__(self):
#         return '%s:%d' % (self.nativetype.__name__, self.sz)
#     def __getstate__(self):
#         items = {}
#         for name in UserSpecifiedBittype.__slots__:
#             items[name] = getattr(self,name)
#         return dict(items)
#     def __setstate__(self, statedict):
#         for k,v in list(statedict.items()):
#             setattr(self, k, v)

# specifiers.UserSpecifiedBittypeList \
# specifiers.UserSpecifiedBittypeList.append(UserSpecifiedBittype(sz=1,nativetype=Int)) = specifiers.types['UserSpecifiedBittypeList']


specifiers = Specifiers()
specifiers.Global = specifiers.spec['Global']
specifiers.autO = specifiers.spec['Auto']
specifiers.bytE = specifiers.types['Byte']
specifiers.chaR = specifiers.types['Char']
specifiers.doublE = specifiers.types['Double']
specifiers.exterN = specifiers.spec['Extern']
specifiers.floaT = specifiers.types['Float']
specifiers.inlinE = specifiers.spec['Inline']
specifiers.int16 = specifiers.types['Int16']
specifiers.int32 = specifiers.types['Int32']
specifiers.inT = specifiers.int32
specifiers.int8 = specifiers.types['Int8']
specifiers.referencE = specifiers.spec['Reference']
specifiers.registeR = specifiers.spec['Register']
specifiers.restricT = specifiers.spec['Restrict']
specifiers.shorT = specifiers.types['Short']
specifiers.signeD = specifiers.spec['Signed']
specifiers.statiC = specifiers.spec['Static']
specifiers.consT = specifiers.spec['Const']
specifiers.uchaR = specifiers.types['Uchar']
specifiers.uint16 = specifiers.types['Uint16']
specifiers.uint32 = specifiers.types['Uint32']
specifiers.uint8 = specifiers.types['Uint8']
specifiers.unsigneD = specifiers.spec['Unsigned']
specifiers.voiD = specifiers.spec['Void']
specifiers.volatilE = specifiers.spec['Volatile']

BYTE = specifiers.bytE
CHAR = specifiers.chaR
DOUBLE = specifiers.doublE
FLOAT = specifiers.floaT
INT = specifiers.inT
INT16 = specifiers.int16
INT32 = specifiers.int32
INT8 = specifiers.int8
SHORT = specifiers.shorT
UCHAR = specifiers.uchaR
UINT16 = specifiers.uint16
UINT32 = specifiers.uint32
UINT8 = specifiers.uint8

AUTO = specifiers.autO
CONST = specifiers.consT
EXTERN = specifiers.exterN
GLOBAL = specifiers.Global
INLINE = specifiers.inlinE
REFERENCE = specifiers.referencE
REGISTER = specifiers.registeR
RESTRICT = specifiers.restricT
SIGNED = specifiers.signeD
STATIC = specifiers.statiC
UNSIGNED = specifiers.unsigneD
VOID = specifiers.voiD
VOLATILE = specifiers.volatilE

if __name__ == "__main__":
    for k, v in list(specifiers.types.items()):
        print(k, '==', v.__doc__)
        if (type(v) == list):
            print(k, '->', ['%s' % elem for elem in v])
            print('type(', k, ') = ', ['%s' % type(elem) for elem in v])
        else:
            print(k, '->', v)
            print('type(', k, ') = ', type(v))
    for k, v in list(specifiers.spec.items()):
        print(k, '==', v.__doc__)
