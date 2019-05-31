from mechmat import ureg
from mechmat.properties.specific_volume import TwoDomainTaitpvT
from mechmat.properties.viscosity import CrossWLF
from mechmat.properties.thermal.polymer import ThermalPolymer
from mechcite import cite


class Polycarbonate_CrossWLF(ThermalPolymer, CrossWLF):
    def __init__(self, **kwargs):
        super(Polycarbonate_CrossWLF, self).__init__(**kwargs)

        osswald_polymer_2015 = cite('osswald_polymer_2015')
        osswald_materials_2012 = cite('osswald_materials_2012')

        self.n = osswald_polymer_2015(0.116 * ureg.dimensionless)
        self.D_1 = osswald_polymer_2015(462. * ureg.Pa * ureg.s)
        self.D_2 = osswald_polymer_2015(573. * ureg.K)
        self.D_3 = osswald_polymer_2015(0. * ureg.K / ureg.Pa)
        self.A_1 = osswald_polymer_2015(8.4 * ureg.dimensionless)
        self.A_2 = osswald_polymer_2015(246.8 * ureg.K)

        self.specific_heat_capacity = osswald_materials_2012(1.26 * ureg.kJ / (ureg.kg * ureg.K))
        self.thermal_conductivity = osswald_materials_2012(0.2 * ureg.W / (ureg.m * ureg.K))
        self.thermal_expansion_coeff = osswald_materials_2012(65. * ureg.um / (ureg.m * ureg.K))
        self.thermal_diffusivity = osswald_materials_2012(1.47 * ureg.m**2 / ureg.s)

        self.viscosity_dynamic = self.viscosity_dynamic


class PolystyreneCrossWLF(ThermalPolymer, CrossWLF):
    def __init__(self, **kwargs):
        super(PolystyreneCrossWLF, self).__init__(**kwargs)

        osswald_polymer_2015 = cite('osswald_polymer_2015')
        osswald_materials_2012 = cite('osswald_materials_2012')

        self.n = osswald_polymer_2015(0.243 * ureg.dimensionless)
        self.D_1 = osswald_polymer_2015(1223. * ureg.Pa * ureg.s)
        self.D_2 = osswald_polymer_2015(503. * ureg.K)
        self.D_3 = osswald_polymer_2015(0. * ureg.K / ureg.Pa)
        self.A_1 = osswald_polymer_2015(6.5 * ureg.dimensionless)
        self.A_2 = osswald_polymer_2015(158.2 * ureg.K)

        self.specific_heat_capacity = osswald_materials_2012(1.34 * ureg.kJ / (ureg.kg * ureg.K))
        self.thermal_conductivity = osswald_materials_2012(0.15 * ureg.W / (ureg.m * ureg.K))
        self.thermal_expansion_coeff = osswald_materials_2012(80. * ureg.um / (ureg.m * ureg.K))
        self.thermal_diffusivity = osswald_materials_2012(0.6 * ureg.m**2 / ureg.s)

        self.viscosity_dynamic = self.viscosity_dynamic


class Polyamide66CrossWLF(ThermalPolymer, CrossWLF):
    def __init__(self, **kwargs):
        super(Polyamide66CrossWLF, self).__init__(**kwargs)

        osswald_polymer_2015 = cite('osswald_polymer_2015')
        osswald_materials_2012 = cite('osswald_materials_2012')

        self.n = osswald_polymer_2015(0.347 * ureg.dimensionless)
        self.D_1 = osswald_polymer_2015(144. * ureg.Pa * ureg.s)
        self.D_2 = osswald_polymer_2015(573. * ureg.K)
        self.D_3 = osswald_polymer_2015(0. * ureg.K / ureg.Pa)
        self.A_1 = osswald_polymer_2015(256999.6 * ureg.dimensionless)
        self.A_2 = osswald_polymer_2015(11235949 * ureg.K)

        self.specific_heat_capacity = osswald_materials_2012(1.67 * ureg.kJ / (ureg.kg * ureg.K))
        self.thermal_conductivity = osswald_materials_2012(0.24 * ureg.W / (ureg.m * ureg.K))
        self.thermal_expansion_coeff = osswald_materials_2012(90. * ureg.um / (ureg.m * ureg.K))
        self.thermal_diffusivity = osswald_materials_2012(1.01 * ureg.m**2 / ureg.s)

        self.viscosity_dynamic = self.viscosity_dynamic


