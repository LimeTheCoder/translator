from lexical_analyser.controller.lexer_controller import Controller as LexicalController
from lexical_analyser.controller.scanner import Scanner as LexicalScanner
from lexical_analyser.model.lexer_model import Model as LexicalModel
from lexical_analyser.view.console_view import ConsoleView as LexicalView
from syntax_analyser.controller.scanner import Scanner as SyntaxScanner
from syntax_analyser.controller.syntax_controller import Controller as SyntaxController
from syntax_analyser.view.syntax_view import ConsoleTreeView


def parse_tokens():
    model = LexicalModel()
    view = LexicalView('Parsed tokens:')
    with LexicalScanner('tests/data/test_full_grammar') as scanner:
        controller = LexicalController(model, view, scanner)
        controller.run()
    return model.get_model_data()


if __name__ == '__main__':
    lexer_info = parse_tokens()
    token_scanner = SyntaxScanner(lexer_info)
    syntax_controller = SyntaxController(token_scanner, ConsoleTreeView)
    res = syntax_controller.run()
