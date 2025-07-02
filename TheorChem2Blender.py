import os
import sys
import stat
import platform
import subprocess

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

#utility modules
from gui.Utility import Utility
from gui.Coordinates import Coordinates
from gui.Tutorial import Tutorial

#gui modules
from gui.Information import Information
from gui.BlenderPath import BlenderPath
from gui.InputRegion import InputRegion
from gui.WalkthroughRegion import WalkthroughRegion
from gui.OutputRegion import OutputRegion
from gui.ConsoleRegion import ConsoleRegion
from gui.IonRegion import IonRegion
from gui.IonConventions import IonConventions
from gui.ActionsRegion import ActionsRegion
from gui.BondConventions import BondConventions
from gui.HighlighterRegion import HighlighterRegion

class TheorChem2Blender:
    '''
    GUI built using the tkinter library to convert computational chemistry files into 3D modeling files.
    This application facilitates the conversion of various computational chemistry files into Blender-compatible
    3D representations.
    '''
    def __init__(self):
        """
        Initializes the TheorChem2Blender GUI, setting up the main application window and regions.
        """
        self.current_os = platform.system()
        self.root = tk.Tk()
        self._initialize_g2b_path()
        self.def_scriptsPath = os.path.join(self.g2b_path, "scripts")
        self._configure_root()
        self._configure_style()
        self._initialize_regions()
        self.place_regions()
        self.initialize_single_tutorial()
        self.initialize_animation_tutorial()
    
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
        else:  # Running as a script
            self.g2b_path = os.path.dirname(os.path.realpath(__file__))
    
    def _configure_root(self):
        """
        Configures the root tkinter window with title, dimensions, and resizability settings.
        """
        self.root.title("TheorChem2Blender")
        #self.root.iconbitmap(Utility.resource_path("icon.ico")) #comment line while TheorChem2Blender.py is inside gui folder
        #self.root.iconbitmap(script_dir+"\\icon.ico") #uncomment line when TheorChem2Blender.py is outside gui folder
        self.root.geometry('800x800')
        #self.root.resizable(0,0)
        self.root.configure(bg="#e0e0e0")

    def _configure_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        #style.configure

    def place(self, region, **kwargs):
        """
        Places the specified region (frame) in the parent widget.

        :param region: The region/frame to be placed (e.g., actionReg, bPathReg).
        :param kwargs: Placement options such as grid(row=.., column=..).
        """
        region.frame.grid(**kwargs)
        
    def _initialize_regions(self):
        """
        Initializes various UI regions required for user interaction within the application.
        """
        self.coordinates = Coordinates() # To use the coordinates module
        self.instructions = Information(self, self.root) # Instructions Region
        
        # Blender Path Region
        self.bPathReg = BlenderPath(self.root)
        self.str_blenderPath = self.bPathReg.searchBlenderPath()
        self.bPathReg.setBlenderPath(self.str_blenderPath)

        self.inputReg = InputRegion(self.root, self.g2b_path) # Input Region
        self.guideReg = WalkthroughRegion(self.root) # Walkthrough Region
        self.highlightReg = HighlighterRegion(self.root) # Highlighter Region
        self.outputReg = OutputRegion(self.root, self.g2b_path) # Output Region
        self.ionReg = IonRegion(self.root) # Ion Region
        
        #Conventions
        self.codeReg = IonConventions(self.root)
        self.bondCodes = BondConventions(self.root)

        #Action Region
        self.actionReg = ActionsRegion(parent=self.root, 
                                       on_reset=self.reset_to_defaults, 
                                       on_convert=self.convert)
        
        self.consoleReg = ConsoleRegion(self.root) # Console Region

    def place_regions(self):
        """
        Places all initialized regions into the tkinter grid layout.
        """
        self.place(self.instructions, row=0, column=0, columnspan=3, pady=2, padx=2, sticky="ew")
        self.place(self.bPathReg, row=1, column=0, columnspan=3, pady=2, padx=2, sticky="w")
        self.place(self.inputReg, row=2, column=0, rowspan=2, padx=2, pady=2, sticky="W")
        self.place(self.guideReg, row=2, column=1, columnspan=2, padx=2, pady=2)
        self.place(self.outputReg, row=3, column=1, sticky="SW", columnspan=2)
        self.place(self.highlightReg, row=4, column=0, padx=2, pady=2)
        self.place(self.ionReg, row=5, column=0, padx=2, pady=2, sticky="W", rowspan=2)
        self.place(self.codeReg, row=5, column=1, padx=2, pady=2, sticky="W")
        self.place(self.bondCodes, row=5, column=2, padx=2, pady=2, sticky="W")
        self.place(self.actionReg, row=6, column=1, pady=2, columnspan=2, sticky="se")
        self.place(self.consoleReg, row=7, column=0, columnspan=3, pady=2, padx=2)

    def initialize_single_tutorial(self):
        """
        Sets up the step-by-step tutorial for a single molecule conversion process.

        calls:
          - `InputRegion`, `OutputRegion`, `ActionRegion`
        """
        text_descriptions = [
            "1. Click on the 'set' button to select one or more files to convert",
            "2. Select the representational model for your 3D model", 
            "3. Choose the output type for your 3D model",
            "4. Click on 'convert' to start the conversion process",
            "5. Click on 'reset' to remove the current button highlights"
        ]
    
        # Step 2: Define the buttons that the user needs to press in order
        action_buttons = [
            self.inputReg.btn_setInputName,  # Button for selecting input file(s)
            self.inputReg.drp_modelTypes,  # Dropdown to select model type
            self.outputReg.drp_outputTypes,  # Dropdown to select output type
            self.actionReg.btn_convert       # Button to start the conversion process
        ]
    
        # Step 3: Initialize the tutorial system with the buttons, descriptions, and actions
        self.single_convert_tutorial = Tutorial(
            action_buttons=action_buttons,  # List of buttons to be pressed in order
            descriptions=text_descriptions,  # Corresponding descriptions for each step
            walkthroughRegion=self.guideReg  # Walkthrough region to display tutorial instructions
        )
        
    def initialize_animation_tutorial(self):
        """
        Sets up the tutorial for animated molecular conversions.

        Modules called: `InputRegion`, `OutputRegion`, `ActionRegion`
        """
        text_descriptions = [
            "1. Click on the 'set' button to select one or more files to convert",
            "2. Select the representational model for your 3D model",
            "3. Click on the 'is animation' checkbox",
            "NOTE1: make sure all the input files have the same extension",
            "NOTE2: make sure all the input files have the same atoms in the same order",
            "4. Choose the output type for your 3D model",
            "5. Click on 'convert' to start the conversion process",
            "6. Click on 'reset' to remove the current button highlights"
        ]
    
        # Step 2: Define the buttons that the user needs to press in order
        action_buttons = [
            self.inputReg.btn_setInputName,  # Button for selecting input file(s)
            self.inputReg.drp_modelTypes,  # Dropdown to select model type (currently not used)
            self.inputReg.chk_isAnimation,
            self.outputReg.drp_outputTypes,  # Dropdown to select output type (currently not used)
            self.actionReg.btn_convert       # Button to start the conversion process
        ]
    
        # Step 3: Initialize the tutorial system with the buttons, descriptions, and actions
        self.animation_convert_tutorial = Tutorial(
            action_buttons=action_buttons,  # List of buttons to be pressed in order
            descriptions=text_descriptions,  # Corresponding descriptions for each step
            walkthroughRegion=self.guideReg  # Walkthrough region to display tutorial instructions
        ) 
        
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
        
    def reset_to_defaults(self):
        """
        Resets the GUI components to their default states, clearing paths, input selections, and highlights.

        Calls:
        - `clear` functions from the following modules:
        `BlenderPath`, `OutputRegion`, `InputRegion`, `IonRegion`, `ConsoleRegion`, `Information`, `Tutorial`
        """
        self.bPathReg.var_blenderPath.set(self.str_blenderPath)
        self.outputReg.var_outputPath.set(self.outputReg.def_outputPath)
        self.inputReg.clear_variables()
        self.highlightReg.reset_highlighter_options()
        self.inputReg.reset_widget_bg_colors()
        self.ionReg.clear_variables()
        self.consoleReg.clear_content()
        self.guideReg.revert_text_to_default()
        self.single_convert_tutorial.reset_buttons_to_default()
        self.animation_convert_tutorial.reset_buttons_to_default()

    def get_blender_exec_name(self):
        """
        Returns the expected Blender executable filename based on the operating system

        :return: Platform-specific Blender executable name
        """
        return "blender.exe" if platform.system() == "Windows" else "Blender"
    
    def exceptions_test_passed(self, b_path, i_names, o_path):
        """
        Validates input parameters for the conversion process.
    
        This function checks whether the required paths and files are valid 
        before running the `convert_manager` function.

        Args:
            b_path (str): Path to the Blender executable.
            i_names (list): List of input file names to convert.
            o_path (str): Output directory path.

        Returns:
            bool: True if all tests pass, False otherwise.
        """
        tests = [
            #(not Utility.findFile(self.get_blender_exec_name(), b_path), 
            #    "The assigned blender path does not contain the blender executable"),
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
            i_type,
            i_path,
            i_name,
            o_path,
            o_name,
            model_type,
            o_type,
            str(is_ionic),
            str(unit_cell),
            str_ion_list,
            is_anim,
            hl_atoms,
            hl_bonds,
            forced_bonds
        ]
        Utility.append_lines_to_file(params_script, lines)
    
    def overwrite_animation_frames(self, is_anim):
        """
        If the input represents an animation, prepares animation frame data for conversion.

        Calls:
        - `append_lines_to_file` from `Utility` module.
        """
        if is_anim:
            anim_frames = os.path.join(self.g2b_path, "scripts", "animation_frames.txt")
            if not os.path.exists(anim_frames):
                raise FileNotFoundError(f"Cannot find 'parameters.txt' at {anim_frames}")
            if len(self.inputReg.lst_InputPaths) > 1: #at least two input files to be read
                print(self.inputReg.lst_InputPaths, "Input paths list is: ")
                frames_list = self.coordinates.combine_animation_frames(self.inputReg.lst_InputPaths)
            frames_list_strings = [' '.join(map(str, frame)) for frame in frames_list] #converting touple list into string
            Utility.append_lines_to_file(anim_frames, frames_list_strings)
        
    def individual_convert(self, exec_loc, b_path, i_type, i_path, i_name, model_type, o_path, 
                       o_name, o_type, is_ionic, unit_cell, str_ion_list, is_anim, hl_atoms, hl_bonds, forced_bonds):
        """ 
        Function to execute bat file that communicates with blender's python API 

        Calls:
        - `self.overwrite_animation_frames` and `self.overwrite_parameters_script`.
    
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
        self.overwrite_animation_frames(is_anim) #only does this if is_anim is True
        self.overwrite_parameters_script(i_type, i_path, i_name, model_type, o_path, o_name, o_type, 
                                    is_ionic, unit_cell, str_ion_list, is_anim, hl_atoms, hl_bonds, forced_bonds)
        subprocess.call([exec_loc, b_path])
    
    def assign_ionic_params(self):
        """
        Retrieves and formats ionic parameters for molecular conversion.

        Calls:
        - `int_hasIons.get`, `lst_ions`, and `int_unitCell.get` from `IonRegion` module
        """
        is_ionic = self.ionReg.int_hasIons.get()
        if not is_ionic:
            is_ionic = "0"
            str_ionList = "---"
        unit_cell = self.ionReg.int_unitCell.get()
        if not unit_cell:
            unit_cell = "0"
        ion_list = self.ionReg.lst_ions
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
        b_path = self.bPathReg.var_blenderPath.get() #blender path
        i_type = self.inputReg.var_inputTypes.get() #input file type
        i_path = self.inputReg.var_inputPath.get() #input specifications.
        i_names = self.inputReg.lst_inputNames #files to convert
        model_type = self.inputReg.var_modelTypes.get() #model specifications
        o_path = self.outputReg.ent_outputPath.get() #output path
        o_type = self.outputReg.var_outputTypes.get() #output type
        is_anim = self.inputReg.var_isAnimation.get() #is animation
        hl_atoms = self.highlightReg.var_hlAtomList.get() #list of atoms to highlight
        hl_bonds = self.highlightReg.var_hlBondList.get() #list of bonds to highlight
        forced_bonds = self.highlightReg.var_forcedBondList.get() #list of bonds to enforce/overwrite
        if self.exceptions_test_passed(b_path, i_names, o_path): 
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

    def help_single_convert(self):
        """
        Starts the step-by-step tutorial for single molecule conversion.

        Calls:
        - `start_tutorial` from `Tutorial` module.
        """
        self.animation_convert_tutorial.reset_buttons_to_default()
        self.single_convert_tutorial.start_tutorial()

    def help_animation_convert(self):
        """
        Starts the step-by-step tutorial for animation-based molecular conversions.

        Calls:
        - `start_tutorial` from `Tutorial` module.
        """
        self.single_convert_tutorial.reset_buttons_to_default()
        self.animation_convert_tutorial.start_tutorial()
            
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TheorChem2Blender()
    app.run()