import unittest

from lexical_analyser.controller.lexer_controller import Controller as LexicalController
from lexical_analyser.controller.scanner import Scanner as LexicalScanner
from lexical_analyser.model.lexer_model import Model as LexicalModel
from syntax_analyser.controller.scanner import Scanner as SyntaxScanner
from syntax_analyser.controller.syntax_controller import Controller as SyntaxController
from syntax_analyser.exceptions.exceptions import UnexpectedEndOfFileException, UnexpectedTokenException
from syntax_analyser.view.syntax_view import ConsoleTreeView


class SyntaxAnalyserTest(unittest.TestCase):

    def run_controller(self, filename):
        lexer_info = self.parse_tokens(filename)
        token_scanner = SyntaxScanner(lexer_info)
        syntax_controller = SyntaxController(token_scanner, ConsoleTreeView)
        return syntax_controller.run()

    def parse_tokens(self, filename):
        model = LexicalModel()
        with LexicalScanner(filename) as scanner:
            controller = LexicalController(model, None, scanner)
            controller.run()
        return model.get_model_data()

    def test_full_grammar(self):
        filename = 'data/test_full_grammar'
        tree = self.run_controller(filename)
        self.assertEqual(['<signal-program>',
                          '<program>',
                          '401 PROGRAM',
                          '<procedure-identifier>',
                          '<identifier>',
                          '1001 TEST1',
                          '59 ;',
                          '<block>',
                          '<declarations>',
                          '<constant-declarations>',
                          '404 CONST',
                          '<constant-declarations-list>',
                          '<constant-declaration>',
                          '<constant-identifier>',
                          '<identifier>',
                          '1002 DAREN',
                          '61 =',
                          '<constant>',
                          '501 56',
                          '59 ;',
                          '<constant-declarations-list>',
                          '<constant-declaration>',
                          '<constant-identifier>',
                          '<identifier>',
                          '1003 VARIABLE',
                          '61 =',
                          '<constant>',
                          '502 +356#94',
                          '59 ;',
                          '<constant-declarations-list>',
                          '<constant-declaration>',
                          '<constant-identifier>',
                          '<identifier>',
                          '1004 CASH',
                          '61 =',
                          '<constant>',
                          '503 987#-321',
                          '59 ;',
                          '<constant-declarations-list>',
                          '<empty>',
                          '402 BEGIN',
                          '<statements-list>',
                          '<empty>',
                          '403 END',
                          '46 .'], tree.to_list())

    def test_grammar_without_declarations(self):
        filename = 'data/syntax_grammar_no_declarations'
        tree = self.run_controller(filename)
        self.assertEqual(['<signal-program>',
                          '<program>',
                          '401 PROGRAM',
                          '<procedure-identifier>',
                          '<identifier>',
                          '1001 TEST1',
                          '59 ;',
                          '<block>',
                          '<declarations>',
                          '<constant-declarations>',
                          '<empty>',
                          '402 BEGIN',
                          '<statements-list>',
                          '<empty>',
                          '403 END',
                          '46 .'], tree.to_list())

    def test_not_complete_program(self):
        filename = 'data/test_basic_grammar'
        self.assertRaises(
            UnexpectedEndOfFileException,
            self.run_controller, filename
        )

    def test_unexpected_token(self):
        filename = 'data/syntax_unexpected_token'
        self.assertRaises(
            UnexpectedTokenException,
            self.run_controller, filename
        )

    def test_unexpected_tokens_after_correct_grammar(self):
        filename = 'data/unexpected_tokens_after_correct_grammar'
        self.assertRaises(
            UnexpectedTokenException,
            self.run_controller, filename
        )


if __name__ == '__main__':
    unittest.main()
