from functools import reduce
import operator

__all__ = ['reciprocal', 'sub', 'add', 'mul', 'div']


def reciprocal(value):
    return value ** -1


def sub(**kwargs):
    return reduce(operator.__sub__, kwargs.values())


def add(**kwargs):
    return reduce(operator.__add__, kwargs.values())


def mul(**kwargs):
    return reduce(operator.__mul__, kwargs.values())


def div(**kwargs):
    return reduce(operator.__truediv__, kwargs.values())
