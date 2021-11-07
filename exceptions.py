class MyException(Exception):
    # Exception message set by value
    def __init__(self, value):
        self.parameter = value

    # Exception message to be printed
    def __str__(self):
        return self.parameter


