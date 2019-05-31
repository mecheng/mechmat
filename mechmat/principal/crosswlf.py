from mechmat import ureg
from mechcite import cite
from numpy import e


@cite('osswald_polymer_2015')
def viscosity_dynamic(shear_rate, tau_star, zero_shear_viscosity, n):
    r"""
    This 6-parameter model considers the effects of shear rate and temperature on the viscosity. Similar to the Bird-Carreau model,
    this model describes both Newtonian and shear thinning behavior. The shear thinning part is modeled by the general Cross equation,\
    which is a popular and earlier alternative to the Bird-Carreau-Yasuda model:

    Args:
        shear_rate: Shear rate :math:`\dot{\gamma}` in :math:`[s^{-1}]`
        tau_star: is the critical shear stress :math:`\tau^{*}`  at the transition from the Newtonian plateau
        zero_shear_viscosity: is the zero shear rate viscosity :math:`\eta_0` in :math:`[Pa s]`
        n: The power law index :math:`n` in :math:`[-]`

    Returns:

    """
    K = zero_shear_viscosity / tau_star
    K *= shear_rate
    return zero_shear_viscosity / (1. + K ** (1. - n))


@cite('osswald_polymer_2015')
def critical_shear_stress(n):
    r"""
    Here, :math:`\tau^{*}` is the critical shear stress at the transition from the Newtonian plateau, and n is the Power Law index

    .. math::

       \tau^{*}=\left(\frac{4 n}{3 n+1}\right)^{\frac{n}{1-n}}

    Args:
        n: The power law index :math:`n` in :math:`[-]`

    Returns:
        The critical shear stress
    """
    tau_star = 4. * n
    tau_star /= 3. * n + 1
    return tau_star ** (n / (1. - n)) * ureg.Pa


@cite('osswald_polymer_2015')
def zero_shear_viscosity(temperature, D_1, temperature_glass_transition, A_1, A_2):
    r"""
    The zero shear viscosity is modeled with the WLF equation, given by:

    .. math::

       \eta_{0}(T)=D_{1} \cdot \exp \left[-\frac{A_{1}\left(T-D_{2}\right)}{A_{2}+T-D_{2}}\right]

    Args:
        temperature: The temperature :math:`T` in :math:`[C^{\circ}]`
        D_1: The viscosity at reference temperature :math:`D_1` in :math:`[Pa s]`
        temperature_glass_transition: The reference temperature :math:`D_2` in :math:`[C^{\circ}]`
        A_1: Temperature dependency shift factor :math:`A_1` in :math:`[-]`
        A_2: Temperature dependency shift factor :math:`A_1` in :math:`[-]`

    Returns:
        zero shear viscosity :math:`\eta_0` in :math:`[Pa s]`
    """
    shift = A_1 * (temperature.to('K') - temperature_glass_transition)
    shift /= A_2 + temperature.to('K') - temperature_glass_transition
    return D_1 * e ** (- shift)


@cite('osswald_polymer_2015')
def glass_transition_temperature(D_2, D_3, p):
    return D_2 + D_3 * p
