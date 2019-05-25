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

    mat = material_factory(True,
                           name='simple material',
                           temperature=20. * u.degC,
                           pressure=1. * u.bar,
                           volumeflow=100. * u.mm * 3)

    return mat


def test_state(simple_material):
    mat_a = simple_material(temperature=50. * u.degC)
    assert mat_a.temperature == 50. * u.degC
    assert mat_a.temperature != simple_material.temperature

def test_markdown(simple_material):
    print(simple_material._repr_markdown_())

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
