import os
import re

import tkinter as tk

from gui.CreateTooltip import CreateTooltip
from gui.Utility import Utility

class InputRegion(object):
    """Section of the app that receives the input for the file(s) to convert"""
    def __init__(self, parent, initial_dir, on_animation_toggle=None):
        """
        Initializes the InputRegion by setting up variables, frame, canvas, and widgets.

        Parameters:
            parent (tk.Widget): The parent widget to attach the frame to.
            initial_dir (str): The initial directory path for file dialogs.
        """
        self.on_animation_toggle = on_animation_toggle #function to handle animation changes in the gui
        self.initialize_variables(initial_dir)
        self.setup_frame(parent)
        self.setup_canvas()
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
                                   fg="blue", bg="#e0e0e0",
                                   relief=tk.GROOVE, borderwidth=2)

    def setup_canvas(self):
        """
        Sets up the canvas with a scrollable frame for the input region.
        """
        self.canvas = tk.Canvas(self.frame, bg="#e0e0e0")
        self.frm_inside = tk.Frame(self.canvas, bg="#e0e0e0")
        self.scrl_frame = tk.Scrollbar(master=self.frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrl_frame.set)
        self.scrl_frame.pack(side="right", fill="y")
        self.canvas.pack(side="left")
        self.canvas.create_window((0, 0), window=self.frm_inside, anchor='nw')
        self.frm_inside.bind("<Configure>", self.canvasConfig)

    def add_widgets(self):
        """
        Adds and configures widgets like buttons, labels, dropdown menus, and checkboxes.
        """
        self.btn_setInputPath = tk.Button(text="set", master=self.frm_inside)
        self.lbl_inputLabel = tk.Label(text="Input name(s)", bg="#e0e0e0", fg='black', master=self.frm_inside)
        CreateTooltip(self.lbl_inputLabel, "Name(s) of the file(s) to be converted")
        
        self.lbl_fileType = tk.Label(text="Input type", bg="#e0e0e0", fg='black', master=self.frm_inside)
        CreateTooltip(self.lbl_fileType, "List of file extensions currently accepted by the program")
        self.lst_inputTypes = [".com", ".xyz", ".mol2"] #planning on reading .mol files in the future as well.
        self.drp_inputTypes = tk.OptionMenu(self.frm_inside, 
                                        self.var_inputTypes, 
                                        *self.lst_inputTypes,
                                        command=self.dropdown_callout)
        CreateTooltip(self.drp_inputTypes, "Choose one of the input types from this list")

        self.lbl_inputNames = tk.Label(textvariable=self.var_inputNames, master=self.frm_inside, 
                                       bg="#e0e0e0", fg='black')
        CreateTooltip(self.lbl_inputNames, "List of input files with the correct extension")
        
        self.btn_setInputName = tk.Button(text="set", master=self.frm_inside, command=self.setInputName)
        CreateTooltip(self.btn_setInputName, "Select one or more input files")
        
        self.lbl_inputType = tk.Label(text="Model type", bg="#e0e0e0", fg='black', master=self.frm_inside)
        CreateTooltip(self.lbl_inputType, "Different representational models supported by Gaussian2Blender")
        
        self.lst_modelTypes = ["Ball-and-Stick", "Stick-only", "Van-der-Waals"]
        self.var_modelTypes.set("Ball-and-Stick")
        self.drp_modelTypes = tk.OptionMenu(self.frm_inside, self.var_modelTypes,
                                            *self.lst_modelTypes, command=self.dropdown_callout)
        CreateTooltip(self.drp_modelTypes, "Choose one of the model representation options from this list")
        
        self.chk_isAnimation = tk.Checkbutton(master=self.frm_inside, text="is animation", bg="#e0e0e0", fg='black',
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
        """
        self.lbl_fileType.grid(row=1, column=0)
        self.drp_inputTypes.grid(row=1, column=1)
        self.lbl_inputLabel.grid(row=2, column=0)
        self.lbl_inputNames.grid(row=2, column=1, sticky="w")
        self.btn_setInputName.grid(row=2, column=2)
        self.lbl_inputType.grid(row=3, column=0, sticky="e")
        self.drp_modelTypes.grid(row=3, column=1, sticky="w")
        self.chk_isAnimation.grid(row=4, column=0)
 
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
        valid_extensions = {".com", ".xyz", ".mol2"}
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
        elif file_ext.lower() == ".mol2": #currently in the making
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

    def canvasConfig(self, event):
        """
        Configures the canvas when the size of the scrollable frame changes.

        Parameters:
            event (tk.Event): The event that triggers this configuration.
        """
        self.canvas.configure(scrollregion=self.canvas.bbox("all"),
                              width=325, height=200)

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
            allowed = [".com", ".xyz", ".mol2"]

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
        print("#### REPRESENTATIONAL MODEL UPDATED ####")