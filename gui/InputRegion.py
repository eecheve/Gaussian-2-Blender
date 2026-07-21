import os
import re

import tkinter as tk
from tkinter import ttk

from gui.CreateTooltip import CreateTooltip
from gui.Utility import Utility
from gui import Styles

class InputRegion(object):
    """Section of the app that receives the input for the file(s) to convert"""
    def __init__(self, parent, initial_dir, on_animation_toggle=None, on_input_type_change=None):
        """
        Initializes the InputRegion by setting up variables, frame, canvas, and widgets.

        Parameters:
            parent (tk.Widget): The parent widget to attach the frame to.
            initial_dir (str): The initial directory path for file dialogs.
        """
        self.on_animation_toggle = on_animation_toggle #function to handle animation changes in the gui
        self.on_input_type_change = on_input_type_change #funtion to activate unit cell only for vasp input
        self.initialize_variables(initial_dir)
        self.setup_frame(parent)
        self.add_widgets()
        self.position_widgets()

    def initialize_variables(self, initial_dir):
        """
        Initializes instance variables related to input paths, file types, and model types.

        Parameters:
            initial_dir (str): The initial directory path for file dialogs.
        """
        self.var_inputPaths = tk.StringVar()
        self.var_inputNames = tk.StringVar()
        self.var_modelTypes = tk.StringVar()
        self.var_inputPath = tk.StringVar()

        self.var_isAnimation = tk.BooleanVar(value=False)

        self.lst_inputNames = []
        self.lst_InputPaths = []
        self.initial_dir = initial_dir
        self.var_inputTypes = tk.StringVar()
        self.var_inputTypes.set(".com")

    def clear_variables(self):
        """
        Clears all variables related to the input fields and resets default values.
        """
        self.var_inputTypes.set(".com")
        if self.on_input_type_change:
            self.on_input_type_change(".com")
        
        self.var_inputPaths.set("")
        self.var_inputNames.set("")
        self.var_modelTypes.set("")
        self.var_inputPath.set("")

        self.var_isAnimation.set(False)

        self.lst_inputNames.clear()
        self.lst_InputPaths.clear()
        self.var_inputTypes.set(".com")

    def setup_frame(self, parent):
        """
        Sets up the main frame for the input region.

        Parameters:
            parent (tk.Widget): The parent widget to attach the frame to.
        """
        self.frame = tk.LabelFrame(master=parent, padx=5, text="Input",
                                   fg=Styles.TITLE_FG, bg=Styles.PANEL_BG,
                                   relief=Styles.FRAME_RELIEF, borderwidth=Styles.FRAME_BORDERWIDTH)

    def add_widgets(self):
        """
        Adds and configures widgets like buttons, labels, dropdown menus, and checkboxes.

        These all live directly in self.frame now - no inner canvas/scrollbar.
        The tab's own content container (see TheorChem2Blender.py) already
        provides scrolling if this ever grows taller than the space available,
        so a second, nested scrollable area here was redundant.

        The frame is split into three bold-headed, separator-divided groups
        (matching the pattern from UnitCellRegion.py): Input Selection, then
        Representation, then Animation Settings - each its own responsibility.
        """
        self.lbl_inputSelection_header = tk.Label(master=self.frame, text="Input Selection",
                                                  bg=Styles.PANEL_BG, fg=Styles.TEXT_FG,
                                                  font=Styles.SECTION_HEADER_FONT)

        self.btn_setInputPath = tk.Button(text="set", master=self.frame)
        self.lbl_inputLabel = tk.Label(text="Input name(s)", bg=Styles.PANEL_BG, fg=Styles.TEXT_FG, master=self.frame)
        CreateTooltip(self.lbl_inputLabel, "Name(s) of the file(s) to be converted")

        self.lbl_fileType = tk.Label(text="Input type", bg=Styles.PANEL_BG, fg=Styles.TEXT_FG, master=self.frame)
        CreateTooltip(self.lbl_fileType, "List of file extensions currently accepted by the program")
        self.lst_inputTypes = [".com", ".xyz", ".mol2", ".vasp"]
        self.drp_inputTypes = tk.OptionMenu(self.frame,
                                        self.var_inputTypes,
                                        *self.lst_inputTypes,
                                        command=self.dropdown_callout)
        CreateTooltip(self.drp_inputTypes, "Choose one of the input types from this list")

        self.lbl_inputNames = tk.Label(textvariable=self.var_inputNames, master=self.frame,
                                       bg=Styles.PANEL_BG, fg=Styles.TEXT_FG)
        CreateTooltip(self.lbl_inputNames, "List of input files with the correct extension")

        self.btn_setInputName = tk.Button(text="set", master=self.frame, command=self.setInputName)
        CreateTooltip(self.btn_setInputName, "Select one or more input files")

        self.sep_selection_representation = ttk.Separator(master=self.frame, orient="horizontal")

        self.lbl_representation_header = tk.Label(master=self.frame, text="Representation",
                                                   bg=Styles.PANEL_BG, fg=Styles.TEXT_FG,
                                                   font=Styles.SECTION_HEADER_FONT)

        self.lbl_inputType = tk.Label(text="Model type", bg=Styles.PANEL_BG, fg=Styles.TEXT_FG, master=self.frame)
        CreateTooltip(self.lbl_inputType, "Different representational models supported by Gaussian2Blender")

        self.lst_modelTypes = ["Ball-and-Stick", "Stick-only", "Van-der-Waals"]
        self.var_modelTypes.set("Ball-and-Stick")
        self.drp_modelTypes = tk.OptionMenu(self.frame, self.var_modelTypes,
                                            *self.lst_modelTypes, command=self.dropdown_callout)
        CreateTooltip(self.drp_modelTypes, "Choose one of the model representation options from this list")

        self.sep_representation_animation = ttk.Separator(master=self.frame, orient="horizontal")

        self.lbl_animationSettings_header = tk.Label(master=self.frame, text="Animation Settings",
                                                      bg=Styles.PANEL_BG, fg=Styles.TEXT_FG,
                                                      font=Styles.SECTION_HEADER_FONT)

        self.chk_isAnimation = tk.Checkbutton(master=self.frame, text="is animation", bg=Styles.PANEL_BG, fg=Styles.TEXT_FG,
                                           variable=self.var_isAnimation, command=self.updateAnimationState)
        CreateTooltip(self.chk_isAnimation, "Check if the input files will serve as animation frames.")

    def reset_widget_bg_colors(self):
        """
        Resets the background color of all interactable widgets to their original state.
        """
        interactables = [self.btn_setInputPath, self.btn_setInputName,
                         self.drp_inputTypes, self.drp_modelTypes, self.chk_isAnimation]
        for interactable in interactables:
            Utility.revert_widget(interactable)

    def position_widgets(self):
        """
        Positions all the widgets inside the frame using grid layout.

        The frame is laid out as three groups - Input Selection,
        Representation, Animation Settings - each headed by a bold label and
        divided from the next by a horizontal separator, matching the
        pattern used in UnitCellRegion.py.
        """
        row = 0
        self.lbl_inputSelection_header.grid(row=row, column=0, columnspan=3, sticky="w", pady=(4, 0))
        row += 1
        self.lbl_fileType.grid(row=row, column=0, padx=(0, 4), pady=3, sticky="e")
        self.drp_inputTypes.grid(row=row, column=1, padx=(0, 4), pady=3, sticky="w")
        row += 1
        self.lbl_inputLabel.grid(row=row, column=0, padx=(0, 4), pady=3, sticky="e")
        self.lbl_inputNames.grid(row=row, column=1, padx=(0, 4), pady=3, sticky="w")
        self.btn_setInputName.grid(row=row, column=2, padx=(0, 4), pady=3)
        row += 1

        self.sep_selection_representation.grid(row=row, column=0, columnspan=3, sticky="ew", pady=6)
        row += 1

        self.lbl_representation_header.grid(row=row, column=0, columnspan=3, sticky="w", pady=(4, 0))
        row += 1
        self.lbl_inputType.grid(row=row, column=0, padx=(0, 4), pady=3, sticky="e")
        self.drp_modelTypes.grid(row=row, column=1, padx=(0, 4), pady=3, sticky="w")
        row += 1

        self.sep_representation_animation.grid(row=row, column=0, columnspan=3, sticky="ew", pady=6)
        row += 1

        self.lbl_animationSettings_header.grid(row=row, column=0, columnspan=3, sticky="w", pady=(4, 0))
        row += 1
        self.chk_isAnimation.grid(row=row, column=0, padx=(0, 4), pady=3, sticky="w")
 
    def updateAnimationState(self):
        """
        Updates the animation state based on the checkbox for animation files.
        Handles both .com and .xyz file types appropriately.
        """
        is_checked = self.var_isAnimation.get()

        if not is_checked:
            print("The files will not be treated as animation.")
            if self.on_animation_toggle:
                self.on_animation_toggle(False)
            return

        file_type = os.path.splitext(self.lst_inputNames[0])[1].lower()
        valid = True

        if file_type == ".com":
            if len(self.lst_inputNames) < 2:
                print("Error: There must be more than one .com file to implement animations.")
                valid = False
            else:
                print("At least two .com files are present. Make sure they have the same number of elements in the same order for the animation to work properly.")

        elif file_type == ".xyz":
            print("Note: Only one .xyz file is required for animation.")
            print("Make sure the .xyz file is a trajectory (contains multiple frames), or the animation will not work.")

        else:
            print(f"Unsupported file type: {file_type}. Please choose either .xyz or .com files for animations.")
            valid = False

        if not valid:
            self.var_isAnimation.set(False)

        if self.on_animation_toggle:
            self.on_animation_toggle(valid)

    def allFilesHaveSameValidExtension(self, file_paths):
        """
        Checks if all files in the list have the same valid extension.

        Parameters:
            file_paths (list): List of file paths to check.

        Returns:
            bool: True if all files have the same valid extension, False otherwise.
        """
        valid_extensions = {".com", ".xyz", ".mol2", ".vasp"}
        extensions = {os.path.splitext(path)[1].lower() for path in file_paths}
    
        if len(extensions) == 1 and extensions.pop() in valid_extensions:
            return True
        return False
            
    def setInputName(self):
        """
        Opens a file dialog to select files and updates the input names list.
        Filters files based on the selected input type and ensures they have the correct extension.
        """
        input_type = self.var_inputTypes.get()
        file_extension = f"*{input_type}"
        file_types = [(f"{input_type.upper()} files", file_extension), ("All files", "*.*")]

        input_examples_dir = os.path.join(self.initial_dir, "input_examples")
        str_paths = tk.filedialog.askopenfilenames(initialdir=input_examples_dir, filetypes=file_types)
    
        if not str_paths:
            return  # No files selected

        if self.allFilesHaveSameValidExtension(str_paths):
            self.updateInputNameList(str_paths)
            path = os.path.dirname(str_paths[0])
            print("##### SETTING INPUT FILES TO CONVERT ####")
            self.var_inputPath.set(path)
            for entry in str_paths:
                f_name = os.path.basename(entry)
                print("has correct file extension", f_name)
        else:
            print(f"Not all selected files have the '{input_type}' extension. Please select files with the '{input_type}' extension.")

                
    
    def isValidExtension(self, file_path):
        """
        Check if file has a valid extension.
        """
        valid_exts = {".com", ".xyz", ".mol2", ".vasp"}
        _, file_ext = os.path.splitext(file_path)
        return file_ext.lower() in valid_exts

    
    def isValidExtension2(self, file_path):
        """
        Checks if the file has a valid extension.

        Parameters:
            file_path (str): The file path to check.

        Returns:
            bool: True if the file has a valid extension, False otherwise.
        """
        _, file_ext = os.path.splitext(file_path)
        if file_ext.lower() == ".com":
            return True
        elif file_ext.lower() == ".xyz":
            return True
        elif file_ext.lower() == ".mol2":
            return True
        elif file_ext.lower() == ".vasp":
            return True
        return False
                
    def updateInputNameList(self, string_list):
        """
        Updates the list of input names and paths.

        Parameters:
            string_list (list): A list of file paths to update the input names and paths.
        """
        self.lst_inputNames.clear()
        self.lst_InputPaths.clear()
        self.var_inputNames.set("")
        s = ""
        for entry in string_list:
            n = os.path.basename(entry)
            e = n + "\n"
            s += e
            self.lst_inputNames.append(n)
            self.lst_InputPaths.append(entry)
        self.var_inputNames.set(s)

    def restrict_input_types_for_animation(self, is_animation):
        """
        Updates the list of selectable input file types based on whether animation is enabled.

        Parameters:
            is_animation (bool): Indicates whether the animation mode is active.

        Behavior:
            - Clears the current dropdown menu options.
            - Populates the menu with the appropriate list of file types.
            - Resets the selected input type if the current selection is no longer valid.
        """
        if is_animation:
            allowed = [".com", ".xyz"]
        else:
            allowed = [".com", ".xyz", ".mol2", ".vasp"]

        menu = self.drp_inputTypes["menu"]
        menu.delete(0, "end")
        for opt in allowed:
            menu.add_command(label=opt, command=lambda value=opt: self.var_inputTypes.set(value))

        if self.var_inputTypes.get() not in allowed:
            self.var_inputTypes.set(allowed[0])
    
    def dropdown_callout(self, event):
        """
        Prints a message when the dropdown selection is changed.

        Parameters:
            event (tk.Event): The event triggered by the dropdown selection.
        """
        if event in self.lst_inputTypes and self.on_input_type_change:
            self.on_input_type_change(event)