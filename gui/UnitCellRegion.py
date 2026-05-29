import tkinter as tk

from gui.CreateTooltip import CreateTooltip
from gui.SelectedIon import SelectedIon

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

    def clear_variables(self):
        self.int_unitCell.set(0)
        self.int_uc_x.set(1)
        self.int_uc_y.set(1)
        self.int_uc_z.set(1)
        self.int_plane_h.set(0)
        self.int_plane_k.set(0)
        self.int_plane_l.set(0)

    def unit_cell_activator(self):
        pass
    
    def get_unit_cell_repeats(self):
        if self.spn_uc_x['state'] == tk.DISABLED:
            return None
        else:
            return self.int_uc_x.get(), self.int_uc_y.get(), self.int_uc_z.get()
        
    def get_miller_indices(self):
        return self.int_plane_h.get(), self.int_plane_k.get(), self.int_plane_l.get()