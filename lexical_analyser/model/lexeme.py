class Lexeme:
    def __init__(self, code, value, position, lexeme_type):
        self.code = code
        self.value = value
        self.position = position
        self.type = lexeme_type

    def __repr__(self):
        return "{0} {1}".format(self.code, self.value)


class Position:
    def __init__(self, row, column):
        self.row = row
        self.column = column

    def __repr__(self):
        return "{0}:{1}".format(self.row, self.column)
