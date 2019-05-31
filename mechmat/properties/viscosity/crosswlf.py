from mechmat import ureg
from mechmat.core.chainable import Chainable, Guarded
from mechmat.principal import crosswlf
from mechcite import cite
from math import inf


class CrossWLF(Chainable):
    r"""
    This 6-parameter model considers the effects of shear rate and temperature on the viscosity. Similar to the Bird-Carreau model,
    this model describes both Newtonian and shear thinning behavior. The shear thinning part is modeled by the general Cross equation,\
    which is a popular and earlier alternative to the Bird-Carreau-Yasuda model:


    """

    @cite('osswald_polymer_2015')
    def __init__(self, **kwargs):
        super(CrossWLF, self).__init__(**kwargs)

        self.set_guard('A_1', ureg.dimensionless)

        self.set_guard('A_2', ureg.K, [0., inf])

        self.set_guard('D_1', ureg.Pa * ureg.s)

        self.set_guard('D_2', ureg.K)

        self.set_guard('D_3', ureg.K / ureg.Pa)

        self.set_guard('n', ureg.dimensionless)

        self.set_guard('tau_star', ureg.Pa)
        self.link_attr('tau_star', crosswlf.critical_shear_stress, n='n')

        self.link_attr('temperature_glass', crosswlf.glass_transition_temperature, D_2='D_2', D_3='D_3', p='pressure')

        self.link_attr('viscosity_zero_shear_rate', crosswlf.zero_shear_viscosity, temperature='temperature', D_1='D_1',
                       temperature_glass_transition='temperature_glass', A_1='A_1', A_2='A_2')

        self.link_attr('viscosity_dynamic', crosswlf.viscosity_dynamic, shear_rate='shear_rate', tau_star='tau_star', zero_shear_viscosity='viscosity_zero_shear_rate', n='n')

    A_1 = Guarded()

    A_2 = Guarded()

    D_1 = Guarded()

    D_2 = Guarded()

    D_3 = Guarded()

    n = Guarded()

    tau_star = Guarded()

    viscosity_zero_shear_rate = Guarded()
