from mechcite import cite
from math import pi

__all__ = ['circle', 'annulus']


@cite('rao_basic_2017')
def circle(V_dot, r):
    r""""
    The apparent shear rate for a melt flowing through a cirlce is defined as

    .. math::

       \dot{\gamma}_{a}=\frac{4 \dot{V}}{\pi R^{3}}

    Source: Rao, Natti S. Basic Polymer Engineering Data. Cincinnati, Ohio, USA: Hanser, 2017.

    Args:
        V_dot: Volumetric_flow in :math:`[L^{3} t^{-1}]`
        r: Radius in :math:`[L^{1}]`

    Returns:
        Apparent shear rate in :math:`[t^{-1}]`
    """
    return 4. * V_dot / (pi * r ** 3)


@cite('rao_basic_2017')
def annulus(V_dot, r_i, r_o):
    r"""
    The apparent shear rate for a melt flowing through a annulus is defined as

    .. math::

       \frac{6 \dot{V}}{\pi\left(r_{o}+r_{i}\right)\left(r_{o}-r_{i}\right)^{2}}

    Source: Rao, Natti S. Basic Polymer Engineering Data. Cincinnati, Ohio, USA: Hanser, 2017.


    Args:
        V_dot: Volumetric_flow in :math:`[L^{3} t^{-1}]`
        r_i: inner radius in :math:`[L^{1}]`
        r_o: inner radius in :math:`[L^{1}]`

    Returns:
        Apparent shear rate in :math:`[t^{-1}]`
    """
    return 6. * V_dot / (pi * (r_o + r_i) * (r_o - r_i) ** 2)
