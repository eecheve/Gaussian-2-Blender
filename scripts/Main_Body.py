import bpy
import sys
import os
from bpy import context, data
from math import radians, degrees
from mathutils import Vector
from typing import Callable, Dict, Optional

import importlib

blend_file_dir = os.path.dirname(bpy.data.filepath) #folder location for ReadMolecules00.blend
os.chdir(blend_file_dir) #ensuring the environment is in the correct file path
if blend_file_dir not in sys.path:
    sys.path.append(blend_file_dir)
    
import Receive_Parameters

class Main_Body(object):
    """
    Main class for managing molecule processing in Blender. Handles reading, refining, 
    and exporting molecular structures while managing parent-child relations and animations.
    """
    def __init__(self, i_file_type, i_folder_path, i_file_name, o_folder_path, o_file_name,
                 represent_type, o_file_type, is_ionic, unit_cell, ion_input_list, is_animation,
                 atom_hl_list, bond_hl_list, forced_bonds_list, custom_bond_thresholds, animation_frames,
                 unit_cell_repeats, miller_indices, polyhedra_centers):
        """
        Initializes the Main_Body class with input and output parameters.

        :param i_file_type: Type of input file (.xyz or .com).
        :param i_folder_path: Path to input folder.
        :param i_file_name: Name of the input file.
        :param o_folder_path: Path to output folder.
        :param o_file_name: Name of the output file.
        :param represent_type: Representation type for molecules.
        :param o_file_type: Output file format.
        :param is_ionic: "1"/"0" - whether the input has ions with specified charge/coordination.
        :param unit_cell: "1"/"0" - whether the input contains a unit cell.
        :param ion_input_list: list of dicts, one per specified ion, each with
                                "element"/"charge"/"coordination" keys.
        :param is_animation: Determines if animation should be applied.
        :param atom_hl_list: List of atoms to highlight.
        :param bond_hl_list: List of bonds to highlight.
        :param forced_bonds_list: List of bonds to overwrite.
        :param animation_frames: string list of all the atoms and cartesian coordinates for every frame.
        """
        self._readers: Dict[str, Callable[[], None]] = {
                    ".com":  self.Read_com_File,
                    ".xyz":  self.Read_xyz_File,
                    ".mol2": self.Read_mol2_File,
                    ".vasp": self.Read_vasp_File
                }
        
        self.i_file_type = i_file_type
        self.i_folder_path = i_folder_path
        self.i_file_name = i_file_name
        self.o_folder_path = o_folder_path
        self.o_file_name = o_file_name
        self.represent_type = represent_type
        self.o_file_type = o_file_type
        self.is_ionic = is_ionic
        self.unit_cell = unit_cell
        self.ion_input_list = ion_input_list
        self.is_animation = is_animation
        self.atom_hl_list = atom_hl_list
        self.bond_hl_list = bond_hl_list
        self.forced_bonds_list = forced_bonds_list
        self.custom_bond_thresholds = custom_bond_thresholds
        self.animation_frames = animation_frames
        self.unit_cell_repeats = unit_cell_repeats
        self.miller_indices = miller_indices
        self.polyhedra_centers = polyhedra_centers
        
        self.coords = []
        self.number_of_elements = 0
        self.unit_cell_points = []

        # Snapshot of connect_with_symbols taken right after the input file
        # is parsed (see the __main__ block), before any growth-cell export
        # mutates or extends it. Each growth-cell export restores from this
        # snapshot so replicated/forbidden-bond edits from one export never
        # leak into the next.
        self.base_connect_with_symbols = []
        
        self.names_and_pos = {}
        self.materials_dict = {}
        self.element_data = {}
        self.ion_data = {}
        self.connect_with_symbols = []
        self.bond_list = []
        self.ion_input = []
        self.elements_present = []
        
        self.imported_modules = {}  # Dictionary to store dynamically loaded modules
        self.load_modules()  # Load all modules dynamically


    def load_modules(self):
        """
        Dynamically imports all required modules and stores them in self.imported_modules.

        :return: None
        """
        MODULES_TO_IMPORT = [
            "Atom_Data", "Refine_Elements",
            "Create_Materials", "Primitives", "Export_Data", "Ions",
            "Instantiate_Molecules", "Animate", "Clear_Transforms",
            "XyzReader", "ComReader", "AtomHighlighter", "BondOverwriter", "VaspReader", "Mol2Reader",
            "BoundBoxBuilder", "UnitCellReplicator", "SceneCleaner"
        ]

        blend_file_dir = os.path.dirname(bpy.data.filepath)
        os.chdir(blend_file_dir)  # Set the correct file path
        if blend_file_dir not in sys.path:
            sys.path.append(blend_file_dir)

        for module in MODULES_TO_IMPORT:
            try:
                if module in self.imported_modules:
                    importlib.reload(self.imported_modules[module])  # Reload for live coding
                else:
                    self.imported_modules[module] = importlib.import_module(module)
            except ModuleNotFoundError as e:
                print(f"Module {module} not found: {e}")
            except Exception as e:
                print(f"Error while importing {module}: {e}")
    
    def get_module(self, module_name):
        """
        Retrieve and reload a module to apply the latest changes.

        :param module_name: (str) Name of the module to retrieve.
        :return: (module) The imported module.
        """
        if module_name not in self.imported_modules:
            self.imported_modules[module_name] = importlib.import_module(module_name)
        else:
            importlib.reload(self.imported_modules[module_name])  # Reload module <-- important
        return self.imported_modules[module_name]
    
    def Obtain_Coords_Connect(self, i_file_type):
        """
        Gets list of coordinates as a string with the atomic symbol and floats for each cartesian 
        coordinate, as well as the connectivity list with numerical inidices associated with each atom
        as well as the char specifying the atom type between connected pairs

        Calls:
            - `Read_com_File`, `Read_xyz_File`, `Read_mol2_File`, or `Read_vasp_File`,
              depending on `i_file_type`.

        :param i_file_type: (str) Type of input file (.com, .xyz, .mol2, or .vasp).
        :return: None
        """
        handler = self._readers.get(i_file_type)
        if handler is None:
            supported = ", ".join(sorted(self._readers.keys()))
            raise ValueError(f"Unsupported input type '{i_file_type}'. Supported: {supported}")
        handler()
    
    def Read_vasp_File(self):
        """
        Reads atomic data from a .vasp file.

        Calls:
        - `extract_coords_from_vasp_file` and `obtain_all_bond_orders` from `VaspReader` module.
        :return: None
        """
        print("1: Reading .vasp file ...")
        VaspReader = self.get_module("VaspReader")
        vaspReader = VaspReader.VaspReader()
        file_path = os.path.join(self.i_folder_path, self.i_file_name)
        self.coords = vaspReader.extract_coords_from_vasp_file(file_path)
        self.number_of_elements = len(self.coords)
        self.connect_with_symbols = vaspReader.obtain_all_bond_orders(self.coords)
        self.unit_cell_points = vaspReader.get_unit_cell_points(file_path)
    
    def Read_mol2_File(self):
        """
        Reads atomic data from a .mol2 file.

        Calls:
        - `extract_coords_from_mol2_file` and `obtain_all_bond_orders` from `Mol2Reader` module.
        :return: None
        """
        print("1: Reading .mol2 file ...")
        Mol2Reader = self.get_module("Mol2Reader")
        mol2Reader = Mol2Reader.Mol2Reader()
        file_path = os.path.join(self.i_folder_path, self.i_file_name)
        self.coords = mol2Reader.extract_coords_from_mol2_file(file_path)
        self.number_of_elements = len(self.coords)
        self.connect_with_symbols = mol2Reader.obtain_all_bond_orders(self.coords, file_path)
    
    def Read_xyz_File(self):
        """
        Reads atomic data from an .xyz file.

        Calls:
        - `extract_coords_from_xyz_file` and `obtain_all_bond_orders` from `XyzReader` module.
        :return: None
        """
        print("1: Reading .xyz file ...")
        XyzReader = self.get_module("XyzReader")
        xyzReader = XyzReader.XyzReader()

        try: # tries to get custom bond orders from user input
                if self.custom_bond_thresholds:
                    xyzReader.calculator.set_custom_thresholds(self.custom_bond_thresholds)
        except AttributeError:
            # If the running BondOrderCalculator doesn't yet have the setter
            print("BondOrderCalculator lacks set_custom_thresholds(); custom thresholds ignored.")


        file_path = os.path.join(self.i_folder_path, self.i_file_name)
        self.coords = xyzReader.extract_coords_from_xyz_file(file_path)
        self.number_of_elements = len(self.coords)
        self.connect_with_symbols = xyzReader.obtain_all_bond_orders(self.coords)
    
    def Read_com_File(self):
        """
        Reads atomic data from a .com file.

        Calls:
        - `extract_coords_from_com_file` and `obtain_all_bond_orders` from `ComReader` module.
        :return: None
        """
        print("1: Reading .com file ...")
        ComReader = self.get_module("ComReader")
        comReader = ComReader.ComReader()
        file_path = os.path.join(self.i_folder_path, self.i_file_name)
        self.coords = comReader.extract_coords_from_com_file(file_path)
        self.number_of_elements = len(self.coords)
        self.connect_with_symbols = comReader.obtain_all_bond_orders(self.coords, file_path)

    def Overwrite_Bonds_if_Needed(self):
        Overwriter = self.get_module("BondOverwriter")
        self.connect_with_symbols = Overwriter.overwrite_connectivity(self.forced_bonds_list, self.connect_with_symbols, self.coords)

    
    def Prepare_Atoms_and_Bonds(self):
        """
        Prepares atoms and bonds for the molecule.

        Calls:
        - `CreateDictionaryWithNamesAndPositions`, `GetElementsPresentInMolecule`, and `GetDataForExistingElements` from `Refine_Elements` module.
        - `CreateAndAssignMaterials` from `Create_Materials` module.
        :return: None
        """
        print("3: Checking present elements ...")
        Refine_Elements = self.get_module("Refine_Elements")
        Atom_Data = self.get_module("Atom_Data")
        self.names_and_pos = Refine_Elements.CreateDictionaryWithNamesAndPositions(self.coords, self.number_of_elements)
        self.elements_present = Refine_Elements.GetElementsPresentInMolecule(self.coords)
        print("3.1: elements present are", self.elements_present)
        self.element_data = Refine_Elements.GetDataForExistingElements(self.elements_present, Atom_Data.Elements)
        print("4: Creating and assigning materials ...")
        Create_Materials = self.get_module("Create_Materials")
        self.materials_dict = Create_Materials.CreateAndAssignMaterials(self.element_data)
        
    def Prepare_Ions(self):
        """
        Prepares ions for the molecule.

        Calls:
        - `GetDataForExistingElements` from `Refine_Elements` module.
        - `CreateIonDataFromInput` from `Ions` module.
        :return: None
        """
        Refine_Elements = self.get_module("Refine_Elements")
        Atom_Data = self.get_module("Atom_Data")
        Ions = self.get_module("Ions")
        self.ion_data = Refine_Elements.GetDataForExistingElements(self.elements_present, Atom_Data.IonicRadii)
        print("4: Checking for present ion specifications ...")
        if self.ion_input_list:
            print("4.1: ion_input_list is not empty")
            self.ion_input = Ions.CreateIonDataFromInput(self.ion_input_list)
        else:
            print("4: There are no ions with charge, coordination, and spin specified")
            self.ion_input = []    
    
    def Build_Molecule(self): 
        """
        Builds the molecule by instantiating elements and bonds.

        Calls:
        - `Instantiate` from `Instantiate_Molecules` module.
        :return: None
        """
        Instantiate_Molecules = self.get_module("Instantiate_Molecules")
        Instantiate_Molecules.Instantiate(self.is_ionic, self.represent_type, self.names_and_pos, 
                                          self.materials_dict, self.connect_with_symbols, self.element_data, 
                                          self.ion_data, self.ion_input, self.unit_cell)
        
    def Build_Unit_Cell(self):
        if self.unit_cell == "1":
            print("User has specified the input has a unit cell")
            if self.unit_cell_points:
                print("The input is a .vasp file containing three lattice vectors")
                BoundBoxBuilder = self.get_module("BoundBoxBuilder")
                BoundBoxBuilder.InstantiateBoundingBox(self.unit_cell_points, self.materials_dict)
            else:
                print("The input is NOT a .vasp file containing three lattice vectors")
                print("No unit cell boundaries will be rendered")
                return
        else:
            return
        
    def Build_Miller_Plane(self, miller_spec, repeats):
        """
        Renders a single Miller plane, clipped to the current export's
        supercell bounding box (or the bare unit cell, for repeats (1,1,1)).

        :param miller_spec: (dict) One entry from self.miller_indices,
                             e.g. {"h": 1, "k": 0, "l": 0}.
        :param repeats: (tuple) (nx, ny, nz) repeat counts for the
                         supercell currently being built.
        :return: None
        """
        if not self.unit_cell_points:
            return

        h = miller_spec.get("h", 0)
        k = miller_spec.get("k", 0)
        l = miller_spec.get("l", 0)

        if h == k == l == 0:
            return

        # Compute supercell bounding box points
        # unit_cell_points: [origin, a1_end, a2_end, a3_end, ...]
        origin = Vector(self.unit_cell_points[0])
        a1 = Vector(self.unit_cell_points[1]) - origin
        a2 = Vector(self.unit_cell_points[2]) - origin
        a3 = Vector(self.unit_cell_points[3]) - origin

        # Scale lattice vectors by this export's repeat counts
        nx, ny, nz = repeats
        a1_super = a1 * nx
        a2_super = a2 * ny
        a3_super = a3 * nz

        # Reconstruct supercell bound_box_points in the same format BoundBoxBuilder expects
        supercell_points = [
            origin,
            origin + a1_super,
            origin + a2_super,
            origin + a3_super,
            origin + a1_super + a2_super,
            origin + a1_super + a3_super,
            origin + a2_super + a3_super,
            origin + a1_super + a2_super + a3_super,
        ]

        MillerPlaneBuilder = self.get_module("MillerPlaneBuilder")
        MillerPlaneBuilder.InstantiateMillerPlane(
            supercell_points, h, k, l, self.materials_dict
        )

    def Build_Miller_Planes(self, repeats):
        """
        Renders every Miller plane listed in self.miller_indices onto the
        current export's supercell, each as its own named object (see
        MillerPlaneBuilder for the naming pattern). Does nothing if no
        Miller planes were specified.

        :param repeats: (tuple) (nx, ny, nz) repeat counts for the
                         supercell currently being built.
        :return: None
        """
        for miller_spec in self.miller_indices:
            self.Build_Miller_Plane(miller_spec, repeats)

    def Replicate_Unit_Cell(self, repeats) -> None:
        """
        Replicates the fully built and decorated unit cell into an
        nx, ny, nz supercell by duplicating and translating the
        unit-cell root Empty.

        :param repeats: (tuple) (nx, ny, nz) repeat counts for this export.
        :return: None
        """
        nx, ny, nz = repeats

        # Guard: no replication requested
        if (nx, ny, nz) == (1, 1, 1):
            return

        print("Duplicating unit cell according to", repeats)

        UnitCellReplicator = self.get_module("UnitCellReplicator")

        # 1. Compute lattice translation vectors (Cartesian)
        x_direction = Vector(self.unit_cell_points[1])
        y_direction = Vector(self.unit_cell_points[2])
        z_direction = Vector(self.unit_cell_points[3])

        # 2. Collect all scene objects except cameras and lights
        scene_objects = [
            obj for obj in bpy.context.scene.objects
            if obj.type not in {"CAMERA", "LIGHT"}
        ]

        # 3. Parent everything to a single unit-cell root Empty
        cell_root = UnitCellReplicator.parent_atoms_and_bonds_to_empty_object(
            scene_objects
        )

        # 4. Replicate along x, then y, then z (grid expansion)
        roots = [cell_root]
        UnitCellReplicator._expand_along_axis(roots, list(roots), nx, x_direction)
        UnitCellReplicator._expand_along_axis(roots, list(roots), ny, y_direction)
        UnitCellReplicator._expand_along_axis(roots, list(roots), nz, z_direction)

        # 5. Flatten hierarchy and remove Empty roots
        UnitCellReplicator.flatten_scene_hierarchy()
        UnitCellReplicator.delete_unit_cell_roots()
        print(f"Supercell generated with {len(roots)} unit-cell instances")

    def Link_Unit_Cells(self, repeats):
        """
        :param repeats: (tuple) (nx, ny, nz) repeat counts for this export.
        """
        if tuple(repeats) == (1, 1, 1):
            return

        UnitCellLinker = self.get_module("UnitCellLinker")
        result = UnitCellLinker.replicate_primitive_bonds(
            lattice_vectors=(
                self.unit_cell_points[1],
                self.unit_cell_points[2],
                self.unit_cell_points[3]
            )
        )
        atoms_in_scene = result.get("atoms_in_scene", {})
        replicated_bonds = result.get("replicated_bonds", [])
        if not replicated_bonds:
            print("Link_Unit_Cells: No replicated bonds detected")
            return

        Primitives = self.get_module("Primitives")
        Primitives.InstantiateBondsFromConnectivity(
            atoms_in_scene,
            self.materials_dict,
            replicated_bonds,
            self.unit_cell
        )

        self.connect_with_symbols.extend(replicated_bonds)
        print(f"Link_Unit_Cells: Instantiated and linked {len(replicated_bonds)} replicated bonds")

    def Parent_Bounding_Box(self):
        """Parents all unit cell wireframe edges to a single Empty at the origin."""
        BoundBoxBuilder = self.get_module("BoundBoxBuilder")
        BoundBoxBuilder.ParentBoundingBoxToEmpty()

    # def Delete_Forbidden_Bonds(self):
    #     bo = self.get_module("BondOverwriter")
    #     bo.delete_forbidden_bonds_from_scene(self.custom_bond_thresholds)

    def Delete_Forbidden_Bonds(self):
        """
        Deletes forbidden bond objects from the scene and removes the
        corresponding entries from connect_with_symbols so downstream
        steps (e.g. Build_Polyhedra) are not affected.
        """
        if not self.custom_bond_thresholds:
            return

        bo = self.get_module("BondOverwriter")
        forbidden_pairs = bo.get_forbidden_type_pairs(self.custom_bond_thresholds)
        if not forbidden_pairs:
            return

        bo.delete_forbidden_bonds_from_scene(self.custom_bond_thresholds)
        self.connect_with_symbols = bo.remove_forbidden_bonds_from_connectivity(
            self.connect_with_symbols, forbidden_pairs
        )

    def Build_Polyhedra(self):
        """
        Builds coordination polyhedra around all instances of each specified
        center element type. Does nothing if no centers are specified.
        Called after Link_Unit_Cells and Delete_Forbidden_Bonds so that
        inter-cell bonds are included in the neighbor search.
        """
        if not self.polyhedra_centers:
            return

        PolyhedronBuilder = self.get_module("PolyhedronBuilder")
        PolyhedronBuilder.BuildPolyhedra(
            self.polyhedra_centers,
            self.connect_with_symbols,
            self.materials_dict
        )
                                             
    def Manage_Parent_Relations(self):
        """
        Manages parent-child relationships for the molecule.

        Calls:
        - `Manage_Parent_Relations` from `Parent_Relations` module.
        :return: None
        """
        Parent_Relations = self.get_module("Parent_Relations")
        Parent_Relations.Manage_Parent_Relations(self.names_and_pos, self.connect_with_symbols)
    
    def Reset_Transforms(self):
        """
        Resets transforms for bonds and elements.

        Calls:
        - `get_bond_obj_list`, `Apply_Bond_Transforms`, and `Apply_Element_Transforms` from `Clear_Transforms` module.
        :return: None
        """
        Clear_Transforms = self.get_module("Clear_Transforms")
        self.bond_list = Clear_Transforms.get_bond_obj_list()
        print("6.1: Applying bond transforms")
        Clear_Transforms.Apply_Bond_Transforms(self.bond_list)
        print("6.2: Applying element transforms")
        Clear_Transforms.Apply_Element_Transforms(self.names_and_pos)
                
    def Export(self, file_name_suffix=""):
        """
        Exports the results to the specified file format.

        Calls:
        - `ExportSceneAs` from `Export_Data` module.

        :param file_name_suffix: (str) Appended to o_file_name before the
                                  extension, e.g. "_2x2x2" for a growth-cell
                                  export. Empty string leaves the name
                                  unchanged, matching the pre-growth-export
                                  behavior.
        :return: None
        """
        print("9: Exporting the results ...")
        Export_Data = self.get_module("Export_Data")
        Export_Data.ExportSceneAs(self.o_folder_path, self.o_file_name + file_name_suffix, self.o_file_type)
               
    def Highlight_Atoms(self):
        """
        Highlights specified atoms in the molecule.

        Calls:
        - `highlight_atom` from `AtomHighlighter` module.
        :return: None
        """
        print("7: highlighting atoms if info is present")
        if not self.atom_hl_list.strip():
            print("7.1: No atoms to highlight, skipping function.")
            return    
        AtomHighlighter = self.get_module("AtomHighlighter")
        atom_list = self.atom_hl_list.replace(" ", "").split(",")
        for atom in atom_list:
            print(f"7.1: highlighting {atom} atom")
            AtomHighlighter.highlight_atom(atom)
            
    def Highlight_Bonds(self):
        """
        Highlights specified bonds in the molecule.

        Calls:
        - `highlight_bond` from `AtomHighlighter` module.
        :return: None
        """
        separators = ['_', '-', '=', '#', '%']
        print("7: highlighting bonds if info is present")
        if not self.bond_hl_list.strip():
            print("7.2: No bonds to highlight, skipping function.")
            return
        AtomHighlighter = self.get_module("AtomHighlighter")
        bond_list = self.bond_hl_list.replace(" ", "").split(";")
        for bond in bond_list:
            for sep in separators:
                if sep in bond:
                    print(f"7.2: Highlighteing {bond} bond")
                    atom1, atom2 = bond.split(sep)
                    AtomHighlighter.highlight_bond(atom1, atom2)
                    break  

    def Animate(self):
        """
        Animates the molecule if animation is enabled.

        Calls:
        - `animate` from `Animate` module.
        :return: None
        """
        if self.is_animation == False:
            return
        else:
            Animate = self.get_module("Animate")
            Animate.animate(anim_frames=self.animation_frames, mode=self.o_file_type)
    
    def Manage_Export(self, file_name_suffix=""):
        """
        Manages the export process based on whether animation is enabled.

        Calls:
        - `Export` or `export_animation` from `Animate` module.

        :param file_name_suffix: (str) Appended to o_file_name before the
                                  extension, e.g. "_2x2x2" for a growth-cell
                                  export.
        :return: None
        """
        if self.is_animation == "false":
            self.Export(file_name_suffix)
        else:
            Animate = self.get_module("Animate")
            export_path = os.path.join(self.o_folder_path, self.o_file_name + file_name_suffix + self.o_file_type)
            Animate.export_animation(export_path)

    def Get_Growth_Specs(self):
        """
        Builds the list of (nx, ny, nz, file_name_suffix) tuples to export,
        one per entry in self.unit_cell_repeats.

        If self.unit_cell_repeats is empty - growth cells not in use - this
        returns a single implicit 1x1x1 spec with no filename suffix, so a
        plain unit-cell export looks exactly as it did before growth-cell
        support existed.

        :return: (list) [(nx, ny, nz, file_name_suffix), ...]
        """
        if not self.unit_cell_repeats:
            return [(1, 1, 1, "")]

        specs = []
        for repeat in self.unit_cell_repeats:
            nx = int(repeat.get("x", 1))
            ny = int(repeat.get("y", 1))
            nz = int(repeat.get("z", 1))
            file_name_suffix = f"_{nx}x{ny}x{nz}"
            specs.append((nx, ny, nz, file_name_suffix))
        return specs

    def Build_And_Export_Growth_Cell(self, nx, ny, nz, file_name_suffix):
        """
        Builds one full supercell (or the bare unit cell, for 1x1x1) from a
        clean scene and exports it. Called once per spec returned by
        Get_Growth_Specs - so once total when no growth cells are
        specified, or once per growth cell otherwise.

        The scene is cleared first because several downstream steps
        (UnitCellLinker, BoundBoxBuilder, UnitCellReplicator) tell primitive
        atoms/edges apart from replicated ones by Blender's auto-generated
        name suffixes - leftover objects from a previous export would
        corrupt that bookkeeping and leak into this export's selection.

        :param nx, ny, nz: (int) Repeat counts along each lattice direction.
        :param file_name_suffix: (str) Appended to the output filename so
                                  each growth-cell export gets its own file.
        :return: None
        """
        SceneCleaner = self.get_module("SceneCleaner")
        SceneCleaner.clear_scene()

        # Restore connect_with_symbols to its freshly-parsed state so bonds
        # added/removed by the previous growth-cell export don't carry over.
        self.connect_with_symbols = list(self.base_connect_with_symbols)

        self.Build_Molecule()
        self.Build_Unit_Cell()
        self.Highlight_Atoms()
        self.Highlight_Bonds()
        self.Animate()

        repeats = (nx, ny, nz)
        self.Replicate_Unit_Cell(repeats)
        self.Link_Unit_Cells(repeats)
        self.Delete_Forbidden_Bonds()
        self.Build_Polyhedra()
        self.Build_Miller_Planes(repeats)
        self.Parent_Bounding_Box()
        self.Manage_Export(file_name_suffix)

