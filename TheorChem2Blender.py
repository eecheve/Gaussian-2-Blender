import os
import sys
import stat
import json
import platform
import subprocess
#import memory_profiler #<-- !!! uncomment this line for benchmarking

import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

#utility modules
from gui.Utility import Utility
from gui.Coordinates import Coordinates
from gui.ScreenSizeManager import ScreenSizeManager
from gui.ProportionalContainer import ProportionalContainer

#gui modules
from gui.Instructions import Instructions
from gui.Information import Information
from gui.BlenderPath import BlenderPath
from gui.InputRegion import InputRegion
from gui.HighlighterRegion import HighlighterRegion
from gui.OutputRegion import OutputRegion
from gui.ConsoleRegion import ConsoleRegion
from gui.IonRegion import IonRegion
from gui.UnitCellRegion import UnitCellRegion
from gui.IonConventions import IonConventions
from gui.ActionsRegion import ActionsRegion
from gui.BondConventions import BondConventions

class TheorChem2BlenderTabSystem:
    def __init__(self):
        #utility
        self.coordinates = Coordinates() # To use the coordinates module
        
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
        Configures the root tkinter window with title and background, and
        starts it maximized (filling the screen without covering the OS
        taskbar/dock or hiding the window's minimize/maximize/close controls).
        """
        self.root = tk.Tk()
        #self.root.iconbitmap("icon.ico") #<---- for when I design a better Icon, 6/15/26; icon empty for now
        ScreenSizeManager.initialize(self.root)
        self.root.title("TheorChem2Blender")
        self.root.configure(bg="#e0e0e0")
        self.root.minsize(ScreenSizeManager.MIN_WIDTH, ScreenSizeManager.MIN_HEIGHT)
        self._maximize_window()

    def _maximize_window(self):
        """
        Starts the window maximized, in an OS-appropriate way.

        Windows has a native "zoomed" state that fills the screen while
        correctly leaving the taskbar and the window's own title bar controls
        (minimize/maximize/close) alone - that's the easy case. macOS doesn't
        expose an equivalent through Tkinter, so instead we size and position
        the window to fill the screen ourselves. A small offset at the top
        leaves room for macOS's own menu bar, which always stays on top and
        cannot be covered.
        """
        if self.current_os == "Windows":
            self.root.state("zoomed")
        else:  # macOS
            screen_width = ScreenSizeManager.get_screen_width()
            screen_height = ScreenSizeManager.get_screen_height()
            menu_bar_offset = 25  # leaves room for macOS's top menu bar
            self.root.geometry(f"{screen_width}x{screen_height - menu_bar_offset}+0+{menu_bar_offset}")

    def _configure_style(self):
        style = ttk.Style()
        style.theme_use("clam")

    def _initialize_notebook(self):
        """
        Lays out the root window as two stacked rows: the notebook (all the
        tabs) on top, and the shared console below it (added later, in
        _create_tabs). The row weights below are what keep that split at
        roughly a fixed ~75%/~25% proportion as the window is resized -
        see ScreenSizeManager for where those numbers come from.
        """
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=ScreenSizeManager.INFO_HEIGHT_WEIGHT
                                        + ScreenSizeManager.CONTENT_HEIGHT_WEIGHT)
        self.root.grid_rowconfigure(1, weight=ScreenSizeManager.CONSOLE_HEIGHT_WEIGHT)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=0, column=0, sticky="nsew")
   
    def place(self, region, **kwargs):
        """
        Places the specified region (frame) in the parent widget.

        :param region: The region/frame to be placed (e.g., actionReg, bPathReg).
        :param kwargs: Placement options such as grid(row=.., column=..).
        """
        region.frame.grid(**kwargs)
    
    def _build_tab_containers(self, tab, enable_content_scrolling=True):
        """
        Every tab is organized the same way: an instructions container fixed
        at ~5% of the window height, and a content container at ~70% (see
        ScreenSizeManager for those weights). The console - shared across
        every tab - lives outside the notebook entirely and takes whatever
        vertical space is left below it (see _initialize_notebook).

        :param tab: The tab's own ttk.Frame (already added to the notebook).
        :param enable_content_scrolling: Whether the content container should
                                          get its own scrollbar once its
                                          contents grow taller than the 70%
                                          it's allocated. Leave this on unless
                                          the tab's content specifically can't
                                          work inside a scrollable area (see
                                          the Actions tab below for why).
        :return: (info_container, content_container) - build the tab's real
                 widgets inside their .content_frame attributes.
        """
        tab.grid_columnconfigure(0, weight=1)
        info_container = ProportionalContainer(
            parent=tab, row=0, weight=ScreenSizeManager.INFO_HEIGHT_WEIGHT
        )
        content_container = ProportionalContainer(
            parent=tab, row=1, weight=ScreenSizeManager.CONTENT_HEIGHT_WEIGHT,
            enable_scrolling=enable_content_scrolling
        )
        return info_container, content_container

    def _create_tabs(self):
        # Tab 1: User Input
        self.input_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.input_tab, text="Input")
        self.input_info_container, self.input_content_container = self._build_tab_containers(self.input_tab)
        self.initialize_input_region(
            info_parent=self.input_info_container.content_frame,
            content_parent=self.input_content_container.content_frame
        )
        self.initialize_blender_region(self.input_content_container.content_frame)
        self.place(self.input_info, row=0, column=0, sticky="nsew")
        self.place(self.blender_path_region, row=0, column=0, padx=10, pady=10, sticky="ew")
        self.place(self.input_region, row=1, column=0, padx=2, pady=2, sticky="new")

        # Tab 2: Customization
        self.customization_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.customization_tab, text="Customization")
        self.customization_info_container, self.customization_content_container = \
            self._build_tab_containers(self.customization_tab)
        self.initialize_customization_region(
            info_parent=self.customization_info_container.content_frame,
            content_parent=self.customization_content_container.content_frame
        )
        self.place(self.custom_info, row=0, column=0, sticky="nsew")
        self.place(self.highlight_region, row=0, column=0, padx=2, pady=2, sticky="new")
        self.place(self.bond_conventions, row=1, column=0, padx=2, pady=2, sticky="new")

        # Tab 3: Ions
        self.ion_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.ion_tab, text="Ions")
        self.ion_info_container, self.ion_content_container = self._build_tab_containers(self.ion_tab)
        self.initialize_ionic_region(
            info_parent=self.ion_info_container.content_frame,
            content_parent=self.ion_content_container.content_frame
        )
        self.place(self.ion_info, row=0, column=0, sticky="nsew")
        self.place(self.ion_region, row=0, column=0, padx=2, pady=2, sticky="new")
        self.place(self.ion_conventions, row=1, column=0, padx=2, pady=2, sticky="new")

        # Tab 4: Unit cell
        self.unit_cell_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.unit_cell_tab, text="Unit Cells")
        self.unit_cell_info_container, self.unit_cell_content_container = \
            self._build_tab_containers(self.unit_cell_tab)
        self.initialize_unit_cell_region(
            info_parent=self.unit_cell_info_container.content_frame,
            content_parent=self.unit_cell_content_container.content_frame
        )
        self.place(self.unit_cell_info, row=0, column=0, sticky="nsew")
        self.place(self.unit_cell_region, row=0, column=0, sticky="new")
        self.notebook.tab(self.unit_cell_tab, state="disabled")

        # Tab 5: Output
        self.output_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.output_tab, text="Output")
        self.output_info_container, self.output_content_container = self._build_tab_containers(self.output_tab)
        self.initialize_output_region(
            info_parent=self.output_info_container.content_frame,
            content_parent=self.output_content_container.content_frame
        )
        self.place(self.output_info, row=0, column=0, sticky="nsew")
        self.place(self.output_region, row=0, column=0, padx=2, pady=2, sticky="new")

        # Tab 6: Actions
        # This one's content container is NOT scrollable, on purpose: its
        # buttons are deliberately anchored to the bottom-right corner using a
        # spacer row that expands to soak up all the container's leftover
        # height. That trick only works when the container is directly
        # grid-managed at a fixed size - inside a scrollable canvas, a
        # weight=1 spacer row has no fixed height to expand into, so the
        # anchoring would stop working.
        self.actions_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.actions_tab, text="Convert!")
        self.actions_info_container, self.actions_content_container = \
            self._build_tab_containers(self.actions_tab, enable_content_scrolling=False)

        actions_content = self.actions_content_container.content_frame
        actions_content.grid_rowconfigure(0, weight=1)     # spacer - pushes action_region down
        actions_content.grid_columnconfigure(0, weight=1)  # spacer - pushes action_region right
        actions_content.grid_columnconfigure(1, weight=1)
        actions_content.grid_columnconfigure(2, weight=1)

        self.initialize_actions_region(
            info_parent=self.actions_info_container.content_frame,
            content_parent=actions_content
        )
        self.place(self.actions_info, row=0, column=0, sticky="nsew")
        self.place(self.action_region, row=0, column=2, padx=2, pady=2, sticky="se")

        # Shared across every tab: the console sits below the notebook (not
        # inside any one tab), always occupying the full window width and
        # whatever vertical space the notebook doesn't use (see the row
        # weights configured in _initialize_notebook).
        self.initialize_console_region()
        self.place(self.console_region, row=1, column=0, sticky="nsew", pady=2, padx=2)

    def initialize_blender_region(self, parent):
        self.blender_path_region = BlenderPath(parent)
        self.str_blenderPath = self.blender_path_region.searchBlenderPath()
        self.blender_path_region.setBlenderPath(self.str_blenderPath)

    def initialize_input_region(self, info_parent, content_parent):
        self.input_info = Information(info_parent, instructions=Instructions.get("input"),
                                      title="Input Instructions", button_name="Input Help")
        self.input_region = InputRegion(content_parent, self.g2b_path,
                                        on_animation_toggle=self.handle_animation_toggle,
                                        on_input_type_change=self.handle_input_type_change) # Input Region

    def initialize_customization_region(self, info_parent, content_parent):
        self.custom_info = Information(info_parent, instructions=Instructions.get("customization"),
                                        title="Customization Instructions", button_name="Custom. Help")
        self.highlight_region = HighlighterRegion(content_parent) # Highlighter Region
        self.bond_conventions = BondConventions(content_parent)

    def initialize_ionic_region(self, info_parent, content_parent):
        self.ion_info = Information(info_parent, instructions=Instructions.get("ions"),
                                        title="Ion Instructions", button_name="Ions Help")
        self.ion_region = IonRegion(content_parent)
        self.ion_conventions = IonConventions(content_parent)

    def initialize_unit_cell_region(self, info_parent, content_parent):
        self.unit_cell_info = Information(info_parent, instructions=Instructions.get("unit_cell"),
                                          title="Unit Cell Instructions", button_name="Unit Cell Help")
        self.unit_cell_region = UnitCellRegion(content_parent)

    def initialize_output_region(self, info_parent, content_parent):
        self.output_info = Information(info_parent, instructions=Instructions.get("output"),
                                        title="Output Instructions", button_name="Output Help")
        self.output_region = OutputRegion(content_parent, self.g2b_path)

    def initialize_actions_region(self, info_parent, content_parent):
        self.actions_info = Information(info_parent, instructions=Instructions.get("actions"),
                                        title="Actions Instructions", button_name="Actions Help")
        self.action_region = ActionsRegion(parent=content_parent,
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
        self.ion_region.clear_radii_variables()

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
        b_path = self.blender_path_region.var_blenderPath.get() #blender path
        i_type = self.input_region.var_inputTypes.get() #input file type
        i_path = self.input_region.var_inputPath.get() #input specifications.
        i_names = self.input_region.lst_inputNames #files to convert
        is_anim = self.input_region.var_isAnimation.get() #is animation
        model_type = self.input_region.var_modelTypes.get() #model specifications
        hl_atoms = self.highlight_region.var_hlAtomList.get() #list of atoms to highlight
        hl_bonds = self.highlight_region.var_hlBondList.get() #list of bonds to highlight
        forced_bonds = self.highlight_region.var_forcedBondList.get() #list of bonds to enforce/overwrite
        custom_thresholds = self.highlight_region.get_custom_thresholds()  # list of dicts of custom bonds
        o_path = self.output_region.ent_outputPath.get() #output path
        o_type = self.output_region.var_outputTypes.get() #output type
        unit_cell_repeats = self.unit_cell_region.get_unit_cell_repeats() #get the x, y, z values of repeating the unit cell
        miller_indices = self.unit_cell_region.get_miller_indices() #gets the miller indices specified by the user
        polyhedra_centers = self.unit_cell_region.get_polyhedra_centers()
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
                                    hl_atoms, hl_bonds, forced_bonds, custom_thresholds, 
                                    unit_cell_repeats, miller_indices, polyhedra_centers) 
            else:
                for i in range(len(i_names)):
                    print("Batch converting", i+1, "of", len(i_names))
                    self.individual_convert(exec_loc, b_path, i_type, i_path, i_names[i], model_type,
                                        o_path, i_names[i].split(".")[0], o_type, is_ionic,
                                        unit_cell, str_ion_list, is_anim,
                                        hl_atoms, hl_bonds, forced_bonds, custom_thresholds, 
                                        unit_cell_repeats, miller_indices, polyhedra_centers)   
        else:
            print("Conversion aborted: input validation failed. Check the console for details.")

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
        unit_cell = self.unit_cell_region.int_unitCell.get()
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
                       o_name, o_type, is_ionic, unit_cell, str_ion_list, is_anim, 
                       hl_atoms, hl_bonds, forced_bonds, custom_thresholds, 
                       unit_cell_repeats, miller_indices, polyhedra_centers):
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
                                    is_ionic, unit_cell, str_ion_list, is_anim, 
                                    hl_atoms, hl_bonds, forced_bonds, custom_thresholds, 
                                    unit_cell_repeats, miller_indices, polyhedra_centers)
        subprocess.call([exec_loc, b_path])

    def input_to_json(self, i_type, i_path, i_name, model_type, o_path, o_name, o_type,
                    is_ionic, unit_cell, str_ion_list, is_anim, 
                    hl_atoms, hl_bonds, forced_bonds, custom_thresholds, 
                    unit_cell_repeats, miller_indices, polyhedra_centers):
        """
        Collects GUI input and writes it to a structured JSON file for Blender processing.

        :param json_path: Path to save the JSON configuration file
        """
        json_path = self.jsonConfigPath
        
        # customizable bond thresholds are a list of atom pairs, bond orders and bond thresholds
        thresholds_json = []
        if custom_thresholds:
            for item in custom_thresholds:
                pair = list(item["atom_pair"])  # ensure JSON serializable
                thresholds_json.append({
                    "atom_pair": pair,
                    "bond_order": int(item["bond_order"]),
                    "threshold": float(item["threshold"])
                })
        
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
            "animation_frames": [],
            "unit_cell_repeats": [],
            "miller_indices": [],
            "polyhedra_centers": polyhedra_centers if polyhedra_centers else []
        }

        # Add custom bond thresholds if there is any
        if thresholds_json:
                config["custom_bond_thresholds"] = thresholds_json

        # Add animation frames if applicable
        if is_anim:
            config["animation_frames"] = self.populate_animation_frames(i_type, self.input_region.lst_InputPaths)

        if unit_cell_repeats:
            repeats = self.populate_unit_cell_repeats(i_type, unit_cell_repeats)
            if repeats:
                config["unit_cell_repeats"] = repeats

        if miller_indices:
            m_indices = self.populate_miller_indices(i_type, miller_indices)
            if m_indices:
                config["miller_indices"] = m_indices

        # Write to JSON file
        with open(json_path, 'w') as f:
            json.dump(config, f, indent=4)

    def populate_unit_cell_repeats(self, i_type, unit_cell_repeats):
        """
        :param unit_cell_repeats: list of [x, y, z] rows, from
                                   UnitCellRegion.get_unit_cell_repeats() -
                                   one entry per unit cell growth the user added.
        :return: list of {"x":.., "y":.., "z":..} dicts, one per row, or None
                 if this input type doesn't support unit cell repeats at all.
        """
        if i_type != ".vasp":
            print("Unit cell repeats currently only allows cell duplication for .vasp files")
            print("This input will be ignored in the rendering")
            return None
        else:
            return [{"x": x, "y": y, "z": z} for x, y, z in unit_cell_repeats]

    def populate_miller_indices(self, i_type, miller_indices):
        """
        :param miller_indices: list of [h, k, l] rows, from
                                UnitCellRegion.get_miller_indices() - one
                                entry per Miller plane the user added.
        :return: list of {"h":.., "k":.., "l":..} dicts, one per row, or None
                 if this input type doesn't support Miller planes at all.
        """
        if i_type != ".vasp":
            print("Unit cell repeats currently only allows cell duplication for .vasp files")
            print("This input will be ignored in the rendering")
            return None
        else:
            return [{"h": h, "k": k, "l": l} for h, k, l in miller_indices]

    
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
        self.input_region.restrict_input_types_for_animation(is_animation)

    def handle_input_type_change(self, input_type):
        state = "normal" if input_type == ".vasp" else "disabled"
        self.notebook.tab(self.unit_cell_tab, state=state)
        if state == "disabled" and self.notebook.select() == str(self.unit_cell_tab):
            self.notebook.select(0) 

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
        num_atoms = len(raw_coords)
        digits = 3 if num_atoms >= 100 else 2
        indexed_coords = []
        for index, entry in enumerate(raw_coords, start=1):
            new_entry = entry.copy()  # Copy the original entry to avoid modifying it
            new_entry[0] = f"{entry[0]}{index:0{digits}d}" #to account for molecules between 100 and 999 atoms
            indexed_coords.append(new_entry)
        return indexed_coords
    
    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = TheorChem2BlenderTabSystem()
    app.run()
