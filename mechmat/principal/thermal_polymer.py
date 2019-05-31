from mechcite import cite


@cite('osswald_materials_2012')
def temperature_glass(temperature_melt):
    return 2 / 3 * temperature_melt


@cite('osswald_materials_2012')
def temperature_melt(temperature_glass):
    return 3 / 2 * temperature_glass
