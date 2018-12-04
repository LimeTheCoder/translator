import texttable as tt


class ConsoleView:
    def __init__(self, message):
        self.__message = message

    def display(self, model_info):
        lexemes, _, _ = model_info

        if not lexemes:
            return

        tab = tt.Texttable()
        tab.header(['Row', 'Column', 'Code', 'Value'])
        for lexeme in lexemes:
            tab.add_row([lexeme.position.row, lexeme.position.column, lexeme.code, lexeme.value])

        print(self.__message)
        print(tab.draw())
        print('\n')
