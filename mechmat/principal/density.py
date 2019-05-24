from .. import ureg

__all__ = ['from_specific_weight']


def from_specific_weight(specific_weight):
    r"""

    Args:
        specific_weight:

    Returns:

    """
    return specific_weight / ureg.g_n
