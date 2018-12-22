from lexical_analyser.model.lexeme import Lexeme
import lexical_analyser.model.keywords as keywords
import lexical_analyser.model.lexeme_types as lexeme_types


class Model:
    __KEYWORDS = {
        keywords.PROGRAM: 401,
        keywords.BEGIN: 402,
        keywords.END: 403,
        keywords.CONST: 404,
        keywords.IF: 405,
        keywords.FI: 406,
        keywords.THEN: 407
    }

    __CONSTANTS_OFFSET = 501
    __IDENTIFIERS_OFFSET = 1001

    def __init__(self):
        self.lexemes = list()
        self.constants = dict()
        self.identifiers = dict()

    def add_identifier(self, identifier, position):
        if identifier in self.__KEYWORDS:
            self.__add_to_output__(self.__KEYWORDS.get(identifier), identifier, position, lexeme_types.KEYWORD)
            return

        if identifier not in self.identifiers:
            self.identifiers[identifier] = len(self.identifiers) + self.__IDENTIFIERS_OFFSET

        self.__add_to_output__(self.identifiers[identifier], identifier, position, lexeme_types.IDENTIFIER)

    def add_delimiter(self, delimiter, position):
        self.__add_to_output__(ord(delimiter), delimiter, position, lexeme_types.DELIMITER)

    def add_constant(self, constant, position):
        if constant not in self.constants:
            self.constants[constant] = len(self.constants) + self.__CONSTANTS_OFFSET

        self.__add_to_output__(self.constants[constant], constant, position, lexeme_types.CONSTANT)

    def get_model_data(self):
        return self.lexemes, self.identifiers, self.constants

    def __add_to_output__(self, code, value, position, lexeme_type):
        self.lexemes.append(Lexeme(code, value, position, lexeme_type))
