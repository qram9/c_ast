
from hir.Statement import Statement
class Default(Statement):
	"""The Ansi C default statement."""
	def __repr__(self):
		return 'default' + ':'
def DefaultTest():
	k = Default()
	return k

if __name__ == '__main__':
	print(DefaultTest())
