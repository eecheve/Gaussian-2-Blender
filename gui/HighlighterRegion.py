import os
import re

import tkinter as tk
from gui.CreateTooltip import CreateTooltip

ELEMENTS = { #dictionary containing the atomic symbol of all 118 elements in the periodic table
    "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar",
    "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr",
    "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe",
    "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu",
    "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn",
    "Fr", "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr",
    "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og"
}

class HighlighterRegion(object):
    def __init__(self, parent):
        """
        Initializes the highlighter region and its widgets.

        Parameters:
            parent (tk.Widget): The parent widget to attach the highlighter frame to.
        """
        self.initialize_variables()
        self.setup_frame(parent)
        self.add_widgets()
        self.position_widgets()

    def initialize_variables(self):
        """
        Initializes the variables for atom and bond highlighting.
        """
        self.var_hlAtomList = tk.StringVar()
        self.var_hlBondList = tk.StringVar()
        self.var_highlightAtoms = tk.BooleanVar(value=False)
        self.var_highlightBonds = tk.BooleanVar(value=False)

    def clear_variables(self):
        """
        Clears the atom and bond highlighting variables (reset to defaults).
        """
        self.var_hlAtomList.set("")
        self.var_hlBondList.set("")
        self.var_highlightAtoms.set(False)
        self.var_highlightBonds.set(False)

    def reset_highlighter_options(self):
        """
        Resets the highlighter options (e.g., disables widgets and clears input lists).
        """
        self.var_highlightAtoms.set(False)
        self.var_highlightBonds.set(False)
        self.lbl_highlightedAtoms['state'] = tk.DISABLED
        self.ent_hlAtomList['state'] = tk.DISABLED
        self.var_hlAtomList.set("")
        self.lbl_highlightedBonds['state'] = tk.DISABLED
        self.ent_hlBondList['state'] = tk.DISABLED
        self.var_hlBondList.set("")

    def setup_frame(self, parent):
        """
        Sets up the frame for the highlighter region.

        Parameters:
            parent (tk.Widget): The parent widget to attach the frame to.
        """
        self.frame = tk.LabelFrame(master=parent, padx=5, text="Highlight atoms and bonds", 
                                   fg="blue", relief=tk.GROOVE, borderwidth=2)

    def add_widgets(self):
        """
        Adds widgets (checkboxes, labels, and entry fields) for atom and bond highlighting.
        """
        self.chk_highlightAtoms = tk.Checkbutton(master=self.frame, text="highlight atoms",
                                                 variable=self.var_highlightAtoms, command=self.toggleAtomHighlighter)
        CreateTooltip(self.chk_highlightAtoms, "Check if you want to highlight one or more atoms in your 3D structure")

        self.lbl_highlightedAtoms = tk.Label(text="Atom list", master=self.frame, state=tk.DISABLED)
        CreateTooltip(self.lbl_highlightedAtoms, "List of atoms to highlight in the resulting 3D model")
        
        self.ent_hlAtomList = tk.Entry(width=30, master=self.frame, 
                                       textvariable=self.var_hlAtomList, state=tk.DISABLED)
        self.ent_hlAtomList.bind("<FocusOut>", self.on_validate_atom_list)
        self.ent_hlAtomList.bind("<Return>", self.on_validate_atom_list)
        self.ent_hlAtomList.bind("<Button-1>", lambda event: 
                                 self.on_enable_editing(event, self.ent_hlAtomList, self.var_highlightAtoms))
        CreateTooltip(self.ent_hlAtomList, "Separate each atom by a comma. E.g. C01, H02, H03, etc")

        self.chk_highlightBonds = tk.Checkbutton(master=self.frame, text="highlight atoms",
                                                 variable=self.var_highlightBonds, command=self.toggleBondHighlighter)
        CreateTooltip(self.chk_highlightBonds, "Check if you want to highlight one or more bonds in your 3D structure")

        self.lbl_highlightedBonds = tk.Label(text="Bonds list", master=self.frame, state=tk.DISABLED)
        CreateTooltip(self.lbl_highlightedBonds, "List of bonds to highlight: '-' singe, '=' double, '#' triple, '%' aromatic")
        
        self.ent_hlBondList = tk.Entry(width=30, master=self.frame, 
                                       textvariable=self.var_hlBondList, state=tk.DISABLED)
        self.ent_hlBondList.bind("<FocusOut>", self.on_validate_bond_list)
        self.ent_hlBondList.bind("<Return>", self.on_validate_bond_list)
        self.ent_hlBondList.bind("<Button-1>", lambda event: 
                                 self.on_enable_editing(event, self.ent_hlBondList, self.var_highlightBonds))
        CreateTooltip(self.ent_hlBondList, "Separate each bond by a semicolon. E.g. C01-C02; C03=C04; C01#C09; O08%C06 etc")

    def position_widgets(self):
        """
        Positions the widgets inside the frame using grid layout.
        """
        self.chk_highlightAtoms.grid(row=0, column=0)
        self.lbl_highlightedAtoms.grid(row=1, column=0)
        self.ent_hlAtomList.grid(row=1, column=1)
        self.chk_highlightBonds.grid(row=2, column=0)
        self.lbl_highlightedBonds.grid(row=3, column=0)
        self.ent_hlBondList.grid(row=3, column=1)

    def toggleAtomHighlighter(self):
        """
        Toggles the state of atom highlighting. Enables or disables the atom list entry.
        If the checkbox is checked, the atom list entry is enabled. If unchecked, it is disabled and cleared.
        """
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
        """
        Toggles the state of bond highlighting. Enables or disables the bond list entry.
        If the checkbox is checked, the bond list entry is enabled. If unchecked, it is disabled and cleared.
        """
        if self.var_highlightBonds.get() == True:
            print("Please select the atoms to highlight separated by commas")
            self.lbl_highlightedBonds['state'] = tk.NORMAL
            self.ent_hlBondList['state'] = tk.NORMAL
        else:
            print("List of atoms removed")
            self.lbl_highlightedBonds['state'] = tk.DISABLED
            self.ent_hlBondList['state'] = tk.DISABLED
            self.var_hlBondList.set("")

    def check_for_atom_syntax(self, entry: str) -> bool:
        """
        Checks if the atom entry follows the correct syntax: ElementSymbol + two-digit number.

        Parameters:
            entry (str): The atom entry to validate (e.g., "C01", "H02").

        Returns:
            bool: True if the entry is valid, False otherwise.
        """
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
        """
        Validates a comma-separated list of atom entries.

        Parameters:
            entry (str): A comma-separated string of atom entries to validate (e.g., "C01, H02").

        Returns:
            bool: True if all entries are valid, False if any entry is invalid.
        """
    
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
        """
        Handles validation when the atom entry loses focus or the Enter key is pressed.

        Parameters:
            event (tk.Event, optional): The event that triggered the validation. Default is None.

        Returns:
            str | None: Returns "break" if Enter was pressed and input is invalid, otherwise None.
        """
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

    def validate_bond_list(self, entry: str) -> bool:
        """
        Validates a semicolon-separated list of bond entries.

        Parameters:
            entry (str): A semicolon-separated string of bond entries to validate (e.g., "C01-C02; C03=C04").

        Returns:
            bool: True if all bond entries are valid, False if any entry is invalid.
        """
    
        # Remove spaces and newlines
        entry = entry.replace(" ", "").replace("\n", "")
    
        # Split into a list based on semicolons
        bond_entries = entry.split(";")
    
        # Apply check_for_bond_syntax() to each entry
        invalid_entries = [bond for bond in bond_entries if not self.check_for_bond_syntax(bond)]
    
        # Print errors if there are invalid entries
        if invalid_entries:
            print(f"Invalid entries found: {', '.join(invalid_entries)}")
            return False
    
        return True
    
    def on_validate_bond_list(self, event=None):
        """
        Handles validation when the bond entry loses focus or the Enter key is pressed.

        Parameters:
            event (tk.Event, optional): The event that triggered the validation. Default is None.

        Returns:
            str | None: Returns "break" if Enter was pressed and input is invalid, otherwise None.
        """
        self.event = event
        user_input = self.var_hlBondList.get().strip()

        if self.validate_bond_list(user_input):  # Valid input: Keep it & confirm entry
            print(f"Valid input: {user_input}")  # Confirmation message
            self.ent_hlBondList.config(state=tk.DISABLED)  # Disable further editing
            return True  # Allow normal event propagation

        else:  # Invalid input: Clear entry
            print("Invalid input! Clearing entry box.")
            self.var_hlBondList.set("")  # Clears the text box
            self.ent_hlBondList.config(state=tk.NORMAL)  # Allow further editing

            # If Enter was pressed, prevent unintended newline behavior
            if event and event.keysym == "Return":
                return "break"

        return None  # Default return
    
    def check_for_bond_syntax(self, entry: str) -> bool:
        """
        Checks if the bond entry follows the correct syntax (e.g., "C01-C02", "C03=C04").

        Parameters:
            entry (str): The bond entry to validate.

        Returns:
            bool: True if the bond entry follows the correct syntax, False otherwise.
        """
        # Define the bond separators
        separators = ["-", "=", "#", "%"]
    
        # Check if the entry contains exactly one separator
        if sum(entry.count(sep) for sep in separators) != 1:
            print(f"Invalid format: '{entry}'. Must contain exactly one of the following separators: {', '.join(separators)}.")
            return False
    
        # Split the entry into two parts based on the separator
        for sep in separators:
            if sep in entry:
                left_part, right_part = entry.split(sep)
                break
    
        # Validate the left and right parts using check_for_atom_syntax()
        if not self.check_for_atom_syntax(left_part):
            print(f"Invalid left part '{left_part}' in '{entry}'.")
            return False
    
        if not self.check_for_atom_syntax(right_part):
            print(f"Invalid right part '{right_part}' in '{entry}'.")
            return False
    
        return True
        
    def on_enable_editing(self, event, tk_textbox, tk_checkbox_variable):
        """
        Enables editing for the clicked entry box if the associated checkbox is checked.

        Parameters:
            event (tk.Event): The event that triggered this function.
            tk_textbox (tk.Entry): The text entry widget to enable or disable.
            tk_checkbox_variable (tk.BooleanVar): The associated checkbox's variable that determines the state.
        """
        self.event = event
        if tk_checkbox_variable.get() == True:
            tk_textbox.config(state=tk.NORMAL)  # Enable the specific textbox that was clicked
            tk_textbox.select_range(0, tk.END)  # Optionally select the entire text