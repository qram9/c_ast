
from hir.Statement import Statement


class BreakStatement(Statement):
    """Represents the break statement in Ansi C.
Nothing much to see here"""

    def __repr__(self):
        return 'break' + ';'


def BreakTest():
    k = BreakStatement()
    return k


if __name__ == '__main__':
    print(BreakTest())
