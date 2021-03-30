class Atom_Data:
    """Atom data class. Stores Radius: covalent; Color: tuple, RGBA values"""

    def __init__(self, radius: float, color=(0.5,0.5,0.5,1), vanDerWaals=0.00): # Gray is the default color if none is specified
        self.radius = radius #covalent radius
        self.color = color
        self.vanDerWaals = vanDerWaals #default is set temprarilly as 0.00, as this is a new idea

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
        return self.vanDerWaals

#Atom data for the first 86 elements of the periodic table. Data taken from https://ptable.com/#Properties/Series
#**Van der Waals radii not found at ptable were taken from https://en.wikipedia.org/wiki/Van_der_Waals_radius
#*** Van der Waals radii not found at wikipedia from Inorganic Materials, Vol 37, No 9, 2001, pp 871-885
Dummy = Atom_Data(0.01, (0.50, 0.50, 0.50, 1))

Hydrogen = Atom_Data(0.37, (0.80, 0.80, 0.80, 1), 1.20)
Helium = Atom_Data(0.32, 1.40)
Lithium = Atom_Data(1.34, (0.96, 0.13, 0.76, 1), 1.82)
Beryllium = Atom_Data(0.90, (0.13, 0.96, 0.55, 1), 1.53) #**
Boron = Atom_Data(0.84, (1.00, 0.70, 0.70, 1), 1.92) #**
Carbon = Atom_Data(0.77, (0.10, 0.10, 0.10, 1), 1.70)
Nitrogen = Atom_Data(0.75, (0.00, 0.00, 0.90, 1), 1.55)
Oxygen = Atom_Data(0.73, (0.90, 0.00, 0.00, 1), 1.52)
Fluorine = Atom_Data(0.71, (0.00, 0.90, 0.00, 1), 1.47)
Neon = Atom_Data(0.69, 1.54)

Sodium = Atom_Data(1.54, (0.00, 0.50, 0.76, 1), 2.27)
Magnesium = Atom_Data(1.30, (0.90, 0.90, 0.90, 1), 1.73)
Aluminium = Atom_Data(1.18, 1.84) #**
Silicon = Atom_Data(1.11, (0.95, 1.00, 0.48, 1), 2.10)
Phosphorus = Atom_Data(1.06, (0.85, 0, 0.95, 1), 1.80)
Sulfur = Atom_Data(1.02, (0.94, 0.94, 0.00, 1), 1.80)
Chlorine = Atom_Data(0.99, (0.00, 0.94, 0.26, 1), 1.75)
Argon = Atom_Data(0.97, 1.88)

Potassium = Atom_Data(1.96, (0.60, 0.00, 0.94, 1), 2.75)
Calcium = Atom_Data(1.74, (0.94, 0.00, 0.36, 1), 2.31) #**
Scandium = Atom_Data(1.44, (0.94, 0.70, 0.00, 1), 2.28) #***
Titanium = Atom_Data(1.36, 2.14) #***
Vanadium = Atom_Data(1.25, (0.66, 0.94, 0.00, 1), 2.03) #*** 
Chromium = Atom_Data(1.27, 1.97) #*** 
Manganese = Atom_Data(1.39, (0.94, 0.00, 0.80, 1), 1.96) #*** 
Iron = Atom_Data(1.25, (0.47, 0.05, 0.13, 1), 1.96) #*** 
Cobalt = Atom_Data(1.26, (0.00, 0.39, 0.94, 1), 1.95) #*** 
Nickel = Atom_Data(1.21, 1.63)
Copper = Atom_Data(1.38, (0.00, 0.94, 0.75, 1), 1.40)
Zinc = Atom_Data(1.31, 1.39)
Gallium = Atom_Data(1.26, 1.87)
Germanium = Atom_Data(1.22, 2.11) #**
Arsenic = Atom_Data(1.19, 1.85)
Selenium = Atom_Data(1.16, 1.90)
Bromine = Atom_Data(1.14, (0.76, 0.00, 0.14, 1), 1.85)
Krypton = Atom_Data(1.10, 2.02)

Rubidium = Atom_Data(2.11, (0.52, 0.04, 0.18, 1), 3.03)
Strontium = Atom_Data(1.92, 2.49)
Yttrium = Atom_Data(1.62, 2.45) #***
Zirconium = Atom_Data(1.48, 2.25) #***
Niobium = Atom_Data(1.37, 2.13) #***
Molybdenum = Atom_Data(1.45, 2.06) #***
Technetium = Atom_Data(1.56, 2.04) #***
Ruthenium = Atom_Data(1.26, 2.02) #***
Rhodium = Atom_Data(1.35, 2.02) #***
Palladium = Atom_Data(1.31, 1.63)
Silver = Atom_Data(1.53, (0.83, 0.83, 0.83, 1), 1.72)
Cadmium = Atom_Data(1.48, 1.58)
Indium = Atom_Data(1.44, 1.93)
Tin = Atom_Data(1.41, 2.17)
Antimony = Atom_Data(1.38, 2.06)
Tellurium = Atom_Data(1.35, 2.06)
Iodine = Atom_Data(1.33, (0.49, 0.03, 0.73, 1), 1.98)
Xenon = Atom_Data(1.30, 2.16)

