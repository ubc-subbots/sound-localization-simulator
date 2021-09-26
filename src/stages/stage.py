class Stage:
    def __init__(self):
        pass

    def write_frame(self, frame):
        frame[self.__class__.__name__] = self.signal