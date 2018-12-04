from controller.processor import IdentifierProcessor, SpacesProcessor, CommentProcessor, DelimitersProcessor, \
    NumberProcessor, ErrorProcessor


class Controller:
    def __init__(self, model, view, scanner):
        self.model = model
        self.view = view
        self.scanner = scanner
        self.processors = [IdentifierProcessor(model, scanner),
                           SpacesProcessor(model, scanner),
                           CommentProcessor(model, scanner),
                           DelimitersProcessor(model, scanner),
                           NumberProcessor(model, scanner)]
        self.error_processor = ErrorProcessor(model, scanner)

    def run(self):
        ch = self.scanner.read_next()
        try:
            while ch:
                processor = next((p for p in self.processors if p.accept(ch)), self.error_processor)
                ch = processor.process(ch)
        finally:
            self.view.display(self.model.get_model_data())
