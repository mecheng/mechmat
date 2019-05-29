from mechcite import cite
from mechmat import ureg
from mechmat.core.chainable import Chainable, Guarded
from mechmat.principal import twodomaintaitpvt

class TwoDomainTaitpvT(Chainable):
    r"""
    The modified 2-domain Tait pvT model is used to determine the density of the material as a function of the temperature and pressure. This variation impacts on many aspects of the flow simulation.

    The 2-domain Tait pvT model is given by the following equations:

    .. math::

       v(T, p)=v_{0}(T)\left[1-C \ln \left(1+\frac{p}{B(T)}\right)\right]+v_{t}(T, p)

    where:
        * :math:`v(T, p)` is the specific geometry at temperature and pressure
        * :math:`v_0` is the specific geometry at zero gauge pressure
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

    @cite('osswald_polymer_2006')
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

        self.link_attr('specific_volume', twodomaintaitpvt.get_specific_volume, p='pressure',
                       v_0='specific_volume_zero_gauge_pressure', v_t='specific_volume_transition_temperature', B='_B')

        self.set_guard('temperature_transition', ureg.degC)
        self.link_attr('temperature_transition', twodomaintaitpvt.get_T_t, p='pressure', b_5='b_5', b_6='b_6')


    _B = Guarded()

    b_1s = Guarded()

    b_1m = Guarded()

    _b_1 = Guarded()

    b_2s = Guarded()

    b_2m = Guarded()

    _b_2 = Guarded()

    b_3m = Guarded()

    b_3s = Guarded()

    _b_3 = Guarded()

    b_4m = Guarded()

    b_4s = Guarded()

    _b_4 = Guarded()

    b_5 = Guarded()

    b_6 = Guarded()

    b_7 = Guarded()

    b_8 = Guarded()

    b_9 = Guarded()

    specific_volume_zero_gauge_pressure = Guarded()

    specific_volume_transition_temperature = Guarded()

    temperature_transition = Guarded()

