import tkinter as tk
from tkinter import ttk

from gui.CreateTooltip import CreateTooltip

ELEMENTS_LIST = sorted([
    "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar",
    "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr",
    "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe",
    "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu",
    "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn",
    "Fr", "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr",
    "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og"
])

class UnitCellRegion(object):
    """Section of the app that customizes information about crystals and their unit cells"""
    def __init__(self, parent):
        self.initialize_variables()
        self.create_widgets(parent)
        self.setup_layout()

    def initialize_variables(self):
        self.int_unitCell = tk.IntVar()
        
        self.int_uc_x = tk.IntVar(value=1)
        self.int_uc_y = tk.IntVar(value=1)
        self.int_uc_z = tk.IntVar(value=1)

        self.int_plane_h = tk.IntVar(value=0)
        self.int_plane_k = tk.IntVar(value=0)
        self.int_plane_l = tk.IntVar(value=0)

        self.int_polyhedra = tk.IntVar()
        self.polyhedra_center_rows = []

    def create_widgets(self, parent):
        self.frame = tk.LabelFrame(master=parent,
                                   padx=5,
                                   text="Unit cell details",
                                   fg="blue",
                                   bg="#e0e0e0",
                                   relief=tk.GROOVE,
                                   borderwidth=2)
        
        self.chk_unitCell = tk.Checkbutton(master=self.frame, text="unit cell boundaries",
                                           fg='black', bg="#e0e0e0",
                                           variable=self.int_unitCell, command=self.unit_cell_activator)
        CreateTooltip(self.chk_unitCell, "Check to replace dashed bonds with solid lines")

        self.lbl_unit_cell_growth = tk.Label(master=self.frame, 
                                             text="Choose unit cell growth", bg="#e0e0e0", fg='black')
        CreateTooltip(self.lbl_unit_cell_growth, "specify the number of repeating units per local axis")  
        
        self.frm_uc_growth = tk.Frame(
            master=self.frame,
            bg="#e0e0e0"
        )
        
        self.lbl_uc_x = tk.Label(self.frm_uc_growth, text="x:", bg="#e0e0e0")
        self.lbl_uc_y = tk.Label(self.frm_uc_growth, text="y:", bg="#e0e0e0")
        self.lbl_uc_z = tk.Label(self.frm_uc_growth, text="z:", bg="#e0e0e0")

        self.spn_uc_x = tk.Spinbox(self.frm_uc_growth, from_=1, to=5, width=5, 
                                   textvariable=self.int_uc_x, state=tk.NORMAL)
        self.spn_uc_y = tk.Spinbox(self.frm_uc_growth, from_=1, to=5, width=5, 
                                   textvariable=self.int_uc_y, state=tk.NORMAL)
        self.spn_uc_z = tk.Spinbox(self.frm_uc_growth, from_=1, to=5, width=5, 
                                   textvariable=self.int_uc_z, state=tk.NORMAL)
        
        self.frm_uc_planes = tk.Frame(
            master=self.frame,
            bg="#e0e0e0"
        )
        self.lbl_uc_planes = tk.Label(master=self.frm_uc_planes, 
                                             text="Miller indices", bg="#e0e0e0", fg='black')
        CreateTooltip(self.lbl_uc_planes, "specify the the Miller numbers to render a plane")
        self.lbl_uc_h = tk.Label(self.frm_uc_planes, text="h:", bg="#e0e0e0")
        self.lbl_uc_k = tk.Label(self.frm_uc_planes, text="k:", bg="#e0e0e0")
        self.lbl_uc_l = tk.Label(self.frm_uc_planes, text="l:", bg="#e0e0e0")
        self.spn_uc_h = tk.Spinbox(self.frm_uc_planes, from_=0, to=9, width=5, 
                                   textvariable=self.int_plane_h, state=tk.NORMAL)
        self.spn_uc_k = tk.Spinbox(self.frm_uc_planes, from_=0, to=9, width=5, 
                                   textvariable=self.int_plane_k, state=tk.NORMAL)
        self.spn_uc_l = tk.Spinbox(self.frm_uc_planes, from_=0, to=9, width=5, 
                                   textvariable=self.int_plane_l, state=tk.NORMAL)
        
        self.btn_clear = tk.Button(master=self.frame, text="Clear", command=self.clear_variables)

        self.chk_polyhedra = tk.Checkbutton(master=self.frame, text="build polyhedra",
                                            fg='black', bg="#e0e0e0",
                                            variable=self.int_polyhedra,
                                            command=self.polyhedra_activator)
        CreateTooltip(self.chk_polyhedra, "Build coordination polyhedra around selected center atoms")

        self.frm_polyhedra_controls = tk.Frame(master=self.frame, bg="#e0e0e0")

        self.btn_add_center = tk.Button(master=self.frm_polyhedra_controls, text="add center",
                                        command=self.add_center_atom, state=tk.DISABLED)
        CreateTooltip(self.btn_add_center, "Add a center atom type for polyhedra construction")

        self.btn_remove_center = tk.Button(master=self.frm_polyhedra_controls, text="remove",
                                           command=self.remove_center_atom, state=tk.DISABLED)
        CreateTooltip(self.btn_remove_center, "Remove the last added center atom type")

        self.frm_polyhedra_rows = tk.Frame(master=self.frame, bg="#e0e0e0")

        self.btn_clear = tk.Button(master=self.frame, text="Clear", command=self.clear_variables)

    def setup_layout(self):
        #<---------------- Changes about the unit cell
        self.frame.grid(row=0, column=0, sticky="w")

        self.chk_unitCell.grid(row=0, column=0, sticky="w")
        self.lbl_unit_cell_growth.grid(row=1, column=0, sticky="w")

        self.frm_uc_growth.grid(row=2, column=0, sticky="w", padx=5)

        self.lbl_uc_x.grid(row=0, column=0, padx=(0, 2))
        self.spn_uc_x.grid(row=0, column=1, padx=(0, 10))

        self.lbl_uc_y.grid(row=0, column=2, padx=(0, 2))
        self.spn_uc_y.grid(row=0, column=3, padx=(0, 10))

        self.lbl_uc_z.grid(row=0, column=4, padx=(0, 2))
        self.spn_uc_z.grid(row=0, column=5)
        
        #------------------ Changes about Miller indices
        self.frm_uc_planes.grid(row=3, column=0, sticky="w", padx=5)
        
        self.lbl_uc_planes.grid(row=0, column=0, columnspan=6, sticky="w")
        self.lbl_uc_h.grid(row=1, column=0, padx=(0, 2))
        self.spn_uc_h.grid(row=1, column=1, padx=(0, 10))
        self.lbl_uc_k.grid(row=1, column=2, padx=(0, 2))
        self.spn_uc_k.grid(row=1, column=3, padx=(0, 10))
        self.lbl_uc_l.grid(row=1, column=4, padx=(0, 2))
        self.spn_uc_l.grid(row=1, column=5)

        self.btn_clear.grid(row=5, column=0, sticky="w", pady=(5, 0))

        #----------------- Polyhedra
        self.chk_polyhedra.grid(row=4, column=0, sticky="w", pady=(8, 0))

        self.frm_polyhedra_controls.grid(row=5, column=0, sticky="w", padx=5)
        self.btn_add_center.grid(row=0, column=0, padx=(0, 4))
        self.btn_remove_center.grid(row=0, column=1)

        self.frm_polyhedra_rows.grid(row=6, column=0, sticky="w", padx=5)

        self.btn_clear.grid(row=7, column=0, sticky="w", pady=(8, 0))

    def clear_variables(self):
        self.int_unitCell.set(0)
        self.int_uc_x.set(1)
        self.int_uc_y.set(1)
        self.int_uc_z.set(1)
        self.int_plane_h.set(0)
        self.int_plane_k.set(0)
        self.int_plane_l.set(0)
        self._remove_all_center_rows()

    def unit_cell_activator(self):
        pass
    
    def get_unit_cell_repeats(self):
        if self.spn_uc_x['state'] == tk.DISABLED:
            return None
        else:
            return self.int_uc_x.get(), self.int_uc_y.get(), self.int_uc_z.get()
        
    def get_miller_indices(self):
        return self.int_plane_h.get(), self.int_plane_k.get(), self.int_plane_l.get()
    
    def polyhedra_activator(self):
        """Enable or disable polyhedra controls based on the checkbox state."""
        if self.int_polyhedra.get():
            self.btn_add_center.config(state=tk.NORMAL)
            self.btn_remove_center.config(state=tk.NORMAL)
        else:
            self.btn_add_center.config(state=tk.DISABLED)
            self.btn_remove_center.config(state=tk.DISABLED)
            self._remove_all_center_rows()

    def add_center_atom(self):
        """Add a new row with an element combobox for a center atom type."""
        var = tk.StringVar(value="V")
        row_frame = tk.Frame(master=self.frm_polyhedra_rows, bg="#e0e0e0")
        lbl = tk.Label(row_frame, text="Center:", bg="#e0e0e0", fg='black')
        cb = ttk.Combobox(row_frame, textvariable=var, values=ELEMENTS_LIST, width=6, state="readonly")
        CreateTooltip(cb, "Select the element type that acts as the polyhedron center")
        lbl.grid(row=0, column=0, padx=(0, 4))
        cb.grid(row=0, column=1)
        row_frame.grid(row=len(self.polyhedra_center_rows), column=0, sticky="w", pady=2)
        self.polyhedra_center_rows.append({"frame": row_frame, "var": var})

    def remove_center_atom(self):
        """Remove the last added center atom row."""
        if not self.polyhedra_center_rows:
            return
        row = self.polyhedra_center_rows.pop()
        row["frame"].destroy()

    def _remove_all_center_rows(self):
        """Remove all center atom rows."""
        for row in self.polyhedra_center_rows:
            row["frame"].destroy()
        self.polyhedra_center_rows.clear()

    def get_polyhedra_centers(self):
        """
        Returns the list of selected center element types if polyhedra
        building is enabled and at least one center is specified.

        :return: (list) Element symbols, e.g. ['V', 'Fe'], or empty list.
        """
        if not self.int_polyhedra.get():
            return []
        return [row["var"].get() for row in self.polyhedra_center_rows if row["var"].get()]