import syntax_analyser.controller.constants as constants
import lexical_analyser.model.keywords as keywords
import lexical_analyser.model.lexeme_types as types
from syntax_analyser.exceptions.exceptions import UnexpectedTokenException, UnexpectedEndOfFileException
from syntax_analyser.model.syntax_tree import TreeNode


class Controller:
    def __init__(self, scanner, view):
        self.syntax_tree = TreeNode(constants.SIGNAL_PROGRAM)
        self.scanner = scanner
        self.view = view

    def run(self):
        try:
            root = self.syntax_tree.add_child(constants.PROGRAM)
            self.process_keyword(root, keywords.PROGRAM)
            self.process_custom_identifier(root, constants.PROCEDURE_IDENTIFIER)
            self.process_keyword(root, keywords.SEMICOLON)
            self.process_block(root)
            self.process_keyword(root, keywords.DOT)
            self.handle_unexpected_tokens()
        finally:
            if self.view:
                self.view.display(self.syntax_tree)

        return self.syntax_tree

    def process_block(self, node):
        root = node.add_child(constants.BLOCK)
        self.process_declarations(root)
        self.process_keyword(root, keywords.BEGIN)
        self.process_statements(root)
        self.process_keyword(root, keywords.END)

    def process_declarations(self, node):
        root = node.add_child(constants.DECLARATIONS)
        self.process_const_declarations(root)

    def process_const_declarations(self, node):
        root = node.add_child(constants.CONSTANT_DECLARATIONS)
        token = self.scanner.look_ahead()
        if not token or token.value != keywords.CONST:
            root.add_child(constants.EMPTY)
            return
        self.process_keyword(root, keywords.CONST)
        self.process_declarations_list(root)

    def process_declarations_list(self, node):
        root = node.add_child(constants.CONSTANT_DECLARATIONS_LIST)
        token = self.scanner.look_ahead()
        if not token or token.type != types.IDENTIFIER:
            root.add_child(constants.EMPTY)
            return

        self.process_constant_declaration(root)
        self.process_declarations_list(root)

    def process_constant_declaration(self, node):
        root = node.add_child(constants.CONSTANT_DECLARATION)
        self.process_custom_identifier(root, constants.CONSTANT_IDENTIFIER)
        self.process_keyword(root, keywords.EQUAL)
        self.process_constant(root)
        self.process_keyword(root, keywords.SEMICOLON)

    def process_constant(self, node):
        root = node.add_child(constants.CONSTANT)
        token = self.require_token(constants.CONSTANT)
        if token.type != types.CONSTANT:
            raise UnexpectedTokenException(constants.CONSTANT, token)
        root.add_child(token)

    def process_statements(self, node):
        root = node.add_child(constants.STATEMENTS_LIST)
        token = self.scanner.look_ahead()
        if not token or token.value != keywords.IF:
            root.add_child(constants.EMPTY)
            return

        self.process_keyword(root, keywords.IF)
        self.process_constant_declaration(root)
        self.process_keyword(root, keywords.THEN)
        self.process_constant(root)
        self.process_keyword(root, keywords.FI)
        self.process_statements(root)

    def process_custom_identifier(self, node, identifier):
        root = node.add_child(identifier)
        self.process_identifier(root)

    def process_identifier(self, node):
        token = self.require_token(constants.IDENTIFIER)
        if token.type != types.IDENTIFIER:
            raise UnexpectedTokenException(constants.IDENTIFIER, token)
        node.add_child(constants.IDENTIFIER).add_child(token)

    def process_keyword(self, node, keyword):
        token = self.require_token(keyword)
        if token.value != keyword:
            raise UnexpectedTokenException(keyword, token)
        node.add_child(token)

    def require_token(self, required):
        token = self.scanner.next_token()
        if not token:
            raise UnexpectedEndOfFileException(required)
        return token

    def handle_unexpected_tokens(self):
        token = self.scanner.next_token()
        if token:
            raise UnexpectedTokenException(constants.EOF, token)
