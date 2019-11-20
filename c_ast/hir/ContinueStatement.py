
from hir.Statement import Statement


class ContinueStatement(Statement):
    """Nothing to see here. Self-explanatory"""

    def __repr__(self):
        return 'continue' + ';'


def ContinueTest():
    k = ContinueStatement()
    return k


if __name__ == '__main__':
    print(ContinueTest())
