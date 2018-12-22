class SyntaxAnalyserException(Exception):
    def __init__(self, expected=None, token=None):
        self.expected = expected
        self.token = token


class UnexpectedTokenException(SyntaxAnalyserException):
    def __str__(self):
        return "Syntax Analyser: ({0}) Wanted {1} but received {2}"\
            .format(self.token.position, self.expected, self.token.value)


class UnexpectedEndOfFileException(SyntaxAnalyserException):
    def __str__(self):
        return "Syntax Analyser: Unexpected end of file, expected {0} instead".format(self.expected)
