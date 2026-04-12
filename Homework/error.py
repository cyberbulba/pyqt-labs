class ExampleError:
    def __init__(self, operation):
        self.operation = operation

    def get_result(self):
        return self.operation
