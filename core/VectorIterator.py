class VectorIterator:
    def __init__(self, vector):
        self.vector = vector
        self.index = 0

    def __iter__(self): # aby šel použít v for-cyklu - new(iterator)
        return self

    def reset(self):
        self.index = 0

    def __next__(self):
        if self.index < len(self.vector):
            val = self.vector[self.index]
            self.index += 1
            return val
        else:
            self.reset()
            val = self.vector[self.index]
            self.index += 1
            return val
