class Ionic:
    """Ionic radius class. Stores: charge, spin, coordination"""
    def __init__(self, charge=0, coordination="", radius=0.0):
        self.charge = charge
        self.coordination = coordination
        self.radius = radius
        
    def set_radius(self, value: float):
        self.radius = value

class Atom_Data:
    """Atom data class. Stores Radius: covalent; Color: tuple, RGBA values"""

    def __init__(self, radius: float, vanDerWaals=0.00, color=(0.5,0.5,0.5, 1), ionicData=[Ionic()]): # Gray is the default color if none is specified
        self.radius = radius #covalent radius
        self.vanDerWaals = vanDerWaals #default is set temprarilly as 0.00 is radius is not reported
        self.color = color #RGBA values: default is gray
        self.ionicData = ionicData

    def get_radius(self):
        """
        returns: <float> atom's covalent radius
        """
        return self.radius

    def get_color(self):
        """
        returns: <tuple size 4> rgba values for color
        """
        return self.color
    
    def get_vanDerWaals(self):
        """
        returns: vanDerWaals radius for element.
        """
        return self.vanDerWaals
    
    def get_ionicData(self):
        return self.ionicData
    
IonicRadii = { #element symbols, their covalent radii & their RGBA color values
    "Ac": [Ionic(3,"VI",1.12)],
    "Al": [Ionic(3,"IV",0.39),Ionic(3,"V",0.48),Ionic(3,"VI",0.535)],
    "Am": [Ionic(2,"VII",1.21),Ionic(2,"VIII",1.26),Ionic(2,"IX",1.31),Ionic(3,"VI",0.975),Ionic(3,"VIII",1.09),
            Ionic(4,"VI",0.85),Ionic(4,"VIII",0.95)],
    "Sb": [Ionic(3,"IVPY",0.76),Ionic(3,"V",0.8),Ionic(3,"VI",0.76),Ionic(5,"VI",0.6)],
    "Ar": [Ionic()],
    "As": [Ionic(3,"VI",0.58),Ionic(5,"IV",0.335),Ionic(5,"VI",0.46)],
    "At": [Ionic(7,"VI",0.62)],
    "Ba": [Ionic(2,"VI",1.35),Ionic(2,"VII",1.38),Ionic(2,"VIII",1.42),Ionic(2,"IX",1.47),Ionic(2,"X",1.52),Ionic(2,"XI",1.57),
            Ionic(2,"XII",1.61)],
    "Bk": [Ionic(3,"VI",0.96),Ionic(4,"VI",0.83),Ionic(4,"VIII",0.93)],
    "Be": [Ionic(2,"III",0.16),Ionic(2,"IV",0.27),Ionic(2,"VI",0.45)],
    "Bi": [Ionic(3,"V",0.96),Ionic(3,"VI",1.03),Ionic(3,"VIII",1.17),Ionic(5,"VI",0.76)],
    "Bh": [Ionic()],
    "B": [Ionic(3,"III",0.01),Ionic(3,"IV",0.11),Ionic(3,"VI",0.27)],
    "Br": [Ionic(-1,"VI",1.96),Ionic(3,"IVSQ",0.59),Ionic(5,"IIIPY",0.31),Ionic(7,"IV",0.25),Ionic(7,"VI",0.39)],
    "Cd": [Ionic(2,"IV",0.78),Ionic(2,"V",0.87),Ionic(2,"VI",0.95),Ionic(2,"VII",1.03),Ionic(2,"VIII",1.1),Ionic(2,"XII",1.31)],
    "Ca": [Ionic(2,"VI",1),Ionic(2,"VII",1.06),Ionic(2,"VIII",1.12),Ionic(2,"IX",1.18),Ionic(2,"X",1.23),Ionic(2,"XII",1.34)],
    "Cf": [Ionic(3,"VI",0.95),Ionic(4,"VI",0.821),Ionic(4,"VIII",0.92)],
    "C": [Ionic(4,"III",0.08),Ionic(4,"IV",0.15),Ionic(4,"VI",0.16)],
    "Ce": [Ionic(3,"VI",1.01),Ionic(3,"VII",1.07),Ionic(3,"VIII",1.143),Ionic(3,"IX",1.196),Ionic(3,"X",1.25),Ionic(3,"XII",1.34),
            Ionic(4,"VI",0.87),Ionic(4,"VIII",0.97),Ionic(4,"X",1.07),Ionic(4,"XII",1.14)],
    "Cs": [Ionic(1,"VI",1.67),Ionic(1,"VIII",1.74),Ionic(1,"IX",1.78),Ionic(1,"X",1.81),Ionic(1,"XI",1.85),Ionic(1,"XII",1.88)],
    "Cl": [Ionic(-1,"VI",1.81),Ionic(5,"IIIPY",0.12),Ionic(7,"IV",0.08),Ionic(7,"VI",0.27)],
    "Cr": [Ionic(2,"VI-ls",0.73),Ionic(2,"0-hs",0.8),Ionic(3,"VI",0.615),Ionic(4,"IV",0.41),Ionic(4,"VI",0.55),
            Ionic(5,"IV",0.345),Ionic(5,"VI",0.49),Ionic(5,"VIII",0.57),Ionic(6,"IV",0.26),Ionic(6,"VI",0.44)],
    "Co": [Ionic(2,"IV-hs",0.58),Ionic(2,"V",0.67),Ionic(2,"VI-ls",0.65),Ionic(2,"0-hs",0.745),Ionic(2,"VIII",0.9),
            Ionic(3,"VI-ls",0.545),Ionic(3,"0-hs",0.61),Ionic(4,"IV",0.4),Ionic(4,"VI-hs",0.53)],
    "Cn": [Ionic()],
    "Cu": [Ionic(1,"II",0.46),Ionic(1,"IV",0.6),Ionic(1,"VI",0.77),Ionic(2,"IV",0.57),Ionic(2,"IVSQ",0.57),Ionic(2,"V",0.65),
            Ionic(2,"VI",0.73),Ionic(3,"VI-ls",0.54)],
    "Cm": [Ionic(3,"VI",0.97),Ionic(4,"VI",0.85),Ionic(4,"VIII",0.95)],
    "Ds": [Ionic()],
    "Db": [Ionic()],
    "Dy": [Ionic(2,"VI",1.07),Ionic(2,"VII",1.13),Ionic(2,"VIII",1.19),Ionic(3,"VI",0.912),Ionic(3,"VII",0.97),Ionic(3,"VIII",1.027),
            Ionic(3,"IX",1.083)],
    "Es": [Ionic()],
    "Er": [Ionic(3,"VI",0.89),Ionic(3,"VII",0.945),Ionic(3,"VIII",1.004),Ionic(3,"IX",1.062)],
    "Eu": [Ionic(2,"VI",1.17),Ionic(2,"VII",1.2),Ionic(2,"VIII",1.25),Ionic(2,"IX",1.3),Ionic(2,"X",1.35),Ionic(3,"VI",0.947),
            Ionic(3,"VII",1.01),Ionic(3,"VIII",1.066),Ionic(3,"IX",1.12)],
    "Fm": [Ionic()],
    "Fl": [Ionic()],
    "F": [Ionic(-1,"II",1.285),Ionic(-1,"III",1.3),Ionic(-1,"IV",1.31),Ionic(-1,"VI",1.33),Ionic(7,"VI",0.08)],
    "Fr": [Ionic(1,"VI",1.8)],
    "Gd": [Ionic(3,"VI",0.938),Ionic(3,"VII",1),Ionic(3,"VIII",1.053),Ionic(3,"IX",1.107)],
    "Ga": [Ionic(3,"IV",0.47),Ionic(3,"V",0.55),Ionic(3,"VI",0.62)],
    "Ge": [Ionic(2,"VI",0.73),Ionic(4,"IV",0.39),Ionic(4,"VI",0.53)],
    "Au": [Ionic(1,"VI",1.37),Ionic(3,"IVSQ",0.68),Ionic(3,"VI",0.85),Ionic(5,"VI",0.57)],
    "Hf": [Ionic(4,"IV",0.58),Ionic(4,"VI",0.71),Ionic(4,"VII",0.76),Ionic(4,"VIII",0.83)],
    "Hs": [Ionic()],
    "He": [Ionic()],
    "Ho": [Ionic(3,"VI",0.901),Ionic(3,"VIII",1.015),Ionic(3,"IX",1.072),Ionic(3,"X",1.12)],
    "H": [Ionic(1,"I",0.38),Ionic(1,"II",0.18)],
    "In": [Ionic(3,"IV",0.62),Ionic(3,"VI",0.8),Ionic(3,"VIII",0.92)],
    "I": [Ionic(-1,"VI",2.2),Ionic(5,"IIIPY",0.44),Ionic(5,"VI",0.95),Ionic(7,"IV",0.42),Ionic(7,"VI",0.53)],
    "Ir": [Ionic(3,"VI",0.68),Ionic(4,"VI",0.625),Ionic(5,"VI",0.57)],
    "Fe": [Ionic(2,"IV-hs",0.63),Ionic(2,"IVSQ-hs",0.64),Ionic(2,"VI-ls",0.61),Ionic(2,"0-hs",0.78),
            Ionic(2,"VIII-hs",0.92),Ionic(3,"IV-hs",0.49),Ionic(3,"V",0.58),Ionic(3,"VI-ls",0.55),
            Ionic(3,"0-hs",0.645),Ionic(3,"VIII-hs",0.78),Ionic(4,"VI",0.585),Ionic(6,"IV",0.25)],
    "Kr": [Ionic()],
    "La": [Ionic(3,"VI",1.032),Ionic(3,"VII",1.1),Ionic(3,"VIII",1.16),Ionic(3,"IX",1.216),Ionic(3,"X",1.27),Ionic(3,"XII",1.36)],
    "Lr": [Ionic()],
    "Pb": [Ionic(2,"IVPY",0.98),Ionic(2,"VI",1.19),Ionic(2,"VII",1.23),Ionic(2,"VIII",1.29),Ionic(2,"IX",1.35),
            Ionic(2,"X",1.4),Ionic(2,"XI",1.45),Ionic(2,"XII",1.49),Ionic(4,"IV",0.65),Ionic(4,"V",0.73),Ionic(4,"VI",0.775),
            Ionic(4,"VIII",0.94)],
    "Li": [Ionic(1,"IV",0.59),Ionic(1,"VI",0.76),Ionic(1,"VIII",0.92)],
    "Lv": [Ionic()],
    "Lu": [Ionic(3,"VI",0.861),Ionic(3,"VIII",0.977),Ionic(3,"IX",1.032)],
    "Mg": [Ionic(2,"IV",0.57),Ionic(2,"V",0.66),Ionic(2,"VI",0.72),Ionic(2,"VIII",0.89)],
    "Mn": [Ionic(2,"IV-hs",0.66),Ionic(2,"V-hs",0.75),Ionic(2,"VI-hs",0.83),Ionic(2,"0-ls",0.67),
            Ionic(2,"VII-hs",0.9),Ionic(2,"VIII",0.96),Ionic(3,"V",0.58),Ionic(3,"VI-ls",0.58),Ionic(3,"0-hs",0.645),
            Ionic(4,"IV",0.39),Ionic(4,"VI",0.53),Ionic(5,"IV",0.33),Ionic(6,"IV",0.255),Ionic(7,"IV",0.25),Ionic(7,"VI",0.46)],
    "Mt": [Ionic()],
    "Md": [Ionic()],
    "Hg": [Ionic(1,"III",0.97),Ionic(1,"VI",1.19),Ionic(2,"II",0.69),Ionic(2,"IV",0.96),Ionic(2,"VI",1.02),Ionic(2,"VIII",1.14)],
    "Mo": [Ionic(3,"VI",0.69),Ionic(4,"VI",0.65),Ionic(5,"IV",0.46),Ionic(5,"VI",0.61),Ionic(6,"IV",0.41),Ionic(6,"V",0.5),
            Ionic(6,"VI",0.59),Ionic(6,"VII",0.73)],
    "Mc": [Ionic()],
    "Nd": [Ionic(2,"VIII",1.29),Ionic(2,"IX",1.35),Ionic(3,"VI",0.983),Ionic(3,"VIII",1.109),Ionic(3,"IX",1.163),Ionic(3,"XII",1.27)],
    "Ne": [Ionic()],
    "Np": [Ionic(2,"VI",1.1),Ionic(3,"VI",1.01),Ionic(4,"VI",0.87),Ionic(4,"VIII",0.98),Ionic(5,"VI",0.75),
            Ionic(6,"VI",0.72),Ionic(7,"VI",0.71)],
    "Ni": [Ionic(2,"IV",0.55),Ionic(2,"IVSQ",0.49),Ionic(2,"V",0.63),Ionic(2,"VI",0.69),Ionic(3,"VI-ls",0.56),
            Ionic(3,"0-hs",0.6),Ionic(4,"VI-ls",0.48)],
    "Nh": [Ionic()],
    "Nb": [Ionic(3,"VI",0.72),Ionic(4,"VI",0.68),Ionic(4,"VIII",0.79),Ionic(5,"IV",0.48),Ionic(5,"VI",0.64),
            Ionic(5,"VII",0.69),Ionic(5,"VIII",0.74)],
    "N": [Ionic(-3,"IV",1.46),Ionic(3,"VI",0.16),Ionic(5,"III",0.104),Ionic(5,"VI",0.13)],
    "No": [Ionic(2,"VI",1.1)],
    "Og": [Ionic()],
    "Os": [Ionic(4,"VI",0.63),Ionic(5,"VI",0.575),Ionic(6,"V",0.49),Ionic(6,"VI",0.545),Ionic(7,"VI",0.525),Ionic(8,"IV",0.39)],
    "O": [Ionic(-2,"II",1.35),Ionic(-2,"III",1.36),Ionic(-2,"IV",1.38),Ionic(-2,"VI",1.4),Ionic(-2,"VIII",1.42)],
    "Pd": [Ionic(1,"II",0.59),Ionic(2,"IVSQ",0.64),Ionic(2,"VI",0.86),Ionic(3,"VI",0.76),Ionic(4,"VI",0.615)],
    "P": [Ionic(3,"VI",0.44),Ionic(5,"IV",0.17),Ionic(5,"V",0.29),Ionic(5,"VI",0.38)],
    "Pt": [Ionic(2,"IVSQ",0.6),Ionic(2,"VI",0.8),Ionic(4,"VI",0.625),Ionic(5,"VI",0.57)],
    "Pu": [Ionic(3,"VI",1),Ionic(4,"VI",0.86),Ionic(4,"VIII",0.96),Ionic(5,"VI",0.74),Ionic(6,"VI",0.71)],
    "Po": [Ionic(4,"VI",0.94),Ionic(4,"VIII",1.08),Ionic(6,"VI",0.67)],
    "K": [Ionic(1,"IV",1.37),Ionic(1,"VI",1.38),Ionic(1,"VII",1.46),Ionic(1,"VIII",1.51),Ionic(1,"IX",1.55),
            Ionic(1,"X",1.59),Ionic(1,"XII",1.64)],
    "Pr": [Ionic(3,"VI",0.99),Ionic(3,"VIII",1.126),Ionic(3,"IX",1.179),Ionic(4,"VI",0.85),Ionic(4,"VIII",0.96)],
    "Pm": [Ionic(3,"VI",0.97),Ionic(3,"VIII",1.093),Ionic(3,"IX",1.144)],
    "Pa": [Ionic(3,"VI",1.04),Ionic(4,"VI",0.9),Ionic(4,"VIII",1.01),Ionic(5,"VI",0.78),Ionic(5,"VIII",0.91),Ionic(5,"IX",0.95)],
    "Ra": [Ionic(2,"VIII",1.48),Ionic(2,"XII",1.7)],
    "Rn": [Ionic()],
    "Re": [Ionic(4,"VI",0.63),Ionic(5,"VI",0.58),Ionic(6,"VI",0.55),Ionic(7,"IV",0.38),Ionic(7,"VI",0.53)],
    "Rh": [Ionic(3,"VI",0.665),Ionic(4,"VI",0.6),Ionic(5,"VI",0.55)],
    "Rg": [Ionic()],
    "Rb": [Ionic(1,"VI",1.52),Ionic(1,"VII",1.56),Ionic(1,"VIII",1.61),Ionic(1,"IX",1.63),Ionic(1,"X",1.66),
            Ionic(1,"XI",1.69),Ionic(1,"XII",1.72),Ionic(1,"XIV",1.83)],
    "Ru": [Ionic(3,"VI",0.68),Ionic(4,"VI",0.62),Ionic(5,"VI",0.565),Ionic(7,"IV",0.38),Ionic(8,"IV",0.36)],
    "Rf": [Ionic()],
    "Sm": [Ionic(2,"VII",1.22),Ionic(2,"VIII",1.27),Ionic(2,"IX",1.32),Ionic(3,"VI",0.958),Ionic(3,"VII",1.02),
            Ionic(3,"VIII",1.079),Ionic(3,"IX",1.132),Ionic(3,"XII",1.24)],
    "Sc": [Ionic(3,"VI",0.745),Ionic(3,"VIII",0.87)],
    "Sg": [Ionic()],
    "Se": [Ionic(-2,"VI",1.98),Ionic(4,"VI",0.5),Ionic(6,"IV",0.28),Ionic(6,"VI",0.42)],
    "Si": [Ionic(4,"IV",0.26),Ionic(4,"VI",0.4)],
    "Ag": [Ionic(1,"II",0.67),Ionic(1,"IV",1),Ionic(1,"IVSQ",1.02),Ionic(1,"V",1.09),Ionic(1,"VI",1.15),Ionic(1,"VII",1.22),
            Ionic(1,"VIII",1.28),Ionic(2,"IVSQ",0.79),Ionic(2,"VI",0.94),Ionic(3,"IVSQ",0.67),Ionic(3,"VI",0.75)],
    "Na": [Ionic(1,"IV",0.99),Ionic(1,"V",1),Ionic(1,"VI",1.02),Ionic(1,"VII",1.12),Ionic(1,"VIII",1.18),Ionic(1,"IX",1.24),
            Ionic(1,"XII",1.39)],
    "Sr": [Ionic(2,"VI",1.18),Ionic(2,"VII",1.21),Ionic(2,"VIII",1.26),Ionic(2,"IX",1.31),Ionic(2,"X",1.36),Ionic(2,"XII",1.44)],
    "S": [Ionic(-2,"VI",1.84),Ionic(4,"VI",0.37),Ionic(6,"IV",0.12),Ionic(6,"VI",0.29)],
    "Ta": [Ionic(3,"VI",0.72),Ionic(4,"VI",0.68),Ionic(5,"VI",0.64),Ionic(5,"VII",0.69),Ionic(5,"VIII",0.74)],
    "Tc": [Ionic(4,"VI",0.645),Ionic(5,"VI",0.6),Ionic(7,"IV",0.37),Ionic(7,"VI",0.56)],
    "Te": [Ionic(-2,"VI",2.21),Ionic(4,"III",0.52),Ionic(4,"IV",0.66),Ionic(4,"VI",0.97),Ionic(6,"IV",0.43),Ionic(6,"VI",0.56)],
    "Ts": [Ionic()],
    "Tb": [Ionic(3,"VI",0.923),Ionic(3,"VII",0.98),Ionic(3,"VIII",1.04),Ionic(3,"IX",1.095),Ionic(4,"VI",0.76),Ionic(4,"VIII",0.88)],
    "Tl": [Ionic(1,"VI",1.5),Ionic(1,"VIII",1.59),Ionic(1,"XII",1.7),Ionic(3,"IV",0.75),Ionic(3,"VI",0.885),Ionic(3,"VIII",0.98)],
    "Th": [Ionic(4,"VI",0.94),Ionic(4,"VIII",1.05),Ionic(4,"IX",1.09),Ionic(4,"X",1.13),Ionic(4,"XI",1.18),Ionic(4,"XII",1.21)],
    "Tm": [Ionic(2,"VI",1.03),Ionic(2,"VII",1.09),Ionic(3,"VI",0.88),Ionic(3,"VIII",0.994),Ionic(3,"IX",1.052)],
    "Sn": [Ionic(4,"IV",0.55),Ionic(4,"V",0.62),Ionic(4,"VI",0.69),Ionic(4,"VII",0.75),Ionic(4,"VIII",0.81)],
    "Ti": [Ionic(2,"VI",0.86),Ionic(3,"VI",0.67),Ionic(4,"IV",0.42),Ionic(4,"V",0.51),Ionic(4,"VI",0.605),Ionic(4,"VIII",0.74)],
    "W": [Ionic(4,"VI",0.66),Ionic(5,"VI",0.62),Ionic(6,"IV",0.42),Ionic(6,"V",0.51),Ionic(6,"VI",0.6)],
    "U": [Ionic(3,"VI",1.025),Ionic(4,"VI",0.89),Ionic(4,"VII",0.95),Ionic(4,"VIII",1),Ionic(4,"IX",1.05),Ionic(4,"XII",1.17),
            Ionic(5,"VI",0.76),Ionic(5,"VII",0.84),Ionic(6,"II",0.45),Ionic(6,"IV",0.52),Ionic(6,"VI",0.73),Ionic(6,"VII",0.81),
            Ionic(6,"VIII",0.86)],
    "V": [Ionic(2,"VI",0.79),Ionic(3,"VI",0.64),Ionic(4,"V",0.53),Ionic(4,"VI",0.58),Ionic(4,"VIII",0.72),Ionic(5,"IV",0.355),
            Ionic(5,"V",0.46),Ionic(5,"VI",0.54)],
    "Xe": [Ionic(8,"IV",0.4),Ionic(8,"VI",0.48)],
    "Yb": [Ionic(2,"VI",1.02),Ionic(2,"VII",1.08),Ionic(2,"VIII",1.14),Ionic(3,"VI",0.868),Ionic(3,"VII",0.925),Ionic(3,"VIII",0.985),
            Ionic(3,"IX",1.042)],
    "Y": [Ionic(3,"VI",0.9),Ionic(3,"VII",0.96),Ionic(3,"VIII",1.019),Ionic(3,"IX",1.075)],
    "Zn": [Ionic(2,"IV",0.6),Ionic(2,"V",0.68),Ionic(2,"VI",0.74),Ionic(2,"VIII",0.9)],
    "Zr": [Ionic(4,"IV",0.59),Ionic(4,"V",0.66),Ionic(4,"VI",0.72),Ionic(4,"VII",0.78),Ionic(4,"VIII",0.84),Ionic(4,"IX",0.89)],
    }