class PolypropyleneCrossWLF(ThermalPolymer, CrossWLF):
    def __init__(self, **kwargs):
        super(PolypropyleneCrossWLF, self).__init__(**kwargs)

        osswald_polymer_2015 = cite('osswald_polymer_2015')
        osswald_materials_2012 = cite('osswald_materials_2012')

        self.n = osswald_polymer_2015(0.251 * ureg.dimensionless)
        self.D_1 = osswald_polymer_2015(564. * ureg.Pa * ureg.s)
        self.D_2 = osswald_polymer_2015(493. * ureg.K)
        self.D_3 = osswald_polymer_2015(0. * ureg.K / ureg.Pa)
        self.A_1 = osswald_polymer_2015(2803.3 * ureg.dimensionless)
        self.A_2 = osswald_polymer_2015(165097.1 * ureg.K)

        self.specific_heat_capacity = osswald_materials_2012(1.93 * ureg.kJ / (ureg.kg * ureg.K))
        self.thermal_conductivity = osswald_materials_2012(0.24 * ureg.W / (ureg.m * ureg.K))
        self.thermal_expansion_coeff = osswald_materials_2012(100. * ureg.um / (ureg.m * ureg.K))
        self.thermal_diffusivity = osswald_materials_2012(0.65 * ureg.m**2 / ureg.s)

        self.viscosity_dynamic = self.viscosity_dynamic


class PolyLacticAcid(ThermalPolymer, CrossWLF, TwoDomainTaitpvT):
    def __init__(self, **kwargs):
        super(PolyLacticAcid, self).__init__(**kwargs)

        oliaei_warpage_2016 = cite('oliaei_warpage_2016')
        self.n = oliaei_warpage_2016(0.01 * ureg.dimensionless)
        self.A_1 = oliaei_warpage_2016(36.10003 * ureg.dimensionless)
        self.A_2 = oliaei_warpage_2016(1.094729 * ureg.K)
        self.D_1 = oliaei_warpage_2016(7.63e+16 * ureg.Pa * ureg.s)
        self.D_2 = oliaei_warpage_2016(432.0627 * ureg.K)
        self.D_3 = oliaei_warpage_2016(0. * ureg.K / ureg.Pa)
        self.tau_star = oliaei_warpage_2016(20402.61 * ureg.Pa)

        self.b_5 = oliaei_warpage_2016(361.26 * ureg.K)
        self.b_6 = oliaei_warpage_2016(7.5e-8 * ureg.K / ureg.Pa)
        self.b_1m = oliaei_warpage_2016(0.000827 * ureg.m ** 3 / ureg.kg)
        self.b_2m = oliaei_warpage_2016(8.5e-7 * ureg.m ** 3 / (ureg.kg * ureg.K))
        self.b_3m = oliaei_warpage_2016(1.63e+8 * ureg.Pa)
        self.b_4m = oliaei_warpage_2016(0.006196 * ureg.K ** -1)
        self.b_1s = oliaei_warpage_2016(0.000821 * ureg.m ** 3 / ureg.kg)
        self.b_2s = oliaei_warpage_2016(4.47e-7 * ureg.m ** 3 / (ureg.kg * ureg.K))
        self.b_3s = oliaei_warpage_2016(2.14e8 * ureg.Pa)
        self.b_4s = oliaei_warpage_2016(0.006078 * ureg.K ** -1)
        self.b_7 = oliaei_warpage_2016(0. * ureg.m ** 3 / ureg.kg)
        self.b_8 = oliaei_warpage_2016(0. * ureg.K ** -1)
        self.b_9 = oliaei_warpage_2016(0. * ureg.Pa ** -1)

        self.specific_volume = self.specific_volume
        self.viscosity_dynamic = self.viscosity_dynamic


