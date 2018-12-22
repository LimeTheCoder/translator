from lexical_analyser.model.lexeme import Position


class Scanner:
    __DEFAULT_CHECKPOINT = 'DEFAULT_CHECKPOINT'

    def __init__(self, filename):
        self.__file = open(filename, 'r')
        self.__currPos = Position(1, 1)
        self.__checkpoints = {
            self.__DEFAULT_CHECKPOINT: Position(1, 1)
        }

    def read_next(self):
        ch = self.__file.read(1)

        if ch == '\n':
            self.__currPos.row += 1
            self.__currPos.column = 1
        else:
            self.__currPos.column += 1

        return ch

    def make_checkpoint(self, name=None):
        if name is None:
            name = self.__DEFAULT_CHECKPOINT

        self.__checkpoints[name] = self.get_previous_position()

    def get_checkpoint(self, name=None):
        if name is None:
            name = self.__DEFAULT_CHECKPOINT

        checkpoint = self.__checkpoints[name]
        return Position(checkpoint.row, checkpoint.column)

    def get_previous_position(self):
        prev_column = self.__currPos.column - 1
        prev_row = self.__currPos.row

        if prev_column <= 0:
            prev_column = 1
            prev_row -= 1

        return Position(prev_row, prev_column)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__file.close()
