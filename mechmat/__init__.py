# -*- coding: utf-8 -*-

"""Top-level package for mechmat."""

__author__ = """Jelle Spijker"""
__email__ = 'spijker.jelle@gmail.com'
__version__ = '0.1.0'

from pint import UnitRegistry, set_application_registry

ureg = UnitRegistry()
Q_ = ureg.Quantity
set_application_registry(ureg)