class PolyLacticAcidThermoplasticPolyUrethane(ThermalPolymer, CrossWLF, TwoDomainTaitpvT):
    def __init__(self, **kwargs):
        super(PolyLacticAcidThermoplasticPolyUrethane, self).__init__(**kwargs)

        oliaei_warpage_2016 = cite('oliaei_warpage_2016')
        self.n = oliaei_warpage_2016(0.301358 * ureg.dimensionless)
        self.A_1 = oliaei_warpage_2016(1398.752 * ureg.dimensionless)
        self.A_2 = oliaei_warpage_2016(15375.78 * ureg.K)
        self.D_1 = oliaei_warpage_2016(4.05e+15 * ureg.Pa * ureg.s)
        self.D_2 = oliaei_warpage_2016(145.6926 * ureg.K)
        self.D_3 = oliaei_warpage_2016(0. * ureg.K / ureg.Pa)
        self.tau_star = oliaei_warpage_2016(27135.87 * ureg.Pa)

        self.b_5 = oliaei_warpage_2016(462. * ureg.K)
        self.b_6 = oliaei_warpage_2016(8e-8 * ureg.K / ureg.Pa)
        self.b_1m = oliaei_warpage_2016(0.0008413 * ureg.m ** 3 / ureg.kg)
        self.b_2m = oliaei_warpage_2016(6.38e-7 * ureg.m ** 3 / (ureg.kg * ureg.K))
        self.b_3m = oliaei_warpage_2016(1.85e+8 * ureg.Pa)
        self.b_4m = oliaei_warpage_2016(0.003812 * ureg.K ** -1)
        self.b_1s = oliaei_warpage_2016(0.00087 * ureg.m ** 3 / ureg.kg)
        self.b_2s = oliaei_warpage_2016(5.14e-7 * ureg.m ** 3 / (ureg.kg * ureg.K))
        self.b_3s = oliaei_warpage_2016(2.0e8 * ureg.Pa)
        self.b_4s = oliaei_warpage_2016(0.003398 * ureg.K ** -1)
        self.b_7 = oliaei_warpage_2016(0. * ureg.m ** 3 / ureg.kg)
        self.b_8 = oliaei_warpage_2016(0. * ureg.K ** -1)
        self.b_9 = oliaei_warpage_2016(0. * ureg.Pa ** -1)

        self.specific_volume = self.specific_volume
        self.viscosity_dynamic = self.viscosity_dynamic


class PolyLacticAcidThermoplasticStarch(ThermalPolymer, CrossWLF, TwoDomainTaitpvT):
    def __init__(self, **kwargs):
        super(PolyLacticAcidThermoplasticStarch, self).__init__(**kwargs)

        oliaei_warpage_2016 = cite('oliaei_warpage_2016')
        self.n = oliaei_warpage_2016(0.607351 * ureg.dimensionless)
        self.A_1 = oliaei_warpage_2016(36.65705 * ureg.dimensionless)
        self.A_2 = oliaei_warpage_2016(11.57926 * ureg.K)
        self.D_1 = oliaei_warpage_2016(9.2e+16 * ureg.Pa * ureg.s)
        self.D_2 = oliaei_warpage_2016(395.1525 * ureg.K)
        self.D_3 = oliaei_warpage_2016(0. * ureg.K / ureg.Pa)
        self.tau_star = oliaei_warpage_2016(160.5206 * ureg.Pa)

        self.b_5 = oliaei_warpage_2016(367.15 * ureg.K)
        self.b_6 = oliaei_warpage_2016(1.05e-7 * ureg.K / ureg.Pa)
        self.b_1m = oliaei_warpage_2016(0.000844 * ureg.m ** 3 / ureg.kg)
        self.b_2m = oliaei_warpage_2016(7.25e-7 * ureg.m ** 3 / (ureg.kg * ureg.K))
        self.b_3m = oliaei_warpage_2016(1.85e+8 * ureg.Pa)
        self.b_4m = oliaei_warpage_2016(0.005837 * ureg.K ** -1)
        self.b_1s = oliaei_warpage_2016(0.000838 * ureg.m ** 3 / ureg.kg)
        self.b_2s = oliaei_warpage_2016(3.29e-7 * ureg.m ** 3 / (ureg.kg * ureg.K))
        self.b_3s = oliaei_warpage_2016(2.45e8 * ureg.Pa)
        self.b_4s = oliaei_warpage_2016(0.005153 * ureg.K ** -1)
        self.b_7 = oliaei_warpage_2016(0. * ureg.m ** 3 / ureg.kg)
        self.b_8 = oliaei_warpage_2016(0. * ureg.K ** -1)
        self.b_9 = oliaei_warpage_2016(0. * ureg.Pa ** -1)

        self.specific_volume = self.specific_volume
        self.viscosity_dynamic = self.viscosity_dynamic
