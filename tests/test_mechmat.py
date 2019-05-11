#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `mechmat` package."""

import pytest

from mechmat import ureg as u
from mechmat.errors import OutOfRangeError
from pint import DimensionalityError


@pytest.fixture
def simple_material():
    from mechmat.material import Material, Category
    from mechmat.linked import Linked

    def get_x(y_var):
        return y_var ** (1 / 2)

    def get_y(x_var):
        return x_var ** 2

    def get_z(x_var, y_var):
        return x_var / y_var

    class Simple(Material):
        def __init__(self):
            super(Simple, self).__init__()
            self.category = Category.FLUID

        x = Linked('m', rng=[0., 10], linked_properties={get_x: {'y_var': 'y'}})

        y = Linked('m**2', linked_properties={get_y: {'x_var': 'x'}})

        z = Linked('m**-1', linked_properties={get_z: {'x_var': 'x',
                                                       'y_var': 'y'}})

    SimpleMat = Simple()
    SimpleMat.x = 2. * u.m

    return SimpleMat


def test_state(simple_material):
    mat_a = simple_material()
    assert mat_a.x == 2. * u.m
    assert mat_a.y == 4. * u.m ** 2
    assert mat_a.z == 0.5 * u.m ** -1


def test_mod_state(simple_material):
    mat_a = simple_material()
    mat_a.y = 9. * u.m ** 2
    assert mat_a.y == 9. * u.m ** 2
    assert mat_a.x == 3. * u.m
    assert mat_a.z == 1 / 3. * u.m ** -1


def test_state_factory(simple_material):
    mat_a = simple_material(x=3. * u.m)
    assert mat_a.x == 3. * u.m
    assert mat_a.y == 9. * u.m ** 2
    assert mat_a.z == 1 / 3. * u.m ** -1


def test_out_of_range(simple_material):
    mat_a = simple_material()
    with pytest.raises(OutOfRangeError):
        mat_a.x = 12. * u.m


def test_dimensionality_error(simple_material):
    mat_a = simple_material()
    with pytest.raises(DimensionalityError):
        mat_a.x = 1. * u.s


def test_auto_convert_unit(simple_material):
    mat_a = simple_material()
    mat_a.x = 1. * u.ft
    assert mat_a.x.m == pytest.approx(0.3048)
