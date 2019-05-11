__all__ = ['OutOfRangeError']


class OutOfRangeError(ValueError):
    r"""
    Raised when trying to set an out-of-range value
    """

    def __init__(self, value, rng, property):
        super(OutOfRangeError, self).__init__()
        self.value = value
        self.rng = rng
        self.property = property

    def __str__(self):
        return "Setting the material attribute {} with{} is out of range {}".format(self.property, self.value, self.rng)
