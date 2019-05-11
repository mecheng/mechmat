#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `mechmat` package."""

import pytest

from mechmat import ureg as u


@pytest.fixture
def simple_material():
    from mechmat.material import Material
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

        x = Linked('m', linked_properties={get_x: {'y_var': 'y'}})

        y = Linked('m**2', linked_properties={get_y: {'x_var': 'x'}})

        z = Linked('m**-1', linked_properties={get_z: {'x_var': 'x',
                                                       'y_var': 'y'}})

    SimpleMat = Simple()
    SimpleMat.x = 2. * u.m

    return SimpleMat


def test_state(simple_material):
    assert simple_material.x == 2. * u.m
    assert simple_material.y == 4. * u.m ** 2
    assert simple_material.z == 0.5 * u.m ** -1


def test_mod_state(simple_material):
    simple_material.y = 9. * u.m ** 2
    assert simple_material.y == 9. * u.m ** 2
    assert simple_material.x == 3. * u.m
    assert simple_material.z == 1 / 3. * u.m ** -1


def test_state_factory(simple_material):
    mat_A = simple_material(x=3. * u.m)
    assert mat_A.x == 3. * u.m
    assert mat_A.y == 9. * u.m ** 2
    assert mat_A.z == 1 / 3. * u.m ** -1
