from mechcite import cite
from numpy import log, e

from mechmat import ureg

__all__ = ['get_specific_volume', 'get_B', 'switch_m_s', 'get_T_t', 'get_v_0', 'get_v_t']


@cite('osswald_polymer_2006')
def get_specific_volume(p, v_0, v_t, B):
    C = 0.0894
    return v_0 * (1. - C * log(1. + p / B)) + v_t


@cite('osswald_polymer_2006')
def get_v_0(T, b_1, b_2, b_5):
    return b_1 + b_2 * (T - b_5)


@cite('osswald_polymer_2006')
def get_v_t(p, T, T_t, b_5, b_7, b_8, b_9):
    if T > T_t:
        return 0. * ureg.m ** 3 / ureg.kg
    else:
        return b_7 * e ** (b_8 * (T - b_5) - b_9 * p)


@cite('osswald_polymer_2006')
def get_B(T, b_3, b_4, b_5):
    return b_3 * e ** (-b_4 * (T - b_5))


@cite('osswald_polymer_2006')
def get_T_t(p, b_5, b_6):
    return b_5 + b_6 * p


@cite('osswald_polymer_2006')
def switch_m_s(T, T_t, s, m):
    if T > T_t:
        return m
    else:
        return s
