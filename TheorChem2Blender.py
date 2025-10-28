import os
import sys
import stat
import json
import platform
import subprocess
import memory_profiler

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

#utility modules
from gui.Utility import Utility
from gui.Coordinates import Coordinates

#gui modules
from gui.Instructions import Instructions
from gui.Information import Information
from gui.BlenderPath import BlenderPath
from gui.InputRegion import InputRegion
from gui.HighlighterRegion import HighlighterRegion
from gui.OutputRegion import OutputRegion
from gui.ConsoleRegion import ConsoleRegion
from gui.IonRegion import IonRegion
from gui.IonConventions import IonConventions
from gui.ActionsRegion import ActionsRegion
from gui.BondConventions import BondConventions

class TheorChem2BlenderTabSystem:
    def __init__(self):
        #utility
        self.coordinates = Coordinates() # To use the coordinates module
        #self.xyzReader = XyzReader()
        
        #system vatiables and paths
        self.current_os = platform.system()
        self._initialize_g2b_path()
        self._initialize_scripts_path()
        
        #related to the gui
        self._configure_root()
        self._configure_style()
        self._initialize_notebook()

        #related to the tabs
        self._create_tabs()
   
    def _initialize_g2b_path(self):
        """
        Determines the file path where the application is running, distinguishing between executable and script mode.
        """
        if getattr(sys, 'frozen', False):  # Check if running as an executable
            if self.current_os == "Darwin": #macOS
                #the pyinstaller bundles gui and scripts inside Resources/ (see TheorChem2Blender_macOS.spec)
                bundle_dir = os.path.dirname(sys.executable)
                self.g2b_path = os.path.abspath(os.path.join(bundle_dir, "../Resources"))
                sys.path.insert(0, self.g2b_path)
            else: #Works well for Windows, don't know if it works for Linux really.
                self.g2b_path = os.path.dirname(sys.executable)
                print(self.g2b_path)
        else:  # Running as a script
            self.g2b_path = os.path.dirname(os.path.realpath(__file__))
    
    def _initialize_scripts_path(self):
        self.def_scriptsPath = os.path.join(self.g2b_path, "scripts")
        self.jsonConfigPath = os.path.join(self.def_scriptsPath, "t2b_config.json")
    
    def _configure_root(self):
        """
        Configures the root tkinter window with title, dimensions, and resizability settings.
        """
        self.root = tk.Tk()
        self.root.title("TheorChem2Blender")
        self.root.geometry("800x600")
        self.root.configure(bg="#e0e0e0")
    
    def _configure_style(self):
        style = ttk.Style()
        style.theme_use("clam")

    def _initialize_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=0, sticky="nsew")
   
    def place(self, region, **kwargs):
        """
        Places the specified region (frame) in the parent widget.

        :param region: The region/frame to be placed (e.g., actionReg, bPathReg).
        :param kwargs: Placement options such as grid(row=.., column=..).
        """
        region.frame.grid(**kwargs)
    
    def _create_tabs(self):
        # Tab 1: User Input
        self.input_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.input_tab, text="Input")
        self.initialize_input_region(self.input_tab)
        self.initialize_blender_region(self.input_tab)
        self.place(self.input_info, row=0, column=0, columnspan=3, pady=2, padx=2, sticky="ew")
        self.place(self.blender_path_region, row=1, column=0, padx=10, pady=10, sticky="ew")
        self.place(self.input_region, row=2, column=0, rowspan=2, padx=2, pady=2, sticky="W")

        # Tab 2: Customization
        self.customization_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.customization_tab, text="Customization")
        self.initialize_customization_region(self.customization_tab)
        self.place(self.custom_info, row=0, column=0, columnspan=3, pady=2, padx=2, sticky="ew")
        self.place(self.highlight_region, row=1, column=0, padx=2, pady=2)
        self.place(self.bond_conventions, row=2, column=0, padx=2, pady=2)

        # Tab 3: Ions
        self.ion_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.ion_tab, text="Ions")
        self.initialize_ionic_region(self.ion_tab)
        self.place(self.ion_info, row=0, column=0, columnspan=3, pady=2, padx=2, sticky="ew")
        self.place(self.ion_region, row=1, column=0, padx=2, pady=2, sticky="W")
        self.place(self.ion_conventions, row=2, column=0, padx=2, pady=2)

        # Tab 4: Output
        self.output_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.output_tab, text="Output")
        self.initialize_output_region(self.output_tab)
        self.place(self.output_info, row=0, column=0, columnspan=3, pady=2, padx=2, sticky="ew")
        self.place(self.output_region, row=1, column=0, padx=2, pady=2, sticky="W")

        # Tab 5: Actions
        self.actions_tab = ttk.Frame(self.notebook)
        self.actions_tab.grid_rowconfigure(0, weight=0) # actions_info
        self.actions_tab.grid_rowconfigure(1, weight=1) # spacer
        self.actions_tab.grid_rowconfigure(2, weight=0) # action_region
        self.actions_tab.grid_columnconfigure(0, weight=1)
        self.actions_tab.grid_columnconfigure(1, weight=1)
        self.actions_tab.grid_columnconfigure(2, weight=1)
        self.notebook.add(self.actions_tab, text="Convert!")
        self.initialize_actions_region(self.actions_tab)
        self.place(self.actions_info, row=0, column=0, columnspan=3, pady=2, padx=2, sticky="ew")
        self.place(self.action_region, row=2, column=2, padx=2, pady=2, sticky="se")

        # In all tabs:
        self.initialize_console_region()
        self.place(self.console_region, row=3, column=0, columnspan=3, pady=2, padx=2)

    def initialize_blender_region(self, parent):
        self.blender_path_region = BlenderPath(parent)
        self.str_blenderPath = self.blender_path_region.searchBlenderPath()
        self.blender_path_region.setBlenderPath(self.str_blenderPath)

    def initialize_input_region(self, parent):
        self.input_info = Information(parent, instructions=Instructions.get("input"), 
                                      title="Input Instructions", button_name="Input Help")
        self.input_region = InputRegion(parent, self.g2b_path, 
                                        on_animation_toggle=self.handle_animation_toggle) # Input Region

    def initialize_customization_region(self, parent):
        self.custom_info = Information(parent, instructions=Instructions.get("customization"),
                                        title="Customization Instructions", button_name="Custom. Help")
        self.highlight_region = HighlighterRegion(parent) # Highlighter Region
        self.bond_conventions = BondConventions(parent)

    def initialize_ionic_region(self, parent):
        self.ion_info = Information(parent, instructions=Instructions.get("ions"),
                                        title="Ion Instructions", button_name="Ions Help")
        self.ion_region = IonRegion(parent)
        self.ion_conventions = IonConventions(parent)

    def initialize_output_region(self, parent):
        self.output_info = Information(parent, instructions=Instructions.get("output"),
                                        title="Output Instructions", button_name="Output Help")
        self.output_region = OutputRegion(parent, self.g2b_path)

    def initialize_actions_region(self, parent):
        self.actions_info = Information(parent, instructions=Instructions.get("actions"),
                                        title="Actions Instructions", button_name="Actions Help")
        self.action_region = ActionsRegion(parent=parent, 
                                       on_reset=self.reset_to_defaults,
                                       on_convert=self.convert,
                                       g2b_path=self.g2b_path,
                                       current_os=self.current_os)
        
    def initialize_console_region(self):
        self.console_region = ConsoleRegion(self.root)
        
    
    def reset_to_defaults(self):
        """
        Resets the GUI components to their default states, clearing paths, input selections, and highlights.

        Calls:
        - `clear` functions from the following modules:
        `BlenderPath`, `OutputRegion`, `InputRegion`, `IonRegion`, `ConsoleRegion`, `Information`, `Tutorial`
        """
        self.blender_path_region.var_blenderPath.set(self.str_blenderPath)
        self.output_region.var_outputPath.set(self.output_region.def_outputPath)
        self.input_region.clear_variables()
        self.highlight_region.reset_highlighter_options()
        self.input_region.reset_widget_bg_colors()
        self.ion_region.clear_variables()

    def convert(self):
        """
        Determines the operating system and executes the appropriate script for converting molecular data.

        Calls:
        - self.convert_manager
        """
        #current_os = platform.system()
        linux_exe_path = os.path.join(self.g2b_path, "scripts", "ReadMolecules.sh")
        windows_exe_path = os.path.join(self.g2b_path, "scripts", "ReadMolecules.bat")

        if self.current_os == "Windows":
            # Windows OS detected
            print(f"Detected {self.current_os} OS. Proceeding with conversion...")
            self.convert_manager(windows_exe_path)
        else:
            # Non Windows OS detected
            print(f"Detected {self.current_os} OS. Proceeding with conversion...")            
            st = os.stat(linux_exe_path) # Add executable permission to the .sh script
            os.chmod(linux_exe_path, st.st_mode | stat.S_IEXEC)
            self.convert_manager(linux_exe_path)

    def convert_manager(self, exec_loc):
        """
        Manages the process of converting input files to 3D object files using Blender's API.

        Calls:
        - `self.exceptions_test_passed`.
        - `self.assign_ionic_params`.
        - `self.individual_convert`.


        :param exec_loc: the path to the executable that will communicate with MainBody.py that handles the Blender part.

        The function performs the following steps:
        1. Collects necessary paths and parameters for the conversion process.
        2. Validates the inputs using the `exceptions_test_passed` function.
        3. If validation succeeds: 
        3.1. Retrieves ionic parameters
        3.2. Iterates through the list of input files and calls the `individual_convert` function to process each file.
        4. If validation fails, outputs relevant error messages to the console.

        """
        anim_frames_path = os.path.join(self.g2b_path, "scripts", "animation_frames.txt")
        b_path = self.blender_path_region.var_blenderPath.get() #blender path
        i_type = self.input_region.var_inputTypes.get() #input file type
        i_path = self.input_region.var_inputPath.get() #input specifications.
        i_names = self.input_region.lst_inputNames #files to convert
        is_anim = self.input_region.var_isAnimation.get() #is animation
        model_type = self.input_region.var_modelTypes.get() #model specifications
        hl_atoms = self.highlight_region.var_hlAtomList.get() #list of atoms to highlight
        hl_bonds = self.highlight_region.var_hlBondList.get() #list of bonds to highlight
        forced_bonds = self.highlight_region.var_forcedBondList.get() #list of bonds to enforce/overwrite
        o_path = self.output_region.ent_outputPath.get() #output path
        o_type = self.output_region.var_outputTypes.get() #output type
        if self.exceptions_test_passed(i_names, o_path): 
            params = self.assign_ionic_params()
            is_ionic = params[0]
            unit_cell = params[1]
            ion_list = params[2]
            str_ion_list = params[3]
            if is_anim:
                print("Converting main molecule for animation")
                self.individual_convert(exec_loc, b_path, i_type, i_path, i_names[0], model_type,
                                    o_path, i_names[0].split(".")[0], o_type, is_ionic,
                                    unit_cell, str_ion_list, is_anim,
                                    hl_atoms, hl_bonds, forced_bonds) 
            else:
                for i in range(len(i_names)):
                    print("Batch converting", i+1, "of", len(i_names))
                    self.individual_convert(exec_loc, b_path, i_type, i_path, i_names[i], model_type,
                                        o_path, i_names[i].split(".")[0], o_type, is_ionic,
                                        unit_cell, str_ion_list, is_anim,
                                        hl_atoms, hl_bonds, forced_bonds)   
        else:
            print("Cannot convert input to animation, check console for errors")

    def exceptions_test_passed(self, i_names, o_path):
        """
        Validates input parameters for the conversion process.
    
        This function checks whether the required paths and files are valid 
        before running the `convert_manager` function.

        Args:
            i_names (list): List of input file names to convert.
            o_path (str): Output directory path.

        Returns:
            bool: True if all tests pass, False otherwise.
        """
        tests = [
            (i_names is None or not i_names, 
                "Please select at least one input file to convert"),
            (not o_path, 
                "Please paste a path for the output file"),
            (not os.path.exists(o_path), 
                "Please paste a path that exists"),
            (not os.path.isdir(o_path), 
                "Please paste a folder path instead of a file path")
        ]
        for condition, error_message in tests:
            if condition:
                print(error_message)
                return False
        return True
    
    def assign_ionic_params(self):
        """
        Retrieves and formats ionic parameters for molecular conversion.

        Calls:
        - `int_hasIons.get`, `lst_ions`, and `int_unitCell.get` from `IonRegion` module
        """
        # 7/10/25 note: I wrote this function 4 years ago and I don't remember what it does.
        # I cannot erase it or change is as it will break several things that I cannot be bothered to write again.
        is_ionic = self.ion_region.int_hasIons.get()
        if not is_ionic:
            is_ionic = "0"
            str_ionList = "---"
        unit_cell = self.ion_region.int_unitCell.get()
        if not unit_cell:
            unit_cell = "0"
        ion_list = self.ion_region.lst_ions
        str_ionList = ""
        if is_ionic == 1:
            is_ionic = "1"
            if ion_list:
                for ion in ion_list:
                    charge_coord = ion.var_chargeCoord.get().strip("()")
                    lst_pair = charge_coord.split(',')
                    str_charge = lst_pair[0]
                    str_coord = lst_pair[1]
                    str_ionList += "("
                    str_ionList += ion.var_element.get()
                    str_ionList += "_"
                    str_ionList += str_charge
                    str_ionList += "_"
                    str_ionList += str_coord
                    str_ionList += ")_"
                str_ionList = str_ionList[:-1]
                print(str_ionList)
            else:
                str_ionList = "---"
        else:
            str_ionList = "---"
        return is_ionic, unit_cell, ion_list, str_ionList

    #@Utility.redirect_print_to_log(logfile='C:\\Users\\User\\G2B\\Gaussian-2-Blender\\output\\output.log') # to save the prints elsewhere
    #@Utility.announce_conversion # to specify which molecule is being converted
    #@Utility.time_function # to measure how much time this function runs
    #@memory_profiler.profile # to measure memory usage
    def individual_convert(self, exec_loc, b_path, i_type, i_path, i_name, model_type, o_path, 
                       o_name, o_type, is_ionic, unit_cell, str_ion_list, is_anim, hl_atoms, hl_bonds, forced_bonds):
        """ 
        Function to execute bat file that communicates with blender's python API 
   
        :param excec_loc: path to the ReadMolecules.bat file which communicates with python
        :param b_path: location of the blender executable
        :param i_path: list of input specifications
        :param i_name: list of input names to be converted into 3D objects
        :param model_type: type of model to export
        :param o_path: output path
        :param o_name: output names
        :param o_type: output type
        :param is_ionic: boolean specifyig wether the input is ionic
        :param unit_cell: boolean specifying whether the input contains a unit cell
        :param str_ion_list: list of strings containing all the ions within the input
        :param is_anim: boolean determining if input list is to be treated as animation
        """
        self.input_to_json(i_type, i_path, i_name, model_type, o_path, o_name, o_type, 
                                    is_ionic, unit_cell, str_ion_list, is_anim, hl_atoms, hl_bonds, forced_bonds)
        subprocess.call([exec_loc, b_path])

    def input_to_json(self, i_type, i_path, i_name, model_type, o_path, o_name, o_type,
                    is_ionic, unit_cell, str_ion_list, is_anim, hl_atoms, hl_bonds, forced_bonds):
        """
        Collects GUI input and writes it to a structured JSON file for Blender processing.

        :param json_path: Path to save the JSON configuration file
        """
        json_path = self.jsonConfigPath
        config = {
            "input": {
                "type": i_type,
                "paths": i_path,
                "names": i_name
            },
            "output": {
                "path": o_path,
                "name": o_name,
                "type": o_type
            },
            "model": {
                "type": model_type
            },
            "flags": {
                "is_ionic": is_ionic,
                "unit_cell": unit_cell,
                "is_anim": is_anim
            },
            "ions": str_ion_list,
            "highlight": {
                "atoms": hl_atoms,
                "bonds": hl_bonds
            },
            "forced_bonds": forced_bonds,
            "animation_frames": []
        }

        # Add animation frames if applicable
        if is_anim:
            config["animation_frames"] = self.populate_animation_frames(i_type, self.input_region.lst_InputPaths)

        # Write to JSON file
        with open(json_path, 'w') as f:
            json.dump(config, f, indent=4)

    def populate_animation_frames(self, i_type, input_paths):
        """
        Generates animation frame data based on input type and paths.

        :param i_type: File type (.com or .xyz)
        :param input_paths: List of input file paths
        :return: List of frame strings
        """
        if i_type == ".com":
            if len(input_paths) > 1:
                frames_list = self.coordinates.combine_animation_frames(input_paths)
                return [' '.join(map(str, frame)) for frame in frames_list]
            else:
                raise ValueError("At least two .com files are required for animation.")
        elif i_type == ".xyz":
            if len(input_paths) != 1:
                raise ValueError("Only one .xyz file should be provided for animation input.")
            xyz_path = input_paths[0]
            frames = self.extract_all_frames(xyz_path)
            combined = self.combine_xyz_animation_frames(frames)
            return [' '.join(map(str, frame)) for frame in combined]
        else:
            raise ValueError(f"Animations with {i_type} files are not supported at the moment.")
    
    def overwrite_animation_frames(self, is_anim, input_type):
        """
        If the input represents an animation, prepares animation frame data for conversion.

        Calls:
        - `append_lines_to_file` from `Utility` module.
        """
        if is_anim:
            anim_frames = os.path.join(self.g2b_path, "scripts", "animation_frames.txt")
            if not os.path.exists(anim_frames):
                raise FileNotFoundError(f"Cannot find 'parameters.txt' at {anim_frames}")
            if input_type == ".com":
                if len(self.input_region.lst_InputPaths) > 1: #at least two input files to be read
                    frames_list = self.coordinates.combine_animation_frames(self.input_region.lst_InputPaths)
                frames_list_strings = [' '.join(map(str, frame)) for frame in frames_list] #converting touple list into string
                Utility.append_lines_to_file(anim_frames, frames_list_strings)
            elif input_type == ".xyz":
                if len(self.input_region.lst_InputPaths) != 1:
                    raise ValueError("Only one .xyz file should be provided for animation input.")
                xyz_path = self.input_region.lst_InputPaths[0]
                frames = self.extract_all_frames(xyz_path) 
                combined = self.combine_xyz_animation_frames(frames)
                frame_strings = [' '.join(map(str, frame)) for frame in combined]
                Utility.append_lines_to_file(anim_frames, frame_strings)
            else:
                raise ValueError(f"Animations with {input_type} files are not supported at the moment")

    def overwrite_parameters_script(self, i_type, i_path, i_name, model_type, o_path, o_name, o_type, 
                              is_ionic, unit_cell, str_ion_list, is_anim, hl_atoms, hl_bonds, forced_bonds):
        """
        overwrites bat script to handle the export or animation of molecules

        Calls:
        - `clear_file_contents` and `append_lines_to_file` from `Utility` module.
    
        :param i_path: Input file path
        :param i_name: Input file name
        :param model_type: Type of model to export
        :param o_path: Output directory path
        :param o_name: Output file name
        :param o_type: Output type
        :param is_ionic: Whether the input is ionic
        :param unit_cell: Whether the input contains a unit cell
        :param str_ion_list: List of ions in string format
        :param is_anim: boolean determining if input list is to be treated as animation
        """
        params_script = os.path.join(self.g2b_path, "scripts", "parameters.txt")

        if not os.path.exists(params_script):
            raise FileNotFoundError(f"Cannot find 'parameters.txt' at {params_script}")

        Utility.clear_file_contents(params_script)
        lines = [
            i_type, i_path, i_name,
            o_path, o_name, model_type, o_type,
            str(is_ionic), str(unit_cell), str_ion_list,
            is_anim,
            hl_atoms, hl_bonds, forced_bonds
        ]
        Utility.append_lines_to_file(params_script, lines)
    
    
    def handle_animation_toggle(self, is_animation):
        self.output_region.restrict_output_types_for_animation(is_animation)
        self.input_region.restrict_input_types_for_animation(is_animation) #<-----

    def extract_all_frames(self, xyz_file_path):
        """
        Extracts all coordinate frames from a multi-frame XYZ animation file.

        :param xyz_file_path: (str) Path to the XYZ file containing multiple animation frames.
        :return: (list) A list of frames, where each frame is a list of [atom, x, y, z] entries.
        """
        with open(xyz_file_path, 'r') as f:
            lines = f.readlines()

        frames = []
        i = 0
        while i < len(lines):
            try:
                num_atoms = int(lines[i].strip())
            except ValueError:
                raise ValueError(f"Invalid atom count at line {i+1}")
            
            frame_lines = lines[i+2:i+2+num_atoms]
            if len(frame_lines) != num_atoms:
                raise ValueError("Incomplete frame detected.")
            
            frame = []
            for line in frame_lines:
                parts = line.split()
                if len(parts) != 4:
                    raise ValueError("Invalid coordinate line.")
                atom, x, y, z = parts
                frame.append([atom, float(x), float(y), float(z)])
            frames.append(frame)
            i += num_atoms + 2
        return frames

    def combine_xyz_animation_frames(self, frames):
        """
        Combines atomic coordinates from multiple XYZ animation frames into a single list.

        :param frames: (list) A list of frames, where each frame is a list of [atom, x, y, z] entries.
        :return: (list) A list of tuples, where each tuple contains the atom ID and its coordinates across all frames.
        """
        if not frames:
            return []

        # Assign indices to atoms in the first frame
        indexed_atoms = self.assign_indices(frames[0])
        num_atoms = len(indexed_atoms)
        combined = []

        for i in range(num_atoms):
            atom_id = indexed_atoms[i][0]
            coords = []
            for frame in frames:
                coords.extend(frame[i][1:])  # x, y, z
            combined.append((atom_id, *coords))
        return combined
    
    def assign_indices(self, raw_coords):
        """
        Assigns unique two-digit indices to atomic symbols.

        :param raw_coords: (list) List of raw coordinates.
        :return: (list) A list of lists with atomic symbols assigned a unique two-digit index.
        """
        indexed_coords = []
        for index, entry in enumerate(raw_coords, start=1):
            new_entry = entry.copy()  # Copy the original entry to avoid modifying it
            new_entry[0] = f"{entry[0]}{index:02d}"
            indexed_coords.append(new_entry)
        return indexed_coords
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = TheorChem2BlenderTabSystem()
    app.run()
