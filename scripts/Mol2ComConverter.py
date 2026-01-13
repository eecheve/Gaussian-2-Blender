from typing import List, Tuple, Dict

def parse_mol2(mol2_path: str):
    """
    Parse a MOL2 file and return:
      atoms: list of [symbol, x, y, z]
      bonds: list of (i, j, order) with 1-based atom indices
    """
    atoms: List[List[float | str]] = []
    bonds: List[Tuple[int, int, float]] = []

    in_atom = False
    in_bond = False

    with open(mol2_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            if line.startswith("@<TRIPOS>ATOM"):
                in_atom = True
                in_bond = False
                continue
            if line.startswith("@<TRIPOS>BOND"):
                in_atom = False
                in_bond = True
                continue
            if line.startswith("@<TRIPOS>"):
                # some other section
                in_atom = False
                in_bond = False
                continue

            if in_atom:
                # MOL2 ATOM line:
                # ID  Name  x  y  z  Type  (rest...)
                parts = line.split()
                if len(parts) < 6:
                    continue  # malformed
                x = float(parts[2])
                y = float(parts[3])
                z = float(parts[4])
                atom_type = parts[5]   # e.g., "S.O2", "C.3", "O.3"
                symbol = atom_type.split('.')[0]  # take "S" from "S.O2"
                atoms.append([symbol, x, y, z])

            elif in_bond:
                # MOL2 BOND line:
                # ID  a1  a2  type
                parts = line.split()
                if len(parts) < 4:
                    continue
                a1 = int(parts[1])
                a2 = int(parts[2])
                btype = parts[3]  # "1", "2", "3", "ar", ...
                order = mol2_bond_type_to_gaussian_order(btype)
                bonds.append((a1, a2, order))

    return atoms, bonds


def mol2_bond_type_to_gaussian_order(btype: str) -> float:
    """
    Map MOL2 bond type to Gaussian bond order.
    """
    btype = btype.lower()
    if btype == "1":
        return 1.0
    if btype == "2":
        return 2.0
    if btype == "3":
        return 3.0
    if btype == "ar":
        return 1.5
    if btype == "am":
        return 1.0
    # fallback: treat unknown as single
    return 1.0



def build_gaussian_connectivity(
    num_atoms: int,
    bonds: List[Tuple[int, int, float]]
) -> Dict[int, List[Tuple[int, float]]]:
    """
    From a list of (i, j, order) bonds, build a connectivity dict suitable for Gaussian.
    Each bond appears exactly once, on the line of the lower-index atom.
    Returns dict: atom_index -> list of (other_atom_index, order)
    """
    conn = {i: [] for i in range(1, num_atoms + 1)}

    seen = set()  # to be extra safe if MOL2 has duplicates
    for i, j, order in bonds:
        if i == j:
            continue
        a, b = sorted((i, j))
        if (a, b) in seen:
            continue
        seen.add((a, b))
        conn[a].append((b, order))

    for i in conn:
        conn[i].sort(key=lambda t: t[0])

    return conn


def write_gaussian_com_from_mol2(
    mol2_path: str,
    com_path: str,
    charge: int = 0,
    multiplicity: int = 1,
    header_lines: List[str] | None = None,
):
    """
    Build a Gaussian .com (geom=connectivity) from a MOL2 file.
    
    - mol2_path: input MOL2 file
    - com_path: output Gaussian .com file
    - charge, multiplicity: Gaussian's "0 1" line
    - header_lines: lines to write between %... and the blank line before charge/mult.
      Example:
        ["%mem=64GB",
         "%nprocshared=20",
         "%chk=dimethyl_dithionate.chk",
         "# opt 6-31+g(d) geom=connectivity m062x"]
    """
    atoms, bonds = parse_mol2(mol2_path)
    num_atoms = len(atoms)
    connectivity = build_gaussian_connectivity(num_atoms, bonds)

    if header_lines is None:
        header_lines = [
            "# opt 6-31+g(d) geom=connectivity m062x"
        ]

    with open(com_path, 'w') as f:
        # You can customize these % lines or pass them in if you want
        # For now, just write the route section from header_lines
        for line in header_lines:
            f.write(line.rstrip() + "\n")

        f.write("\n")
        f.write("Generated from MOL2\n")
        f.write("\n")

        # Charge and multiplicity
        f.write(f"{charge} {multiplicity}\n")

        # Coordinates
        for symbol, x, y, z in atoms:
            f.write(f" {symbol:<2s}  {x: .6f}  {y: .6f}  {z: .6f}\n")

        # Blank line separating coords and connectivity
        f.write("\n")

        # Connectivity block
        for i in range(1, num_atoms + 1):
            neighbors = connectivity.get(i, [])
            if not neighbors:
                f.write(f" {i}\n")
                continue

            line_parts = [str(i)]
            for j, order in neighbors:
                line_parts.append(str(j))
                line_parts.append(f"{order:.1f}")
            f.write(" " + " ".join(line_parts) + "\n")

        f.write("\n")

header = [ 
    "%rwf=temp_file_name.rwf", 
    "%nosave", 
    "%mem=64GB", 
    "%nprocshared=20", 
    "%chk=temp_file_name.chk", 
    "# opt 6-31+g(d) geom=connectivity m062x", 
]

molecules_to_add = [
    "taxol", "geosmin", "absicic-acid", "cholesterol", "retinol", "testosterone", "estradiol", "cortisone", 
    "progesterone", "vitamin-b1", "vitamin-d2", "vitamin-d3", "b-carotene", "squalene", "zeaxanthin", "phytol", 
    "geranylgeraniol", "lanosterol", "stearidonic-acid", "Eicosatetraenoic-acid", "Eicosapentaenoic-acid",
    "riboflavin", "fad", "folic-acid", "tribenzylamine"
]

benchmark_path = "C:\\Users\\User\\G2B\\Gaussian-2-Blender\\input_examples\\benchmarking2\\"

i = benchmark_path + "taxol.mol2"
o = benchmark_path + "taxol.com"
write_gaussian_com_from_mol2( 
    mol2_path=i, 
    com_path=o, 
    charge=0, 
    multiplicity=1, 
    header_lines=header)

for molecule in molecules_to_add:
    i = benchmark_path + molecule + ".mol2"
    o = benchmark_path + molecule + ".com"
    write_gaussian_com_from_mol2(mol2_path=i, com_path=o, charge=0, multiplicity=1, header_lines=header)
