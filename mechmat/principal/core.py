from scipy.interpolate import interp1d, interp2d
from warnings import warn
from functools import reduce
import operator
from mechmat import ureg

__all__ = ['reciprocal', 'sub', 'add', 'mul', 'div', 'Interp']


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


class Interp:
    def __init__(self, kind='cubic', cite=None, **kwargs):
        self._cite = cite
        self._kind = kind
        self._args = list(kwargs.keys())
        for key, value in kwargs.items():
            setattr(self, key, value)
        if cite:
            self._func = cite(self._build_interp(kind, **kwargs))
        else:
            self._func = self._build_interp(kind, **kwargs)

    def __call__(self, **kwargs):
        return self._func(*list(kwargs.values()))

    def _build_interp(self, kind, **kwargs):
        args = self._args
        if len(kwargs) == 2:
            try:
                self._interp = interp1d(getattr(self, args[0]).m, getattr(self, args[1]).m, kind=kind, copy=False)
            except ValueError:
                self._interp = interp1d(getattr(self, args[0]).m, getattr(self, args[1]).m, copy=False)
                self._kind = 'linear'
                warn('{}-interpolation not possible. Linear-interpolation is used as fallback.'.format(kind))

            @ureg.wraps(getattr(self, args[1]).u, getattr(self, args[0]).u)
            def func(x):
                return self._interp(x).item()
        elif len(kwargs) == 3:
            try:
                self._interp = interp2d(getattr(self, args[0]).m, getattr(self, args[1]).m, getattr(self, args[2]).m,
                                        kind=kind, copy=False)
            except ValueError:
                self._interp = interp2d(getattr(self, args[0]).m, getattr(self, args[1]).m, getattr(self, args[2]).m,
                                        copy=False)
                self._kind = 'linear'
                warn('{}-interpolation not possible. Linear-interpolation is used as fallback.'.format(kind))

            @ureg.wraps(getattr(self, args[2]).u, (getattr(self, args[0]).u, getattr(self, args[1]).u))
            def func(x, y):
                return self._interp(x, y).item()
        else:
            raise ValueError('Interp should have either one axis or two axes')
        return func
