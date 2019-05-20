from .. import ureg

__all__ = ['from_density']


def from_density(density):
    r"""

    Args:
        density:

    Returns:

    """
    return density * ureg.g_n
