from model.lexeme import Lexeme


class Model:
    __KEYWORDS = {
        'PROGRAM': 401,
        'BEGIN': 402,
        'END': 403,
        'CONST': 404
    }

    __CONSTANTS_OFFSET = 501
    __IDENTIFIERS_OFFSET = 1001

    def __init__(self):
        self.lexemes = list()
        self.constants = dict()
        self.identifiers = dict()

    def add_identifier(self, identifier, position):
        if identifier in self.__KEYWORDS:
            self.__add_to_output__(self.__KEYWORDS.get(identifier), identifier, position)
            return

        if identifier not in self.identifiers:
            self.identifiers[identifier] = len(self.identifiers) + self.__IDENTIFIERS_OFFSET

        self.__add_to_output__(self.identifiers[identifier], identifier, position)

    def add_delimiter(self, delimiter, position):
        self.__add_to_output__(ord(delimiter), delimiter, position)

    def add_constant(self, constant, position):
        if constant not in self.constants:
            self.constants[constant] = len(self.constants) + self.__CONSTANTS_OFFSET

        self.__add_to_output__(self.constants[constant], constant, position)

    def get_model_data(self):
        return self.lexemes, self.identifiers, self.constants

    def __add_to_output__(self, code, value, position):
        self.lexemes.append(Lexeme(code, value, position))
