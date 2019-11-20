from hir.Traversable import Traversable


class Declarator(Traversable):
    def __init__(self):
        Traversable.__init__(self)
        self.setNumChildren(0)
