from numpy.linalg import norm
from mechmat import ureg

__all__ = ['distance', 'halfway']


@ureg.wraps(ureg.m, (ureg.m, ureg.m))
def distance(point_1, point_2):
    r"""
    Returns the distance between two points.


    Args:
        point_1: Scalar or vector of point 1
        point_2: Scalar or vector of point 2

    Returns:
        Scalar of the distance between point_2 and point_1

    """
    return norm(point_2 - point_1)


def halfway(point_1, point_2):
    return point_1 + (point_2 - point_1) / 2
