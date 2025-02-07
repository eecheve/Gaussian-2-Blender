from pickle import FALSE
import sys
import os
import re

import tkinter as tk

from gui.CreateTooltip import CreateTooltip
from gui.Utility import Utility

ELEMENTS = { #dictionary containing the atomic symbol of all 118 elements in the periodic table
    "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar",
    "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr",
    "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe",
    "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu",
    "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn",
    "Fr", "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr",
    "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og"
}

class InputRegion(object):
    """Section of the app that receives the input for the file(s) to convert"""
    def __init__(self, parent, initial_dir):
        self.initialize_variables(initial_dir)
        self.setup_frame(parent)
        self.setup_canvas()
        self.add_widgets()
        self.position_widgets()

    def initialize_variables(self, initial_dir):
        """Initialize instance variables."""
        self.var_inputPaths = tk.StringVar()
        self.var_inputNames = tk.StringVar()
        self.var_modelTypes = tk.StringVar()
        self.var_inputPath = tk.StringVar()
        self.var_hlAtomList = tk.StringVar()
        self.var_hlBondList = tk.StringVar()
        self.var_isAnimation = tk.BooleanVar(value=False)
        self.var_highlightAtoms = tk.BooleanVar(value=False)
        self.var_highlightBonds = tk.BooleanVar(value=False)
        self.lst_inputNames = []
        self.lst_InputPaths = []
        self.initial_dir = initial_dir
        self.var_inputTypes = tk.StringVar()
        self.var_inputTypes.set(".com")

    def clear_variables(self):
        """Clear input-related variables."""
        self.var_inputPaths.set("")
        self.var_inputNames.set("")
        self.var_modelTypes.set("")
        self.var_inputPath.set("")
        self.var_hlAtomList.set("")
        self.var_isAnimation.set(False)
        self.var_highlightAtoms.set(False)
        self.var_highlightBonds.set(False)
        self.lst_inputNames.clear()
        self.lst_InputPaths.clear()
        self.var_inputTypes.set(".com")

    def setup_frame(self, parent):
        """Set up the main frame."""
        self.frame = tk.LabelFrame(master=parent, padx=5, text="Input", fg="blue", relief=tk.GROOVE, borderwidth=2)

    def setup_canvas(self):
        """Set up the canvas and scrollable frame."""
        self.canvas = tk.Canvas(self.frame)
        self.frm_inside = tk.Frame(self.canvas)
        self.scrl_frame = tk.Scrollbar(master=self.frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrl_frame.set)
        self.scrl_frame.pack(side="right", fill="y")
        self.canvas.pack(side="left")
        self.canvas.create_window((0, 0), window=self.frm_inside, anchor='nw')
        self.frm_inside.bind("<Configure>", self.canvasConfig)

    def add_widgets(self):
        """Add and configure widgets."""
        self.btn_setInputPath = tk.Button(text="set", master=self.frm_inside)
        self.lbl_inputLabel = tk.Label(text="Input name(s)", master=self.frm_inside)
        CreateTooltip(self.lbl_inputLabel, "Name(s) of the file(s) to be converted")
        
        self.lbl_fileType = tk.Label(text="Input type", master=self.frm_inside)
        CreateTooltip(self.lbl_fileType, "List of file extensions currently accepted by the program")
        self.lst_inputTypes = [".com", ".xyz"] #planning on reading .mol files in the future as well.
        self.drp_inputTypes = tk.OptionMenu(self.frm_inside, 
                                        self.var_inputTypes, 
                                        *self.lst_inputTypes,
                                        command=self.dropdown_callout)
        CreateTooltip(self.drp_inputTypes, "Choose one of the input types from this list")

        self.lbl_inputNames = tk.Label(textvariable=self.var_inputNames, master=self.frm_inside, fg="gray")
        CreateTooltip(self.lbl_inputNames, "List of input files with the correct extension")
        
        self.btn_setInputName = tk.Button(text="set", master=self.frm_inside, command=self.setInputName)
        CreateTooltip(self.btn_setInputName, "Select one or more input files")
        
        self.lbl_inputType = tk.Label(text="Model type", master=self.frm_inside)
        CreateTooltip(self.lbl_inputType, "Different representational models supported by Gaussian2Blender")
        
        self.lst_modelTypes = ["Ball-and-Stick", "Stick-only", "Van-der-Waals"]
        self.var_modelTypes.set("Ball-and-Stick")
        self.drp_modelTypes = tk.OptionMenu(self.frm_inside, self.var_modelTypes, 
                                            *self.lst_modelTypes, command=self.dropdown_callout)
        CreateTooltip(self.drp_modelTypes, "Choose one of the model representation options from this list")

        self.chk_highlightAtoms = tk.Checkbutton(master=self.frm_inside, text="highlight atoms",
                                                 variable=self.var_highlightAtoms, command=self.toggleAtomHighlighter)
        CreateTooltip(self.chk_highlightAtoms, "Check if you want to highlight one or more atoms in your 3D structure")

        self.lbl_highlightedAtoms = tk.Label(text="Atom list", master=self.frm_inside, state=tk.DISABLED)
        CreateTooltip(self.lbl_highlightedAtoms, "List of atoms to highlight in the resulting 3D model")
        
        self.ent_hlAtomList = tk.Entry(width=30, master=self.frm_inside, 
                                       textvariable=self.var_hlAtomList, state=tk.DISABLED)
        self.ent_hlAtomList.bind("<FocusOut>", self.on_validate_atom_list)
        self.ent_hlAtomList.bind("<Return>", self.on_validate_atom_list)
        self.ent_hlAtomList.bind("<Button-1>", lambda event: 
                                 self.on_enable_editing(event, self.ent_hlAtomList, self.var_highlightAtoms))
        CreateTooltip(self.ent_hlAtomList, "Separate each atom by a comma. E.g. C01, H02, H03, etc")

        self.chk_highlightBonds = tk.Checkbutton(master=self.frm_inside, text="highlight atoms",
                                                 variable=self.var_highlightBonds, command=self.toggleBondHighlighter)
        CreateTooltip(self.chk_highlightBonds, "Check if you want to highlight one or more bonds in your 3D structure")

        self.lbl_highlightedBonds = tk.Label(text="Bonds list", master=self.frm_inside, state=tk.DISABLED)
        CreateTooltip(self.lbl_highlightedBonds, "List of bonds to highlight: '-' singe, '=' double, '#' triple, '%' aromatic")
        
        self.ent_hlBondList = tk.Entry(width=30, master=self.frm_inside, 
                                       textvariable=self.var_hlBondList, state=tk.DISABLED)
        self.ent_hlBondList.bind("<FocusOut>", self.on_validate_bond_list)
        self.ent_hlBondList.bind("<Return>", self.on_validate_bond_list)
        self.ent_hlBondList.bind("<Button-1>", lambda event: 
                                 self.on_enable_editing(event, self.ent_hlBondList, self.var_highlightBonds))
        CreateTooltip(self.ent_hlBondList, "Separate each bond by a semicolon. E.g. C01-C02; C03=C04; C01#C09; O08%C06 etc")
        
        self.chk_isAnimation = tk.Checkbutton(master=self.frm_inside, text="is animation",
                                           variable=self.var_isAnimation, command=self.updateAnimationState)
        CreateTooltip(self.chk_isAnimation, "Check if the input files will serve as animation frames.")

    def reset_widget_bg_colors(self):
        """recerts all the interactable widgets to their original colors"""
        interactables = [self.btn_setInputPath, self.btn_setInputName,
                         self.drp_inputTypes, self.drp_modelTypes, self.chk_isAnimation]
        for interactable in interactables:
            Utility.revert_widget(interactable)

    def position_widgets(self):
        """Position widgets in the frame."""
        self.lbl_fileType.grid(row=1, column=0)
        self.drp_inputTypes.grid(row=1, column=1)
        self.lbl_inputLabel.grid(row=2, column=0)
        self.lbl_inputNames.grid(row=2, column=1, sticky="w")
        self.btn_setInputName.grid(row=2, column=2)
        self.lbl_inputType.grid(row=3, column=0, sticky="e")
        self.drp_modelTypes.grid(row=3, column=1, sticky="w")
        self.chk_highlightAtoms.grid(row=4, column=0)
        self.lbl_highlightedAtoms.grid(row=5, column=0)
        self.ent_hlAtomList.grid(row=5, column=1)
        self.chk_highlightBonds.grid(row=6, column=0)
        self.lbl_highlightedBonds.grid(row=7, column=0)
        self.ent_hlBondList.grid(row=7, column=1)
        self.chk_isAnimation.grid(row=8, column=0)

    def toggleAtomHighlighter(self):
        if self.var_highlightAtoms.get() == True:
            print("Please select the atoms to highlight separated by commas")
            self.lbl_highlightedAtoms['state'] = tk.NORMAL
            self.ent_hlAtomList['state'] = tk.NORMAL
        else:
            print("List of atoms removed")
            self.lbl_highlightedAtoms['state'] = tk.DISABLED
            self.ent_hlAtomList['state'] = tk.DISABLED
            self.var_hlAtomList.set("")

    def toggleBondHighlighter(self):
        if self.var_highlightBonds.get() == True:
            print("Please select the atoms to highlight separated by commas")
            self.lbl_highlightedBonds['state'] = tk.NORMAL
            self.ent_hlBondList['state'] = tk.NORMAL
        else:
            print("List of atoms removed")
            self.lbl_highlightedBonds['state'] = tk.DISABLED
            self.ent_hlBondList['state'] = tk.DISABLED
            self.var_hlBondList.set("")
    
    def updateAnimationState(self):
        if not self.var_isAnimation.get():
            print("The files will not be treated as animation.")
            return #this is called when che checkbox was checked, and is unchecked now
        if len(self.lst_inputNames) < 2:
            print("Error: There must be more than one file to implement animations.")
            self.var_isAnimation.set(False)  # Uncheck the checkbox if conditions are not met
            return
        print("At least two files are present as input. Make sure they have the same number of elements in the same order for the animation to work properly.")

        
    def allFilesHaveSameValidExtension(self, file_paths):
        """
        Checks if all files in the list have the same valid extension.
    
        :param file_paths: List of file paths.
        :return: True if all files have the same valid extension, False otherwise.
        """
        valid_extensions = {".com", ".xyz"}
        #valid_extensions = {".com", ".xyz", ".mol"} #<-- for future Emmanuel to tackle
        extensions = {os.path.splitext(path)[1].lower() for path in file_paths}
    
        if len(extensions) == 1 and extensions.pop() in valid_extensions:
            return True
        return False
        
    def check_for_atom_syntax(self, entry: str) -> bool:
        """Checks if the entry follows the format: ElementSymbol + two-digit number."""
        # Use regex to find where letters end and digits begin
        match = re.match(r"([A-Z][a-z]?)(\d+)$", entry)  # Ensures first letter is uppercase, second is optional lowercase
        if not match:
            print(f"Invalid format: '{entry}'. Expected ElementSymbol (1-2 letters) + two-digit number.")
            return False
        element_symbol, number_part = match.groups()

        # Validate atomic symbol
        if element_symbol not in ELEMENTS:
            print(f"Invalid element symbol '{element_symbol}' in '{entry}'.")
            return False

        # Validate number part (must be exactly two digits)
        if not re.fullmatch(r"\d{2}", number_part):
            print(f"Invalid number format '{number_part}' in '{entry}'. Must be a two-digit number (01-99).")
            return False

        return True

    def validate_atom_list(self, entry: str) -> bool:
        """Validates a comma-separated list of atomic symbols with numbers."""
    
        # Step 1: Remove spaces and newlines
        entry = entry.replace(" ", "").replace("\n", "")

        # Step 2: Split into a list based on commas
        atom_entries = entry.split(",")

        # Step 3: Apply check_for_atom_syntax() to each entry
        invalid_entries = [atom for atom in atom_entries if not self.check_for_atom_syntax(atom)]

        # Step 4: Print errors if there are invalid entries
        if invalid_entries:
            print(f"Invalid entries found: {', '.join(invalid_entries)}")
            return False

        return True

    def on_validate_atom_list(self, event=None):
        """Validation function called when the entry loses focus or Enter is pressed."""
        self.event = event
        user_input = self.var_hlAtomList.get().strip()

        if self.validate_atom_list(user_input):  # Valid input: Keep it & confirm entry
            print(f"Valid input: {user_input}")  # Confirmation message
            self.ent_hlAtomList.config(state=tk.DISABLED)  # Disable further editing
            return True  # Allow normal event propagation

        else:  # Invalid input: Clear entry
            print("Invalid input! Clearing entry box.")
            self.var_hlAtomList.set("")  # Clears the text box
            self.ent_hlAtomList.config(state=tk.NORMAL)  # Allow further editing

            # If Enter was pressed, prevent unintended newline behavior
            if event and event.keysym == "Return":
                return "break"

        return None  # Default return

    def on_validate_bond_list(self, event=None):
        print("here should be the logic for bond list entry")
    
    def on_enable_editing(self, event, tk_textbox, tk_checkbox_variable):
        """Enable editing when any entry box is clicked."""
        self.event = event
        if tk_checkbox_variable.get() == True:
            tk_textbox.config(state=tk.NORMAL)  # Enable the specific textbox that was clicked
            tk_textbox.select_range(0, tk.END)  # Optionally select the entire text
    
    def setInputName(self):
        """
        Opens a file dialog and allows selecting one or more files.
        Filters files based on the selected input type from the dropdown menu.
        Updates the input names list and displays all the elements to convert in the GUI.
        """
        input_type = self.var_inputTypes.get()
        file_extension = f"*{input_type}"
        file_types = [(f"{input_type.upper()} files", file_extension), ("All files", "*.*")]

        str_paths = tk.filedialog.askopenfilenames(initialdir=self.initial_dir, filetypes=file_types)
    
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
        Checks if the file has an acceptable extension.
        Currently accepts '.com', '.xyz', and '.mol'.

        :param file_path: Path to the file.
        :return: True if the file has an accepted extension, False otherwise.
        """
        _, file_ext = os.path.splitext(file_path)
        if file_ext.lower() == ".com":
            return True
        elif file_ext.lower() == ".xyz":
            return True
        #elif file_ext.lower() == ".mol": <--- for the future
        #    return True
        return False
                
    def updateInputNameList(self, string_list):
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
        self.canvas.configure(scrollregion=self.canvas.bbox("all"),
                              width=325, height=200)

    def dropdown_callout(self, event):
        print("#### REPRESENTATIONAL MODEL UPDATED ####")

    #must be called when the reset button is pressed.
    def reset_highlighter_options(self):
        self.var_highlightAtoms.set(False)

        self.lbl_highlightedAtoms['state'] = tk.DISABLED
        self.ent_hlAtomList['state'] = tk.DISABLED
        self.var_hlAtomList.set("")

        self.lbl_highlightedBonds['state'] = tk.DISABLED
        self.ent_hlBondList['state'] = tk.DISABLED
        self.var_hlBondList.set("")