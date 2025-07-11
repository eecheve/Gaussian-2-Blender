import bpy
import sys
import os
from bpy import context, data
from math import radians, degrees

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
                 represent_type, o_file_type, str_ionic_cell, str_ion_input_list, str_is_animation,
                 atom_hl_list, bond_hl_list, forced_bonds_list):
        """
        Initializes the Main_Body class with input and output parameters.
        
        :param i_file_type: Type of input file (.xyz or .com).
        :param i_folder_path: Path to input folder.
        :param i_file_name: Name of the input file.
        :param o_folder_path: Path to output folder.
        :param o_file_name: Name of the output file.
        :param represent_type: Representation type for molecules.
        :param o_file_type: Output file format.
        :param str_ionic_cell: String representation of ionic cell data.
        :param str_ion_input_list: String representation of ion input list.
        :param str_is_animation: Determines if animation should be applied.
        :param atom_hl_list: List of atoms to highlight.
        :param bond_hl_list: List of bonds to highlight.
        :param forced_bonds_list: List of bonds to overwrite.
        """
        self.i_file_type = i_file_type
        self.i_folder_path = i_folder_path
        self.i_file_name = i_file_name
        self.o_folder_path = o_folder_path
        self.o_file_name = o_file_name
        self.represent_type = represent_type
        self.o_file_type = o_file_type
        self.str_ionic_cell = str_ionic_cell
        self.str_ion_input_list = str_ion_input_list
        self.str_is_animation = str_is_animation
        self.atom_hl_list = atom_hl_list
        self.bond_hl_list = bond_hl_list
        self.forced_bonds_list = forced_bonds_list
        
        self.coords = []
        self.number_of_elements = 0
        self.is_ionic=""
        self.unit_cell = []
        self.ion_input_list = []
        self.raw_coords = []
        self.raw_connect = []
        self.raw_key_frames = []
        
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
            "Atom_Data", "Import_Data", "Refine_Data", "Refine_Elements", 
            "Create_Materials", "Primitives", "Export_Data", "Ions", 
            "Instantiate_Molecules", "Raw_Parameters", "Animate", "Clear_Transforms",
            "XyzReader", "AtomHighlighter", "BondOverwriter"
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

                print(f"Successfully imported {module}")

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
            - `Read_com_File` and `Refine_com_File` if the input file type is .com.
            - `Read_xyz_File` if the input file type is .xyz.

        :param i_file_type: (str) Type of input file (.xyz or .com).
        :return: None
        """
        if i_file_type == ".com":
            self.Read_com_File()
            self.Refine_com_File()
        elif i_file_type == ".xyz":
            self.Read_xyz_File()
        elif i_file_type == ".mol2":
            self.Read_mol2_File()
    
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
        file_path = os.path.join(self.i_folder_path, self.i_file_name)
        self.coords = xyzReader.extract_coords_from_xyz_file(file_path)
        self.number_of_elements = len(self.coords)
        self.connect_with_symbols = xyzReader.obtain_all_bond_orders(self.coords)
    
    def Read_com_File(self):
        """
        Reads atomic data from a .com file.

        Calls:
        - `Set_Raw_Parameters` from `Raw_Parameters` module.
        :return: None
        """
        print("1: Reading .com file ...")  
        Raw_Parameters = self.get_module("Raw_Parameters")   
        raw_coords_connect = Raw_Parameters.Set_Raw_Parameters(self.i_folder_path, self.i_file_name)
        self.raw_coords = raw_coords_connect[0]
        self.raw_connect = raw_coords_connect[1]
               
    def Refine_com_File(self):
        """
        Refines extracted data from a .com file.

        Calls:
        - `RefineCoordList`, `RefineConnectivity`, and `AddElementSymbolsToConnecrivityList` from `Refine_Data` module.
        :return: None
        """
        print("2: Refining extracted data ...")
        Refine_Data = self.get_module("Refine_Data")
        self.coords = Refine_Data.RefineCoordList(self.raw_coords)
        self.number_of_elements = len(self.coords)
        print("2.1: number of elements in molecule is: ", self.number_of_elements)
        connect = Refine_Data.RefineConnectivity(self.raw_connect)
        self.connect_with_symbols = Refine_Data.AddElementSymbolsToConnecrivityList(connect, self.coords, self.number_of_elements)

    def Overwrite_Bonds_if_Needed(self):
        Overwriter = self.get_module("BondOverwriter")
        self.connect_with_symbols = Overwriter.overwrite_connectivity(self.forced_bonds_list, self.connect_with_symbols, self.coords)

    
    def Manage_Ionic_Information(self):
        """
        Manages ionic information for the molecule.

        Calls:
        - `rebuild_list` and `make_tuple_in_list` from `Refine_Data` module.
        :return: None
        """
        Refine_Data = self.get_module("Refine_Data")
        ionic_cell = Refine_Data.rebuild_list(self.str_ionic_cell)
        ionic_cell = Refine_Data.make_tuple_in_list(ionic_cell)
        self.is_ionic = ionic_cell[0][0]
        self.unit_cell = ionic_cell[0][1]
        self.ion_input_list = Refine_Data.rebuild_list(self.str_ion_input_list)
        self.ion_input_list = Refine_Data.make_tuple_in_list(self.ion_input_list)
    
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
                
    def Export(self):
        """
        Exports the results to the specified file format.

        Calls:
        - `ExportSceneAs` from `Export_Data` module.
        :return: None
        """
        print("9: Exporting the results ...")
        Export_Data = self.get_module("Export_Data")
        Export_Data.ExportSceneAs(self.o_folder_path, self.o_file_name, self.o_file_type)
               
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
        if self.str_is_animation == "0":
            return
        else:
            #blend_file_dir = os.path.dirname(__file__)  # Ensure this variable is defined
            blend_file_dir = bpy.path.abspath("//")  # Correctly gets the .blend file directory
            anim_frames_file = os.path.join(blend_file_dir, "animation_frames.txt")
            Animate = self.get_module("Animate")
            Animate.animate(anim_frames_path=anim_frames_file, mode=self.o_file_type)
    
    def Manage_Export(self):
        """
        Manages the export process based on whether animation is enabled.

        Calls:
        - `Export` or `export_animation` from `Animate` module.
        :return: None
        """
        if self.str_is_animation == "0":
            self.Export()
        else:
            Animate = self.get_module("Animate")
            export_path = os.path.join(self.o_folder_path, self.o_file_name + self.o_file_type)
            Animate.export_animation(export_path)
    
if __name__ == "__main__":
    params_file_path = os.path.join(blend_file_dir, "parameters.txt")
    
    if not os.path.isfile(params_file_path):
        raise FileNotFoundError(f"Error: The file 'parameters.txt' was not found at {params_file_path}")
    
    params_data = Receive_Parameters.get_parameters_data(params_file_path)
    main_body_instance = Main_Body(params_data["i_file_type"],
                                   params_data["i_folder_path"],
                                   params_data["i_file_name"],
                                   params_data["o_folder_path"],
                                   params_data["o_file_name"],
                                   params_data["represent_type"],
                                   params_data["o_file_type"],
                                   params_data["str_ionic_cell"],
                                   params_data["str_ion_input_list"],
                                   params_data["str_is_animation"],
                                   params_data["atom_hl_list"],
                                   params_data["bond_hl_list"],
                                   params_data["forced_bonds_list"])
    main_body_instance.Obtain_Coords_Connect(main_body_instance.i_file_type)
    main_body_instance.Overwrite_Bonds_if_Needed()
    main_body_instance.Manage_Ionic_Information()
    main_body_instance.Prepare_Atoms_and_Bonds()
    main_body_instance.Prepare_Ions()
    main_body_instance.Build_Molecule()
    main_body_instance.Highlight_Atoms()
    main_body_instance.Highlight_Bonds()
    main_body_instance.Animate()
    main_body_instance.Manage_Export()