if __name__ == "__main__":
    json_config_path = os.path.join(blend_file_dir, "t2b_config.json")
    
    if not os.path.isfile(json_config_path):
        raise FileNotFoundError(f"Error: The file 't2b_config.json' was not found at {json_config_path}")
    
    params_data = Receive_Parameters.get_parameters_data(json_config_path)
    main_body_instance = Main_Body(params_data["i_file_type"],
                                   params_data["i_folder_path"],
                                   params_data["i_file_name"],
                                   params_data["o_folder_path"],
                                   params_data["o_file_name"],
                                   params_data["represent_type"],
                                   params_data["o_file_type"],
                                   params_data["is_ionic"],
                                   params_data["unit_cell"],
                                   params_data["ion_input_list"],
                                   params_data["is_animation"],
                                   params_data["atom_hl_list"],
                                   params_data["bond_hl_list"],
                                   params_data["forced_bonds_list"],
                                   params_data["custom_bond_thresholds"],
                                   params_data["animation_frames"],
                                   params_data["unit_cell_repeats"],
                                   params_data["miller_indices"],
                                   params_data["polyhedra_centers"])
    # Phase 1: parse the input file and resolve ionic/ion data once. None of
    # this depends on the growth-cell or Miller-plane settings, so it only
    # needs to run a single time no matter how many exports follow.
    main_body_instance.Obtain_Coords_Connect(main_body_instance.i_file_type)
    main_body_instance.Overwrite_Bonds_if_Needed()
    main_body_instance.Prepare_Atoms_and_Bonds()
    main_body_instance.Prepare_Ions()
    main_body_instance.base_connect_with_symbols = list(main_body_instance.connect_with_symbols)

    # Phase 2: build and export once per growth-cell spec (or once, bare,
    # if no growth cells were specified). Every Miller plane listed in
    # miller_indices is rendered onto each supercell.
    for nx, ny, nz, file_name_suffix in main_body_instance.Get_Growth_Specs():
        main_body_instance.Build_And_Export_Growth_Cell(nx, ny, nz, file_name_suffix)