from controller.lexer_controller import Controller
from controller.scanner import Scanner
from model.lexer_model import Model
from view.console_view import ConsoleView

if __name__ == '__main__':
    model = Model()
    view = ConsoleView('Parsed tokens:')
    with Scanner('tests/data/test_full_grammar') as scanner:
        controller = Controller(model, view, scanner)
        controller.run()
