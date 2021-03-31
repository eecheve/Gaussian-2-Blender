class Atom_Data:
    """Atom data class. Stores Radius: covalent; Color: tuple, RGBA values"""

    def __init__(self, radius: float, vanDerWaals=0.00, color=(0.5,0.5,0.5)): # Gray is the default color if none is specified
        self.radius = radius #covalent radius
        self.vanDerWaals = vanDerWaals #default is set temprarilly as 0.00 is radius is not reported
        self.color = color #RGBA values: default is gray

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

# Atom data: radii measured in Angstroms, taken from the reference below:
# "Atomic Radii of the Elements," in CRC Handbook of Chemistry and Physics, 101st Edition
# (Internet Version 2020), John R. Rumble, ed., CRC Press/Taylor & Francis, Boca Raton, FL
# Elements arranged alphabetically, except for 'Dummy' which is a placeholder for non-elements
Dummy = Atom_Data(radius=0.01, color=(0.50, 0.50, 0.50, 1))

Actinium = Atom_Data(2.01, 2.47)
Aluminum = Atom_Data(1.24, 1.84)
Americium = Atom_Data(1.73, 2.44)
Antimony = Atom_Data(1.40, 2.06)
Argon = Atom_Data(1.01, 1.88)
Arsenic = Atom_Data(1.20, 1.85)
Astatine = Atom_Data(1.48, 2.02, (0.99, 0.28, 0.11, 1))
Barium = Atom_Data(2.06, 2.68)
Berkelium = Atom_Data(1.68, 2.44)
Beryllium = Atom_Data(0.99, 1.53, (0.13, 0.96, 0.55, 1))
Bismuth = Atom_Data(1.50, 2.07, (0.53, 0.84, 0.55, 1))
Bohrium = Atom_Data(1.41)
Boron = Atom_Data(0.84, 1.92, (1.00, 0.70, 0.70, 1))
Bromine = Atom_Data(1.17, 1.85, (0.76, 0.00, 0.14, 1))
Cadmium = Atom_Data(1.40, 2.18)
Calcium = Atom_Data(1.74, 2.31, (0.94, 0.00, 0.36, 1))
Californium = Atom_Data(1.68, 2.45)
Carbon = Atom_Data(0.75, 1.70, (0.10, 0.10, 0.10, 1))
Cerium = Atom_Data(1.84, 2.42)
Cesium = Atom_Data(2.38, 3.43)
Chlorine = Atom_Data(1.00, 1.75, (0.00, 0.94, 0.26, 1))
Chromium = Atom_Data(1.30, 2.06)
Cobalt = Atom_Data(1.18, 2.00, (0.00, 0.39, 0.94, 1))
Copernicium = Atom_Data(1.22)
Copper = Atom_Data(1.22, 1.96, (0.00, 0.94, 0.75, 1))
Curium = Atom_Data(1.68, 2.45)
Darmstadtium = Atom_Data(1.28)
Dubnium = Atom_Data(1.49)
Dysprosium = Atom_Data(1.80, 2.31)
Einsteinium = Atom_Data(1.65, 2.45)
Erbium = Atom_Data(1.77, 2.29)
Europium = Atom_Data(1.83, 2.35, (1.00, 0.18, 0.39, 1))
Fermium = Atom_Data(1.67, 2.45)
Flerovium = Atom_Data(1.43)
Fluorine = Atom_Data(0.60, 1.47, (0.00, 0.90, 0.00, 1))
Francium = Atom_Data(2.42, 3.48)
Gadolinium = Atom_Data(1.82, 2.34)
Gallium = Atom_Data(1.23, 1.87)
Germanium = Atom_Data(1.20, 2.11)
Gold = Atom_Data(1.30, 2.14, (0.99, 0.95, 0.11, 1))
Hafnium = Atom_Data(1.64, 2.23)
Hassium = Atom_Data(1.34)
Helium = Atom_Data(0.37, 1.40)
Holmium = Atom_Data(1.79, 2.30)
Hydrogen = Atom_Data(0.32, 1.10, (0.80, 0.80, 0.80, 1))
Indium = Atom_Data(1.42, 1.93)
Iodine = Atom_Data(1.36, 1.98, (0.49, 0.03, 0.73, 1))
Iridium = Atom_Data(1.32, 2.13)
Iron = Atom_Data(1.24, 2.04, (0.47, 0.05, 0.13, 1))
Krypton = Atom_Data(1.16, 2.02)
Lanthanum = Atom_Data(1.94, 2.43)
Lawrencium = Atom_Data(1.61, 2.46)
Lead = Atom_Data(1.45, 2.02, (0.06, 0.06, 0.06, 1))
Lithium = Atom_Data(1.30, 1.82, (0.96, 0.13, 0.76, 1))
Livermorium = Atom_Data(1.75)
Lutetium = Atom_Data(1.74, 2.24)
Magnesium = Atom_Data(1.40, 1.73, (0.90, 0.90, 0.90, 1))
Manganese = Atom_Data(1.29, 2.05, (0.94, 0.00, 0.80, 1))
Meitnerium = Atom_Data(1.29)
Mendelevium = Atom_Data(1.73, 2.46)
Mercury = Atom_Data(1.32, 2.23)
Molybdenum = Atom_Data(1.46, 2.17)
Moscovium = Atom_Data(1.62)
Neodymium = Atom_Data(1.88, 2.39)
Neon = Atom_Data(0.62, 1.54)
Neptunium = Atom_Data(1.80, 2.39)
Nickel = Atom_Data(1.17, 1.97)
Nihonium = Atom_Data(1.36)
Niobium = Atom_Data(1.56, 2.18)
Nitrogen = Atom_Data(0.71, 1.55, (0.00, 0.00, 0.90, 1))
Nobelium = Atom_Data(1.76, 2.46)
Oganesson = Atom_Data(1.57)
Osmium = Atom_Data(1.36, 2.16)
Oxygen = Atom_Data(0.64, 1.52, (0.90, 0.00, 0.00 ,1))
Palladium = Atom_Data(1.30, 2.10)
Phosphorus = Atom_Data(1.09, 1.80, (0.85, 0.00, 0.95, 1))
Platinum = Atom_Data(1.30, 2.13)
Plutonium = Atom_Data(1.80, 2.43, (1.00, 0.80, 0.00, 1))
Polonium = Atom_Data(1.42, 1.97, (0.53, 1.00, 0.32, 1))
Potassium = Atom_Data(2.00, 2.75, (0.60, 0.00, 0.94, 1))
Praseodymium = Atom_Data(1.90, 2.40)
Promethium = Atom_Data(1.86, 2.38)
Protactinium = Atom_Data(1.84, 2.43)
Radium = Atom_Data(2.11, 2.83)
Radon = Atom_Data(1.46, 2.20, (0.57, 0.99, 0.10, 1))
Rhenium = Atom_Data(1.41)
Rhodium = Atom_Data(1.34, 2.10)
Roentgenium = Atom_Data(1.21)
Rubidium = Atom_Data(2.15, 3.03)
Ruthenium = Atom_Data(1.36, 2.13)
Rutherfordium = Atom_Data(1.57)
Samarium = Atom_Data(1.85, 2.36)
Scandium = Atom_Data(1.59, 2.15, (0.94, 0.70, 0.00, 1))
Seaborgium = Atom_Data(1.43)
Selenium = Atom_Data(1.18, 1.90)
Silicon = Atom_Data(1.14, 2.10, (0.95, 1.00, 0.48, 1))
Silver = Atom_Data(1.36, 2.11, (0.83, 0.83, 0.83, 1))
Sodium = Atom_Data(1.60, 2.27, (0.00, 0.50, 0.76, 1))
Strontium = Atom_Data(1.90, 2.49)
Sulfur = Atom_Data(1.04, 1.80, (0.94, 0.94, 0.00, 1))
Tantalum = Atom_Data(1.58, 2.22)
Technetium = Atom_Data(1.38, 2.16)
Tellurium = Atom_Data(1.37, 2.06)
Tennessine = Atom_Data(1.65)
Terbium = Atom_Data(1.81, 2.33)
Thallium = Atom_Data(1.44, 1.96)
Thorium = Atom_Data(1.90, 2.45)
Thulium = Atom_Data(1.77, 2.27)
Tin = Atom_Data(1.40, 2.17)
Titanium = Atom_Data(1.48, 2.11)
Tungsten = Atom_Data(1.50, 2.18)
Uranium = Atom_Data(1.83, 2.41, (0.53, 1.00, 0.32, 1))
Vanadium = Atom_Data(1.44, 2.07)
Xenon = Atom_Data(1.36, 2.16)
Ytterbium = Atom_Data(1.78, 2.26)
Yttrium = Atom_Data(1.76, 2.32)
Zinc = Atom_Data(1.20, 2.01)
Zirconium = Atom_Data(1.64, 2.23)


Elements = { #element symbols, their covalent radii & their RGBA color values
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
    

