from math import inf

from mechmat import ureg
from mechmat.linked import Linked, Guard
from mechmat.principal import specific_weight, density, specific_volume, twodomaintaitpvt

__all__ = ['Material', 'TwoDomainTaitpvT']


class Material(Linked):
    def __init__(self, **kwargs):
        super(Material, self).__init__(**kwargs)

        self.set_guard('density', ureg.kg / ureg.m ** 3, [0., inf])
        self.link_attr('density', density.from_specific_volume, specific_volume='specific_volume')
        self.link_attr('density', density.from_specific_weight, specific_weight='specific_weight')

        self.set_guard('specific_volume', ureg.m ** 3 / ureg.kg, [0., inf])
        self.link_attr('specific_volume', specific_volume.from_density, density='density')

        self.set_guard('specific_weight', ureg.N / ureg.m ** 3, [0., inf])
        self.link_attr('specific_weight', specific_weight.from_density, density='density')

        self.set_guard('specific_heat', ureg.J / (ureg.kg / ureg.K), [0., inf])

        self.set_guard('pressure', ureg.Pa, [0., inf])

        self.set_guard('temperature', ureg.degC, [-273.15, inf])

        self.set_guard('enthalpie', ureg.J, [0., inf])

        self.set_guard('molar_weight', ureg.kg / ureg.mol, [0., inf])

        self.set_guard('mass', ureg.kg, [0., inf])

        self.set_guard('mass_flow', ureg.kg / ureg.s)

        self.set_guard('volume', ureg.m ** 3, [0., inf])

        self.set_guard('volume_flow')

        self.set_guard('dt', ureg.s)

        self._logistic_properties += ['name', 'short_name', 'CAS', 'category']

    _version = 1
    """int: version of the material class. Bump this value up for big changes in the class which aren't compatible with 
        earlier release. """

    category = None
    r""":class:`~Category` The Material category"""

    name = None
    r"""str: The common name of the material"""

    CAS = None
    r"""str: Chemical Abstracts Service number"""

    @property
    def short_name(self):
        r"""
        str: Short name for the material. When it is not user specified, the :attr:`~name` is used. When this consists
        of multiple words, the short name is build from all first letters. When the name consist of a single word, the
        first two letters are used """
        if hasattr(self, '_short_name'):
            return self._short_name
        else:
            if self.name is None:
                return None
            words = self.name.split(' ')
            if len(words) > 1:
                return ''.join([w[0] for w in words])
            return self.name[:2]

    @short_name.setter
    def short_name(self, value):
        self._short_name = value

    def __repr__(self):
        state = {}
        for prop in self._logistic_properties:
            if getattr(self, prop) is not None:
                state[prop] = getattr(self, prop)
        for prop in self._state:
            if getattr(self, prop) is not None:
                state[prop] = getattr(self, prop)
        return '{} with state {}>'.format(str(type(self))[:-2], state)

    density = Guard()

    specific_volume = Guard()

    specific_weight = Guard()

    specific_heat = Guard()

    pressure = Guard()

    temperature = Guard()

    enthalpie = Guard()

    molar_weight = Guard()

    mass = Guard()

    mass_flow = Guard()

    volume = Guard()

    volume_flow = Guard()

    dt = Guard()


