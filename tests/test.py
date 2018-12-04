import unittest

from controller.exceptions import UnexpectedEndOfFileException, UnexpectedSymbolException
from controller.lexer_controller import Controller
from controller.scanner import Scanner
from model.lexer_model import Model
from view.console_view import ConsoleView


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
        self.assertEqual(['401 PROGRAM 1:1', '1001 TEST1 1:9', '59 ; 1:14'], lexemes_str)
        self.assertEqual({'TEST1': 1001}, identifiers)
        self.assertEqual({}, constants)

    def test_full_grammar(self):
        filename = 'data/test_full_grammar'
        self.run_controller(filename)

        lexemes, identifiers, constants = self.model.get_model_data()

        lexemes_str = [str(lexeme) for lexeme in lexemes]
        expected_lexemes_str = ['401 PROGRAM 1:1', '1001 TEST1 1:9', '59 ; 1:14', '404 CONST 3:1',
                                '1002 DAREN 4:5', '61 = 4:10', '501 56 4:11', '59 ; 4:13', '1003 VARIABLE 5:5',
                                '61 = 5:14', '502 +356#94 5:16', '59 ; 5:23', '1004 CASH 6:5', '61 = 6:10',
                                '503 987#-321 6:12', '59 ; 6:20', '402 BEGIN 8:1', '403 END 10:1',
                                '46 . 10:4']
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
        self.assertEqual(['401 PROGRAM 1:1', '1001 TEST1 1:9', '59 ; 1:14'], lexemes_str)
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
