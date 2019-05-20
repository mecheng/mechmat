from .. import ureg

__all__ = ['from_specific_weight', 'from_specific_volume']


def from_specific_weight(specific_weight):
    r"""

    Args:
        specific_weight:

    Returns:

    """
    return specific_weight / ureg.g_n


def from_specific_volume(specific_volume):
    r"""

    Args:
        specific_volume:

    Returns:

    """
    return specific_volume ** -1