# Atom data: radii measured in Angstroms, taken from the reference below:
# "Atomic Radii of the Elements," in CRC Handbook of Chemistry and Physics, 101st Edition
# (Internet Version 2020), John R. Rumble, ed., CRC Press/Taylor & Francis, Boca Raton, FL
# Elements arranged alphabetically, except for 'Dummy' which is a placeholder for non-elements
Dummy = Atom_Data(radius=0.01, color=(1.0, 0.65, 1.0, 1))

Actinium = Atom_Data(2.01, 2.47, ionicData=IonicRadii["Ac"])
Aluminum = Atom_Data(1.24, 1.84, ionicData=IonicRadii["Al"])
Americium = Atom_Data(1.73, 2.44, ionicData=IonicRadii["Am"])
Antimony = Atom_Data(1.40, 2.06, ionicData=IonicRadii["Sb"])
Argon = Atom_Data(1.01, 1.88, ionicData=IonicRadii["Ar"])
Arsenic = Atom_Data(1.20, 1.85, ionicData=IonicRadii["As"])
Astatine = Atom_Data(1.48, 2.02, (0.99, 0.28, 0.11, 1), ionicData=IonicRadii["At"])
Barium = Atom_Data(2.06, 2.68, ionicData=IonicRadii["Ba"])
Berkelium = Atom_Data(1.68, 2.44, ionicData=IonicRadii["Bk"])
Beryllium = Atom_Data(0.99, 1.53, (0.13, 0.96, 0.55, 1), ionicData=IonicRadii["Be"])
Bismuth = Atom_Data(1.50, 2.07, (0.53, 0.84, 0.55, 1), ionicData=IonicRadii["Bi"])
Bohrium = Atom_Data(1.41, ionicData=IonicRadii["Bh"])
Boron = Atom_Data(0.84, 1.92, (1.00, 0.70, 0.70, 1), ionicData=IonicRadii["B"])
Bromine = Atom_Data(1.17, 1.85, (0.76, 0.00, 0.14, 1), ionicData=IonicRadii["Br"])
Cadmium = Atom_Data(1.40, 2.18, ionicData=IonicRadii["Cd"])
Calcium = Atom_Data(1.74, 2.31, (0.94, 0.00, 0.36, 1), ionicData=IonicRadii["Ca"])
Californium = Atom_Data(1.68, 2.45, ionicData=IonicRadii["Cf"])
Carbon = Atom_Data(0.75, 1.70, (0.10, 0.10, 0.10, 1), ionicData=IonicRadii["Ac"])
Cerium = Atom_Data(1.84, 2.42, ionicData=IonicRadii["Ce"])
Cesium = Atom_Data(2.38, 3.43, ionicData=IonicRadii["Cs"])
Chlorine = Atom_Data(1.00, 1.75, (0.00, 0.94, 0.26, 1), ionicData=IonicRadii["Cl"])
Chromium = Atom_Data(1.30, 2.06, ionicData=IonicRadii["Cr"])
Cobalt = Atom_Data(1.18, 2.00, (0.00, 0.39, 0.94, 1), ionicData=IonicRadii["Co"])
Copernicium = Atom_Data(1.22, ionicData=IonicRadii["Cn"])
Copper = Atom_Data(1.22, 1.96, (0.00, 0.94, 0.75, 1), ionicData=IonicRadii["Cu"])
Curium = Atom_Data(1.68, 2.45, ionicData=IonicRadii["Cm"])
Darmstadtium = Atom_Data(1.28, ionicData=IonicRadii["Ds"])
Dubnium = Atom_Data(1.49, ionicData=IonicRadii["Db"])
Dysprosium = Atom_Data(1.80, 2.31, ionicData=IonicRadii["Dy"])
Einsteinium = Atom_Data(1.65, 2.45, ionicData=IonicRadii["Es"])
Erbium = Atom_Data(1.77, 2.29, ionicData=IonicRadii["Er"])
Europium = Atom_Data(1.83, 2.35, (1.00, 0.18, 0.39, 1), ionicData=IonicRadii["Eu"])
Fermium = Atom_Data(1.67, 2.45, ionicData=IonicRadii["Fm"])
Flerovium = Atom_Data(1.43, ionicData=IonicRadii["Fl"])
Fluorine = Atom_Data(0.60, 1.47, (0.00, 0.90, 0.00, 1), ionicData=IonicRadii["F"])
Francium = Atom_Data(2.42, 3.48, ionicData=IonicRadii["Fr"])
Gadolinium = Atom_Data(1.82, 2.34, ionicData=IonicRadii["Gd"])
Gallium = Atom_Data(1.23, 1.87, ionicData=IonicRadii["Ga"])
Germanium = Atom_Data(1.20, 2.11, ionicData=IonicRadii["Ge"])
Gold = Atom_Data(1.30, 2.14, (0.99, 0.95, 0.11, 1), ionicData=IonicRadii["Au"])
Hafnium = Atom_Data(1.64, 2.23, ionicData=IonicRadii["Hf"])
Hassium = Atom_Data(1.34, ionicData=IonicRadii["Hs"])
Helium = Atom_Data(0.37, 1.40, ionicData=IonicRadii["He"])
Holmium = Atom_Data(1.79, 2.30, ionicData=IonicRadii["Ho"])
Hydrogen = Atom_Data(0.32, 1.10, (0.80, 0.80, 0.80, 1), ionicData=IonicRadii["H"])
Indium = Atom_Data(1.42, 1.93, ionicData=IonicRadii["In"])
Iodine = Atom_Data(1.36, 1.98, (0.49, 0.03, 0.73, 1), ionicData=IonicRadii["I"])
Iridium = Atom_Data(1.32, 2.13, ionicData=IonicRadii["Ir"])
Iron = Atom_Data(1.24, 2.04, (0.47, 0.05, 0.13, 1), ionicData=IonicRadii["Fe"])
Krypton = Atom_Data(1.16, 2.02, ionicData=IonicRadii["Kr"])
Lanthanum = Atom_Data(1.94, 2.43, ionicData=IonicRadii["La"])
Lawrencium = Atom_Data(1.61, 2.46, ionicData=IonicRadii["Lr"])
Lead = Atom_Data(1.45, 2.02, (0.06, 0.06, 0.06, 1), ionicData=IonicRadii["Pb"])
Lithium = Atom_Data(1.30, 1.82, (0.96, 0.13, 0.76, 1), ionicData=IonicRadii["Li"])
Livermorium = Atom_Data(1.75, ionicData=IonicRadii["Lv"])
Lutetium = Atom_Data(1.74, 2.24, ionicData=IonicRadii["Lu"])
Magnesium = Atom_Data(1.40, 1.73, (0.90, 0.90, 0.90, 1), ionicData=IonicRadii["Mg"])
Manganese = Atom_Data(1.29, 2.05, (0.94, 0.00, 0.80, 1), ionicData=IonicRadii["Mn"])
Meitnerium = Atom_Data(1.29, ionicData=IonicRadii["Mt"])
Mendelevium = Atom_Data(1.73, 2.46, ionicData=IonicRadii["Md"])
Mercury = Atom_Data(1.32, 2.23, ionicData=IonicRadii["Hg"])
Molybdenum = Atom_Data(1.46, 2.17, ionicData=IonicRadii["Mo"])
Moscovium = Atom_Data(1.62, ionicData=IonicRadii["Mc"])
Neodymium = Atom_Data(1.88, 2.39, ionicData=IonicRadii["Nd"])
Neon = Atom_Data(0.62, 1.54, ionicData=IonicRadii["Ne"])
Neptunium = Atom_Data(1.80, 2.39, ionicData=IonicRadii["Np"])
Nickel = Atom_Data(1.17, 1.97, ionicData=IonicRadii["Ni"])
Nihonium = Atom_Data(1.36, ionicData=IonicRadii["Nh"])
Niobium = Atom_Data(1.56, 2.18, ionicData=IonicRadii["Nb"])
Nitrogen = Atom_Data(0.71, 1.55, (0.00, 0.00, 0.90, 1), ionicData=IonicRadii["N"])
Nobelium = Atom_Data(1.76, 2.46, ionicData=IonicRadii["No"])
Oganesson = Atom_Data(1.57, ionicData=IonicRadii["Og"])
Osmium = Atom_Data(1.36, 2.16, ionicData=IonicRadii["Os"])
Oxygen = Atom_Data(0.64, 1.52, (0.90, 0.00, 0.00 ,1), ionicData=IonicRadii["O"])
Palladium = Atom_Data(1.30, 2.10, ionicData=IonicRadii["Pd"])
Phosphorus = Atom_Data(1.09, 1.80, (0.85, 0.00, 0.95, 1), ionicData=IonicRadii["P"])
Platinum = Atom_Data(1.30, 2.13, ionicData=IonicRadii["Pt"])
Plutonium = Atom_Data(1.80, 2.43, (1.00, 0.80, 0.00, 1), ionicData=IonicRadii["Pu"])
Polonium = Atom_Data(1.42, 1.97, (0.53, 1.00, 0.32, 1), ionicData=IonicRadii["Po"])
Potassium = Atom_Data(2.00, 2.75, (0.60, 0.00, 0.94, 1), ionicData=IonicRadii["K"])
Praseodymium = Atom_Data(1.90, 2.40, ionicData=IonicRadii["Pr"])
Promethium = Atom_Data(1.86, 2.38, ionicData=IonicRadii["Pm"])
Protactinium = Atom_Data(1.84, 2.43, ionicData=IonicRadii["Pa"])
Radium = Atom_Data(2.11, 2.83, ionicData=IonicRadii["Ra"])
Radon = Atom_Data(1.46, 2.20, (0.57, 0.99, 0.10, 1), ionicData=IonicRadii["Rn"])
Rhenium = Atom_Data(1.41, ionicData=IonicRadii["Re"])
Rhodium = Atom_Data(1.34, 2.10, ionicData=IonicRadii["Rh"])
Roentgenium = Atom_Data(1.21, ionicData=IonicRadii["Rg"])
Rubidium = Atom_Data(2.15, 3.03, ionicData=IonicRadii["Rb"])
Ruthenium = Atom_Data(1.36, 2.13, ionicData=IonicRadii["Ru"])
Rutherfordium = Atom_Data(1.57, ionicData=IonicRadii["Rf"])
Samarium = Atom_Data(1.85, 2.36, ionicData=IonicRadii["Sm"])
Scandium = Atom_Data(1.59, 2.15, (0.94, 0.70, 0.00, 1), ionicData=IonicRadii["Sc"])
Seaborgium = Atom_Data(1.43, ionicData=IonicRadii["Sg"])
Selenium = Atom_Data(1.18, 1.90, ionicData=IonicRadii["Se"])
Silicon = Atom_Data(1.14, 2.10, (0.95, 1.00, 0.48, 1), ionicData=IonicRadii["Si"])
Silver = Atom_Data(1.36, 2.11, (0.83, 0.83, 0.83, 1), ionicData=IonicRadii["Ag"])
Sodium = Atom_Data(1.60, 2.27, (0.00, 0.50, 0.76, 1), ionicData=IonicRadii["Na"])
Strontium = Atom_Data(1.90, 2.49, ionicData=IonicRadii["Sr"])
Sulfur = Atom_Data(1.04, 1.80, (0.94, 0.94, 0.00, 1), ionicData=IonicRadii["S"])
Tantalum = Atom_Data(1.58, 2.22, ionicData=IonicRadii["Ta"])
Technetium = Atom_Data(1.38, 2.16, ionicData=IonicRadii["Tc"])
Tellurium = Atom_Data(1.37, 2.06, ionicData=IonicRadii["Te"])
Tennessine = Atom_Data(1.65, ionicData=IonicRadii["Ts"])
Terbium = Atom_Data(1.81, 2.33, ionicData=IonicRadii["Tb"])
Thallium = Atom_Data(1.44, 1.96, ionicData=IonicRadii["Tl"])
Thorium = Atom_Data(1.90, 2.45, ionicData=IonicRadii["Th"])
Thulium = Atom_Data(1.77, 2.27, ionicData=IonicRadii["Tm"])
Tin = Atom_Data(1.40, 2.17, ionicData=IonicRadii["Sn"])
Titanium = Atom_Data(1.48, 2.11, ionicData=IonicRadii["Ti"])
Tungsten = Atom_Data(1.50, 2.18, ionicData=IonicRadii["W"])
Uranium = Atom_Data(1.83, 2.41, (0.53, 1.00, 0.32, 1), ionicData=IonicRadii["U"])
Vanadium = Atom_Data(1.44, 2.07, ionicData=IonicRadii["V"])
Xenon = Atom_Data(1.36, 2.16, ionicData=IonicRadii["Xe"])
Ytterbium = Atom_Data(1.78, 2.26, ionicData=IonicRadii["Yb"])
Yttrium = Atom_Data(1.76, 2.32, ionicData=IonicRadii["Y"])
Zinc = Atom_Data(1.20, 2.01, ionicData=IonicRadii["Zn"])
Zirconium = Atom_Data(1.64, 2.23, ionicData=IonicRadii["Zr"])