Caesium = Atom_Data(2.25, 3.43)
Barium = Atom_Data(1.98, 2.68)
Lanthanum = Atom_Data(1.69)
Hafnium = Atom_Data(1.50)
Tantalum = Atom_Data(1.38)
Tungsten = Atom_Data(1.46)
Rhenium = Atom_Data(1.59)
Osmium = Atom_Data(1.28, 2.03) #***
Iridium = Atom_Data(1.37, 2.03) #***
Platinum = Atom_Data(1.28, 1.75)
Gold = Atom_Data(1.44, (0.99, 0.95, 0.11, 1), 1.66)
Mercury = Atom_Data(1.49, 1.55)
Thallium = Atom_Data(1.48, 1.96)
Lead = Atom_Data(1.47, (0.06, 0.06, 0.06, 1), 2.02)
Bismuth = Atom_Data(1.46, (0.53, 0.84, 0.55, 1), 2.07)
Polonium = Atom_Data(1.90, (0.53, 1.00, 0.32, 1), 1.97) #empirical
Astatine = Atom_Data(1.27, (0.99, 0.28, 0.11, 1), 2.02) #calculated
Radon = Atom_Data(1.45, (0.57, 0.99, 0.10, 1), 2.20)

Cerium = Atom_Data(1.85) #empirical
Praseodymium = Atom_Data(1.85) #empirical
Neodymium = Atom_Data(1.85) #empirical
Promethium = Atom_Data(1.85) #empirical
Samarium = Atom_Data(1.85) #empirical
Europium = Atom_Data(1.85, (1.00, 0.18, 0.39, 1)) #empirical
Gadolinium = Atom_Data(1.80) #empirical
Terbium = Atom_Data(1.75) #empirical
Dysprosium = Atom_Data(1.75) #empirical
Holmium = Atom_Data(1.75) #empirical
Erbium = Atom_Data(1.75) #empirical
Thulium = Atom_Data(1.75) #empirical
Ytterbium = Atom_Data(1.75) #empirical
Lutentium = Atom_Data(1.75) #empirical

Elements = { #element symbols, their covalent radii & their RGBA color values
    "?s": Dummy,
    "H": Hydrogen,
    "He": Helium,
    "Li": Lithium,
    "B": Boron,
    "C": Carbon,
    "N": Nitrogen,
    "O": Oxygen,
    "F": Fluorine,
    "Ne": Neon,
    "Na": Sodium,
    "Mg": Magnesium,
    "Al": Aluminium,
    "Si": Silicon,
    "P": Phosphorus,
    "S": Sulfur,
    "Cl": Chlorine,
    "Ar": Argon,
    "K": Potassium,
    "Ca": Calcium,
    "Sc": Scandium,
    "Ti": Titanium,
    "V": Vanadium,
    "Cr": Chromium,
    "Mn": Manganese,
    "Fe": Iron,
    "Co": Cobalt,
    "Ni": Nickel,
    "Cu": Copper,
    "Zn": Zinc,
    "Ga": Gallium,
    "Ge": Germanium,
    "As": Arsenic,
    "Se": Selenium,
    "Br": Bromine,
    "Kr": Krypton,
    "Rb": Rubidium,
    "Sr": Strontium,
    "Y": Yttrium,
    "Zr": Zirconium,
    "Nb": Niobium,
    "Mo": Molybdenum,
    "Tc": Technetium,
    "Ru": Ruthenium,
    "Rh": Rhodium,
    "Pd": Palladium,
    "Ag": Silver,
    "Cd": Cadmium,
    "In": Indium,
    "Sn": Tin,
    "Sb": Antimony,
    "Te": Tellurium,
    "I": Iodine,
    "Xe": Xenon,
    "Cs": Caesium,
    "Ba": Barium,
    "La": Lanthanum,
    "Hf": Hafnium,
    "Ta": Tantalum,
    "W": Tungsten,
    "Re": Rhenium,
    "Os": Osmium,
    "Ir": Iridium,
    "Pt": Platinum,
    "Au": Gold,
    "Hg": Mercury,
    "Tl": Thallium,
    "Pb": Lead,
    "Bi": Bismuth,
    "Po": Polonium,
    "At": Astatine,
    "Rn": Radon,
    "Ce": Cerium,
    "Pr": Praseodymium,
    "Nd": Neodymium,
    "Pm": Promethium,
    "Sm": Samarium,
    "Eu": Europium,
    "Gd": Gadolinium,
    "Tb": Terbium,
    "Dy": Dysprosium,
    "Ho": Holmium,
    "Er": Erbium,
    "Tm": Thulium,
    "Yb": Ytterbium,
    "Lu": Lutentium,
    }
    

