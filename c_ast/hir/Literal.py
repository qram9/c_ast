from hir.Expression import Expression


class Literal(Expression):
    """Represents a base class to store 
IntegerLiteral, CharLiteral, FloatLitertal Ansi C 
types"""

    def __init__(self):
        """Initializes the type by calling 
Expression.__init__() assistance to 
subclasses"""
        self.initialize()
        Expression.__init__(self)