class TwoDomainTaitpvT(Linked):
    r"""
    The modified 2-domain Tait pvT model is used to determine the density of the material as a function of the temperature and pressure. This variation impacts on many aspects of the flow simulation.

    The 2-domain Tait pvT model is given by the following equations:

    .. math::

       v(T, p)=v_{0}(T)\left[1-C \ln \left(1+\frac{p}{B(T)}\right)\right]+v_{t}(T, p)

    where:
        * :math:`v(T, p)` is the specific volume at temperature and pressure
        * :math:`v_0` is the specific volume at zero gauge pressure
        * :math:`T` is the temperature
        * :math:`p` is the pressure
        * :math:`C` is a constant
        * :math:`B` accounts for the pressure sensitivity of the material

    The input for fully specified state:
        * b_1s
        * b_1m
        * b_2s
        * b_2m
        * b_3s
        * b_3m
        * b_4s
        * b_4m
        * b_5
        * b_6
        * b_7
        * b_8
        * b_9
        * temperature
        * pressure
    """

    def __init__(self, **kwargs):
        super(TwoDomainTaitpvT, self).__init__(**kwargs)
        self.temperature_transition = self.temperature_transition  # need for initialization of material state

        self.set_guard('_B', ureg.Pa)
        self.link_attr('_B', twodomaintaitpvt.get_B, T='temperature', b_3='_b_3', b_4='_b_4', b_5='b_5')

        self.set_guard('b_1s', ureg.m ** 3 / ureg.kg)
        self.set_guard('b_1m', ureg.m ** 3 / ureg.kg)
        self.set_guard('_b_1', ureg.m ** 3 / ureg.kg)
        self.link_attr('_b_1', twodomaintaitpvt.switch_m_s, T='temperature', T_t='temperature_transition', s='b_1s',
                       m='b_1m')

        self.set_guard('b_2s', ureg.m ** 3 / (ureg.kg * ureg.K))
        self.set_guard('b_2m', ureg.m ** 3 / (ureg.kg * ureg.K))
        self.set_guard('_b_2', ureg.m ** 3 / (ureg.kg * ureg.K))
        self.link_attr('_b_2', twodomaintaitpvt.switch_m_s, T='temperature', T_t='temperature_transition', s='b_2s',
                       m='b_2m')

        self.set_guard('b_3s', ureg.Pa)
        self.set_guard('b_3m', ureg.Pa)
        self.set_guard('_b_3', ureg.Pa)
        self.link_attr('_b_3', twodomaintaitpvt.switch_m_s, T='temperature', T_t='temperature_transition', s='b_3s',
                       m='b_3m')

        self.set_guard('b_4s', ureg.K ** -1)
        self.set_guard('b_4m', ureg.K ** -1)
        self.set_guard('_b_4', ureg.K ** -1)
        self.link_attr('_b_4', twodomaintaitpvt.switch_m_s, T='temperature', T_t='temperature_transition', s='b_4s',
                       m='b_4m')

        self.set_guard('b_5', ureg.K)
        self.set_guard('b_6', ureg.K / ureg.Pa)
        self.set_guard('b_7', ureg.m ** 3 / ureg.kg)
        self.set_guard('b_8', ureg.K ** -1)
        self.set_guard('b_9', ureg.Pa ** -1)

        self.set_guard('specific_volume_zero_gauge_pressure', ureg.m ** 3 / ureg.kg)
        self.link_attr('specific_volume_zero_gauge_pressure', twodomaintaitpvt.get_v_0, T='temperature', b_1='_b_1',
                       b_2='_b_2', b_5='b_5')

        self.set_guard('specific_volume_transition_temperature', ureg.m ** 3 / ureg.kg)
        self.link_attr('specific_volume_transition_temperature', twodomaintaitpvt.get_v_t, p='pressure',
                       T='temperature', T_t='temperature_transition', b_5='b_5', b_7='b_7', b_8='b_8', b_9='b_9')

        self.set_guard('specific_volume', ureg.m ** 3 / ureg.kg)
        self.link_attr('specific_volume', twodomaintaitpvt.get_specific_volume, p='pressure',
                       v_0='specific_volume_zero_gauge_pressure', v_t='specific_volume_transition_temperature', B='_B')

        self.set_guard('temperature', ureg.degC)

        self.set_guard('temperature_transition', ureg.degC)
        self.link_attr('temperature_transition', twodomaintaitpvt.get_T_t, p='pressure', b_5='b_5', b_6='b_6')

        self.set_guard('pressure', ureg.Pa)

    _B = Guard()

    b_1s = Guard()

    b_1m = Guard()

    _b_1 = Guard()

    b_2s = Guard()

    b_2m = Guard()

    _b_2 = Guard()

    b_3m = Guard()

    b_3s = Guard()

    _b_3 = Guard()

    b_4m = Guard()

    b_4s = Guard()

    _b_4 = Guard()

    b_5 = Guard()

    b_6 = Guard()

    b_7 = Guard()

    b_8 = Guard()

    b_9 = Guard()

    specific_volume_zero_gauge_pressure = Guard()

    specific_volume_transition_temperature = Guard()

    specific_volume = Guard()

    temperature = Guard()

    temperature_transition = Guard()

    pressure = Guard()
