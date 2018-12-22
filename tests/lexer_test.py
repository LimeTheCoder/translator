import unittest

from lexical_analyser.controller.exceptions import UnexpectedEndOfFileException, UnexpectedSymbolException
from lexical_analyser.controller.lexer_controller import Controller
from lexical_analyser.controller.scanner import Scanner
from lexical_analyser.model.lexer_model import Model
from lexical_analyser.view.console_view import ConsoleView


class TranslatorTest(unittest.TestCase):

    def run_controller(self, filename):
        self.model = Model()
        self.view = ConsoleView('Parsed tokens:')

        with Scanner(filename) as scanner:
            controller = Controller(self.model, self.view, scanner)
            controller.run()

    def test_basic_grammar(self):
        filename = 'data/test_basic_grammar'
        self.run_controller(filename)

        lexemes, identifiers, constants = self.model.get_model_data()

        lexemes_str = [str(lexeme) for lexeme in lexemes]
        self.assertEqual(['401 PROGRAM', '1001 TEST1', '59 ;'], lexemes_str)
        self.assertEqual({'TEST1': 1001}, identifiers)
        self.assertEqual({}, constants)

    def test_full_grammar(self):
        filename = 'data/test_full_grammar'
        self.run_controller(filename)

        lexemes, identifiers, constants = self.model.get_model_data()

        lexemes_str = [str(lexeme) for lexeme in lexemes]
        expected_lexemes_str = ['401 PROGRAM', '1001 TEST1', '59 ;', '404 CONST',
                                '1002 DAREN', '61 =', '501 56', '59 ;', '1003 VARIABLE',
                                '61 =', '502 +356#94', '59 ;', '1004 CASH', '61 =',
                                '503 987#-321', '59 ;', '402 BEGIN', '403 END',
                                '46 .']
        self.assertEqual(expected_lexemes_str, lexemes_str)
        self.assertEqual({'CASH': 1004, 'DAREN': 1002, 'TEST1': 1001, 'VARIABLE': 1003}, identifiers)
        self.assertEqual({'56': 501, '+356#94': 502, '987#-321': 503}, constants)

    def test_store_parsed_lexemes_to_model_before_exception(self):
        filename = 'data/test_invalid_comment'
        self.assertRaises(
            UnexpectedSymbolException,
            self.run_controller, filename
        )

        lexemes, identifiers, constants = self.model.get_model_data()

        lexemes_str = [str(lexeme) for lexeme in lexemes]
        self.assertEqual(['401 PROGRAM', '1001 TEST1', '59 ;'], lexemes_str)
        self.assertEqual({'TEST1': 1001}, identifiers)
        self.assertEqual({}, constants)

    def test_unclosed_comment(self):
        filename = 'data/test_unclosed_comment'
        self.assertRaises(
            UnexpectedEndOfFileException,
            self.run_controller, filename
        )

    def test_invalid_comment(self):
        filename = 'data/test_invalid_comment'
        self.assertRaises(
            UnexpectedSymbolException,
            self.run_controller, filename
        )

    def test_uncompleted_number(self):
        filename = 'data/test_uncompleted_number'
        self.assertRaises(
            UnexpectedEndOfFileException,
            self.run_controller, filename
        )

    def test_invalid_number(self):
        filename = 'data/test_invalid_number'
        self.assertRaises(
            UnexpectedSymbolException,
            self.run_controller, filename
        )

    def test_invalid_symbol(self):
        filename = 'data/test_invalid_symbol'
        self.assertRaises(
            UnexpectedSymbolException,
            self.run_controller, filename
        )


if __name__ == '__main__':
    unittest.main()