Elements = { #element symbols, their covalent radii & their RGBA color values
    "Xx": Dummy,
    "Ac": Actinium,
    "Al": Aluminum,
    "Am": Americium,
    "Sb": Antimony,
    "Ar": Argon,
    "As": Arsenic,
    "At": Astatine,
    "Ba": Barium,
    "Bk": Berkelium,
    "Be": Beryllium,
    "Bi": Bismuth,
    "Bh": Bohrium,
    "B": Boron,
    "Br": Bromine,
    "Cd": Cadmium,
    "Ca": Calcium,
    "Cf": Californium,
    "C": Carbon,
    "Ce": Cerium,
    "Cs": Cesium,
    "Cl": Chlorine,
    "Cr": Chromium,
    "Co": Cobalt,
    "Cn": Copernicium,
    "Cu": Copper,
    "Cm": Curium,
    "Ds": Darmstadtium,
    "Db": Dubnium,
    "Dy": Dysprosium,
    "Es": Einsteinium,
    "Er": Erbium,
    "Eu": Europium,
    "Fm": Fermium,
    "Fl": Flerovium,
    "F": Fluorine,
    "Fr": Francium,
    "Gd": Gadolinium,
    "Ga": Gallium,
    "Ge": Germanium,
    "Au": Gold,
    "Hf": Hafnium,
    "Hs": Hassium,
    "He": Helium,
    "Ho": Holmium,
    "H": Hydrogen,
    "In": Indium,
    "I": Iodine,
    "Ir": Iridium,
    "Fe": Iron,
    "Kr": Krypton,
    "La": Lanthanum,
    "Lr": Lawrencium,
    "Pb": Lead,
    "Li": Lithium,
    "Lv": Livermorium,
    "Lu": Lutetium,
    "Mg": Magnesium,
    "Mn": Manganese,
    "Mt": Meitnerium,
    "Md": Mendelevium,
    "Hg": Mercury,
    "Mo": Molybdenum,
    "Mc": Moscovium,
    "Nd": Neodymium,
    "Ne": Neon,
    "Np": Neptunium,
    "Ni": Nickel,
    "Nh": Nihonium,
    "Nb": Niobium,
    "N": Nitrogen,
    "No": Nobelium,
    "Og": Oganesson,
    "Os": Osmium,
    "O": Oxygen,
    "Pd": Palladium,
    "P": Phosphorus,
    "Pt": Platinum,
    "Pu": Plutonium,
    "Po": Polonium,
    "K": Potassium,
    "Pr": Praseodymium,
    "Pm": Promethium,
    "Pa": Protactinium,
    "Ra": Radium,
    "Rn": Radon,
    "Re": Rhenium,
    "Rh": Rhodium,
    "Rg": Roentgenium,
    "Rb": Rubidium,
    "Ru": Ruthenium,
    "Rf": Rutherfordium,
    "Sm": Samarium,
    "Sc": Scandium,
    "Sg": Seaborgium,
    "Se": Selenium,
    "Si": Silicon,
    "Ag": Silver,
    "Na": Sodium,
    "Sr": Strontium,
    "S": Sulfur,
    "Ta": Tantalum,
    "Tc": Technetium,
    "Te": Tellurium,
    "Ts": Tennessine,
    "Tb": Terbium,
    "Tl": Thallium,
    "Th": Thorium,
    "Tm": Thulium,
    "Sn": Tin,
    "Ti": Titanium,
    "W": Tungsten,
    "U": Uranium,
    "V": Vanadium,
    "Xe": Xenon,
    "Yb": Ytterbium,
    "Y": Yttrium,
    "Zn": Zinc,
    "Zr": Zirconium,
    }