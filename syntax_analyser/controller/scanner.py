class Scanner:
    def __init__(self, lexer_info):
        self.tokens, _, _ = lexer_info
        self.idx = 0

    def next_token(self):
        token = self.__get_token_by_idx__(self.idx)
        self.idx += 1
        return token

    def look_ahead(self):
        return self.__get_token_by_idx__(self.idx)

    def __get_token_by_idx__(self, idx):
        return self.tokens[idx] if idx < len(self.tokens) else None
