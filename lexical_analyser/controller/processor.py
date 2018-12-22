from lexical_analyser.controller.exceptions import UnexpectedSymbolException, UnexpectedEndOfFileException
from lexical_analyser.model import keywords


class InputProcessor:
    def __init__(self, model, scanner):
        self.model = model
        self.scanner = scanner

    def accept(self, ch):
        pass

    def process(self, ch):
        pass


class IdentifierProcessor(InputProcessor):
    def accept(self, ch):
        return is_letter(ch)

    def process(self, ch):
        identifier = ''
        self.scanner.make_checkpoint()

        while is_letter(ch) or is_digit(ch):
            identifier += ch
            ch = self.scanner.read_next()

        self.model.add_identifier(identifier, self.scanner.get_checkpoint())
        return ch


class SpacesProcessor(InputProcessor):
    __SPACE_CODES = [9, 10, 11, 12, 13, 32]

    def accept(self, ch):
        return ch and ord(ch) in self.__SPACE_CODES

    def process(self, ch):
        while self.accept(ch):
            ch = self.scanner.read_next()
        return ch


class CommentProcessor(InputProcessor):
    def accept(self, ch):
        return ch == '('

    def process(self, ch):
        self.scanner.make_checkpoint()
        curr = self.scanner.read_next()
        if curr != '*':
            raise UnexpectedSymbolException(self.scanner.get_checkpoint(), ch)

        prev = curr = ''
        while prev != '*' or curr != ')':
            prev = curr
            curr = self.scanner.read_next()

            if not curr:
                raise UnexpectedEndOfFileException(self.scanner.get_previous_position())

        return self.scanner.read_next()


class DelimitersProcessor(InputProcessor):
    __DELIMITERS = [keywords.DOT, keywords.SEMICOLON, keywords.EQUAL]

    def accept(self, ch):
        return ch in self.__DELIMITERS

    def process(self, ch):
        while self.accept(ch):
            self.model.add_delimiter(ch, self.scanner.get_previous_position())
            ch = self.scanner.read_next()
        return ch


class ErrorProcessor(InputProcessor):
    def accept(self, ch):
        return True

    def process(self, ch):
        raise UnexpectedSymbolException(self.scanner.get_previous_position(), ch)


class NumberProcessor(InputProcessor):
    __SIGN_CHARS = ['+', '-']
    __FRACTIONAL_SEPARATOR = '#'
    __START_CHECKPOINT = 'NUMBER_START_CHECKPOINT'

    def accept(self, ch):
        return is_digit(ch) or self.__is_sign__(ch)

    def process(self, ch):
        self.scanner.make_checkpoint(self.__START_CHECKPOINT)
        number, last_ch = self.__read_unsigned_number__()
        if self.__is_sign__(ch) and not number:
            raise UnexpectedSymbolException(self.scanner.get_checkpoint(), ch)

        fractional, last_ch = self.__handle_fractional_part__(last_ch)
        number = ch + number + fractional
        self.model.add_constant(number, self.scanner.get_checkpoint(self.__START_CHECKPOINT))
        return last_ch

    def __handle_fractional_part__(self, last_ch):
        if last_ch != self.__FRACTIONAL_SEPARATOR:
            return '', last_ch

        head_ch = self.__read_number_head_symbol__()
        fractional, last_ch = self.__read_number__(head_ch)
        return self.__FRACTIONAL_SEPARATOR + fractional, last_ch

    def __read_number_head_symbol__(self):
        head_ch = self.scanner.read_next()

        if not head_ch:
            raise UnexpectedEndOfFileException(self.scanner.get_previous_position())

        if not self.accept(head_ch):
            raise UnexpectedSymbolException(self.scanner.get_previous_position(), head_ch)
        return head_ch

    def __read_number__(self, head_ch):
        self.scanner.make_checkpoint()

        fractional, last_ch = self.__read_unsigned_number__()
        if self.__is_sign__(head_ch) and not fractional:
            raise UnexpectedSymbolException(self.scanner.get_checkpoint(), head_ch)
        return head_ch + fractional, last_ch

    def __read_unsigned_number__(self):
        number = ''
        while True:
            ch = self.scanner.read_next()
            if not is_digit(ch):
                break

            number += ch
        return number, ch

    def __is_sign__(self, ch):
        return ch in self.__SIGN_CHARS


def is_digit(ch):
    return '0' <= ch <= '9'


def is_letter(ch):
    return 'A' <= ch <= 'Z'
