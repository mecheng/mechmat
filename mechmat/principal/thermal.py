

def thermal_diffusivity(thermal_conductivity, specific_heat_capacity, density):
    r"""
    The rate of transfer of heat of a material from the hot end to the cold end.

    .. math:

       \alpha = \frac{k}{\rho c_p}

    Args:
        thermal_conductivity: :math:`k`
        specific_heat_capacity: :math:`c_p`
        density: :math:`\rho`

    Returns:

    """
    return thermal_conductivity / (density * specific_heat_capacity)
