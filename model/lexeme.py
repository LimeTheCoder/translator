class Lexeme:
    def __init__(self, code, value, position):
        self.code = code
        self.value = value
        self.position = position

    def __repr__(self):
        return "{0} {1} {2}".format(self.code, self.value, self.position)


class Position:
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def __repr__(self):
        return "{0}:{1}".format(self.row, self.column)
