from mechmat.core.chainable import Chainable, Guarded
from mechmat.principal import core, thermal
from mechmat import ureg


class ThermalConductivity(Chainable):
    def __init__(self, **kwargs):
        super(ThermalConductivity, self).__init__(**kwargs)

        self.set_guard('thermal_conductivity', ureg.W / (ureg.m * ureg.K))
        self.link_attr('thermal_conductivity', core.reciprocal, value='thermal_conductivity')

        self.set_guard('thermal_resistivity', ureg.m * ureg.K / ureg.W)
        self.link_attr('thermal_resistivity', core.reciprocal, value='thermal_conductivity')

        self.set_guard('thermal_conductance', ureg.W / ureg.K)
        self.link_attr('thermal_conductance', core.reciprocal, value='thermal_resistance')

        self.set_guard('thermal_resistance', ureg.K / ureg.W)
        self.link_attr('thermal_resistance', core.reciprocal, value='thermal_conductance')

        self.set_guard('heat_transfer_coeff', ureg.W / (ureg.K * ureg.m ** -2))
        self.link_attr('heat_transfer_coeff', core.reciprocal, value='thermal_insulance')

        self.set_guard('thermal_insulance', ureg.K * ureg.m ** 2 / ureg.W)
        self.link_attr('thermal_insulance', core.reciprocal, value='heat_transfer_coeff')

        self.set_guard('thermal_diffusivity', ureg.m ** 2 / ureg.s)
        self.link_attr('thermal_diffusivity', thermal.thermal_diffusivity, thermal_conductivity='thermal_conductivity',
                       density='density', specific_heat_capacity='specific_heat_capacity')

        self.set_guard('thermal_transmittance_convection', ureg.K * ureg.m ** 2 / ureg.W)

        self.set_guard('thermal_transmittance_radiation', ureg.K * ureg.m ** 2 / ureg.W)

    thermal_conductivity = Guarded()

    thermal_resistivity = Guarded()

    thermal_conductance = Guarded()

    thermal_resistance = Guarded()

    heat_transfer_coeff = Guarded()

    thermal_insulance = Guarded()

    thermal_diffusivity = Guarded()

    thermal_transmittance_convection = Guarded()

    thermal_transmittance_radiation = Guarded()
