from mechmat import ureg
from mechmat.linked import Linked, Guard
from mechmat.principal import crossarrhenius


class CrossArrhenius(Linked):
    r"""
    The model is based on the assumption that the fluid flow obeys the Arrhenius equation for molecular kinetics.

    .. math::

       \eta(T, \dot{\gamma})=\frac{\eta_{0}(T)}{1+(\lambda(T) \dot{\gamma})^{a}}

    where:
        * :math:`\eta_{0}\left(T_{\mathrm{ref}}\right)` zero shear rate viscosity at reference temperature
        * :math:`\lambda\left(T_{\text { ref }}\right)` “relaxation time” at reference temperature
        * :math:`a` “shear-thinning”constant
        * :math:`E_{\mathrm{a}}` Arrhenius activation energy
        * :math:`R` gas constant
        * :math:`T` temperature
        * :math:`T_{ref}` reference temperature

    The input for fully specified state:
        * temperature
        * temperature_cross_arrhenius_ref
        * arrhenius_activation_energy
        * relaxation_time_ref
        * shear_rate
        * shear_thinning_const
        * viscosity_zero_shear_rate_ref
    """

    def __init__(self, **kwargs):
        super(CrossArrhenius, self).__init__(**kwargs)

        self.set_guard('arrhenius_activation_energy', ureg.J / ureg.mol)

        self.set_guard('_arrhenius', ureg.dimensionality)
        self.link_attr('_arrhenius', crossarrhenius.arrhenius, temperature='temperature',
                       arrhenius_activation_energy='arrhenius_activation_energy',
                       temperature_ref='temperature_cross_arrhenius_ref')

        self.set_guard('relaxation_time', ureg.s)
        self.link_attr('relaxation_time', crossarrhenius.relaxation_time, relaxation_time_ref='relaxation_time_ref',
                       zero_shear_viscosity_ref='viscosity_zero_shear_rate_ref')

        self.set_guard('relaxation_time_ref', ureg.s)
        self.set_guard('viscosity_dynamic', ureg.Pa * ureg.s)
        self.link_attr('viscosity_dynamic', crossarrhenius.viscosity_dynamic, shear_rate='shear_rate',
                       zero_shear_viscosity='viscosity_zero_shear_rate', relaxation_time='relaxation_time',
                       shear_thinning_const='shear_thinning_const')

        self.set_guard('viscosity_zero_shear_rate', ureg.Pa * ureg.s)
        self.link_attr('viscosity_zero_shear_rate', crossarrhenius.zero_shear_viscosity, arrhenius='_arrhenius',
                       zero_shear_viscosity_ref='viscosity_zero_shear_rate_ref')

        self.set_guard('viscosity_zero_shear_rate_ref', ureg.Pa * ureg.s)
        self.set_guard('shear_rate', ureg.s ** -1)
        self.set_guard('shear_thinning_const', ureg.dimensionless)
        self.set_guard('temperature', ureg.degC)
        self.set_guard('temperature_cross_arrhenius_ref', ureg.degC)

    arrhenius_activation_energy = Guard()

    _arrhenius = Guard()

    relaxation_time = Guard()

    relaxation_time_ref = Guard()

    viscosity_dynamic = Guard()

    viscosity_zero_shear_rate = Guard()

    viscosity_zero_shear_rate_ref = Guard()

    shear_rate = Guard()

    shear_thinning_const = Guard()

    temperature = Guard()

    temperature_cross_arrhenius_ref = Guard()
