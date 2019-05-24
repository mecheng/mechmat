#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `mechmat` package."""

import pytest

from mechmat import ureg as u
from mechmat.core.errors import OutOfRangeError
from pint import DimensionalityError


@pytest.fixture
def simple_material():
    from mechmat.material import material_factory
    from mechmat.properties.specific_volume import TwoDomainTaitpvT
    from mechmat.properties.viscosity import CrossArrhenius

    SimplePLA = material_factory(True, TwoDomainTaitpvT, CrossArrhenius,
                                 temperature=20. * u.degc,
                                 pressure=1. * u.bar,
                                 volume=100. * u.mm * 3,
                                 b_1s=0.000821 * u.m ** 3 / u.kg,
                                 b_1m=0.000826 * u.m ** 3 / u.kg,
                                 b_2s=4.469e-7 * u.m ** 3 / (u.kg * u.K),
                                 b_2m=8.503e-7 * u.m ** 3 / (u.kg * u.K),
                                 b_3s=2.14200e8 * u.Pa,
                                 b_3m=1.628000e8 * u.Pa,
                                 b_4s=0.006079 * u.K ** -1,
                                 b_5=348.15 * u.K,
                                 b_6=9.547e-8 * u.K / u.Pa,
                                 b_7=0. * u.m ** 3 / u.kg,
                                 b_8=0. * u.K ** -1,
                                 b_9=0. * u.Pa ** -1,
                                 arrhenius_activation_energy=70.7 * u.kJ / u.mol,
                                 relaxation_time_ref=0.01 * u.s,
                                 viscosity_zero_shear_rate_ref=2039. * u.Pa * u.s,
                                 shear_thinning_const=0.82,
                                 temperature_cross_arrhenius_ref=210. * u.degC)

    return SimplePLA


def test_state(simple_material):
    mat_a = simple_material()
    assert mat_a.temperature == 20. * u.degC


# def test_mod_state(simple_material):
#     mat_a = simple_material()
#     mat_a.y = 9. * u.m ** 2
#     assert mat_a.y == 9. * u.m ** 2
#     assert mat_a.x == 3. * u.m
#     assert mat_a.z == 1 / 3. * u.m ** -1
#
#
# def test_state_factory(simple_material):
#     mat_a = simple_material(x=3. * u.m)
#     assert mat_a.x == 3. * u.m
#     assert mat_a.y == 9. * u.m ** 2
#     assert mat_a.z == 1 / 3. * u.m ** -1
#
#
# def test_out_of_range(simple_material):
#     mat_a = simple_material()
#     with pytest.raises(OutOfRangeError):
#         mat_a.x = 12. * u.m
#
#
# def test_dimensionality_error(simple_material):
#     mat_a = simple_material()
#     with pytest.raises(DimensionalityError):
#         mat_a.x = 1. * u.s
#
#
# def test_auto_convert_unit(simple_material):
#     mat_a = simple_material()
#     mat_a.x = 1. * u.ft
#     assert mat_a.x.m == pytest.approx(0.3048)
