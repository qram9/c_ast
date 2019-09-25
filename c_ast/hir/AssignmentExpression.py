from BinaryExpression import BinaryExpression
from operator import assignmentOperator
class AssignmentExpression(BinaryExpression):
	"""Assignment Expression works on any 
sequence with three args, lhs, op, rhs. 
Except for a differentiating class type, and 
operator from the assignment operators group, 
instances hold same data as BinaryExpression 
instances."""
	def __init__(self, *args):
		lhs, op, rhs = args
		BinaryExpression.__init__(self, lhs, op, rhs)

def AssignmentExpressionTest():
	from Identifier import Identifier
	return AssignmentExpression(Identifier('a'), assignmentOperator.ADD, Identifier('b'))

if __name__ == '__main__':
	print AssignmentExpressionTest()
