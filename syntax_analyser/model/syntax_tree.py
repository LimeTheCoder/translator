
class TreeNode:
    def __init__(self, value, parent=None, childs=None):
        self.value = str(value)
        self.parent = parent
        self.childs = childs if childs else []

    def add_child(self, value):
        node = TreeNode(value)
        node.parent = self
        self.childs.append(node)
        return node

    def to_list(self):
        res = [self.value]
        if not self.childs:
            return res

        for child in self.childs:
            res += child.to_list()

        return res

    def __str__(self, level=0):
        ret = "\t" * level + repr(self.value) + "\n"
        for child in self.childs:
            ret += child.__str__(level + 1)
        return ret

    def __repr__(self):
        return self.value
