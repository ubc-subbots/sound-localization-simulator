class Stage:
    def __init__(self):
        self.signal = None

    def write_frame(self, frame):
        frame[self.__class__.__name__] = self.signal