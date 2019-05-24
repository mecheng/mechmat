from mechmat.material import Material
from mechmat.properties.specific_volume import TwoDomainTaitpvT
from mechmat.properties.viscosity import CrossArrhenius


class Polymer(Material):
    def __init__(self, **kwargs):
        super(Polymer, self).__init__(**kwargs)


class PolyActicAcid(Polymer, TwoDomainTaitpvT, CrossArrhenius):
    r"""
Poly(lactic acid) or polylactic acid or polylactide (PLA) is a thermoplastic aliphatic polyester derived from renewable
biomass, typically from fermented plant starch such as from corn, cassava, sugarcane or sugar beet pulp. In 2010, PLA
had the second highest consumption geometry of any bioplastic of the world.

    Sources:
        * `Ultimaker PLA Technical data sheet <https://ultimaker.com/download/74970/UM180821%20TDS%20PLA%20RB%20V11.pdf>`_
        * `Ultimaker PLA Safety data sheet <https://ultimaker.com/download/75095/UM180816%20SDS%20PLA%20RB%20V11.pdf>`_
    """

    def __init__(self, **kwargs):
        super(PolyActicAcid, self).__init__(**kwargs)

        self.CAS = '26100-51-6'
        self.name = 'Polyactic acid'
        self.short_name = 'PLA'
