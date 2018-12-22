class LexerException(Exception):
    def __init__(self, position, value=None):
        self.position = position
        self.value = value


class UnexpectedSymbolException(LexerException):
    def __str__(self):
        return "Lexer: Unexpected symbol: {0} at position: {1}".format(self.value, self.position)


class UnexpectedEndOfFileException(LexerException):
    def __str__(self):
        return "Lexer: Unexpected end of file at position: {0}".format(self.position)
