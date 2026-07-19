import tkinter as tk
from tkinter import ttk

from gui.CreateTooltip import CreateTooltip
from gui.LabeledComboRow import LabeledComboRow
from gui.RepeatableRowGroup import RepeatableRowGroup

ELEMENTS_LIST = sorted([
    "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne", "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar",
    "K", "Ca", "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr",
    "Rb", "Sr", "Y", "Zr", "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn", "Sb", "Te", "I", "Xe",
    "Cs", "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb", "Lu",
    "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", "Po", "At", "Rn",
    "Fr", "Ra", "Ac", "Th", "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm", "Md", "No", "Lr",
    "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og"
])

SECTION_HEADER_FONT = ("Helvetica", 9, "bold")

# Small vertical gap between rows in the growth/Miller lists, just enough to
# keep them from looking cramped. Tweak here if you want more/less breathing
# room - it's used by both lists below.
ROW_SPACING = 4


class UnitCellRegion(object):
    """Section of the app that customizes information about crystals and their unit cells"""
    def __init__(self, parent):
        self.initialize_variables()
        self.create_widgets(parent)
        self.setup_layout()

    def initialize_variables(self):
        self.int_unitCell = tk.IntVar()
        self.int_allowGrowth = tk.IntVar()
        self.int_allowMiller = tk.IntVar()
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

        # ---------------- Group 1: Unit Cell Boundaries ----------------
        self.lbl_boundaries_header = tk.Label(master=self.frame, text="Unit Cell Boundaries",
                                              bg="#e0e0e0", fg='black', font=SECTION_HEADER_FONT)

        self.chk_unitCell = tk.Checkbutton(master=self.frame, text="unit cell boundaries",
                                           fg='black', bg="#e0e0e0",
                                           variable=self.int_unitCell, command=self.unit_cell_activator)
        CreateTooltip(self.chk_unitCell, "Check to replace dashed bonds with solid lines")

        self.sep_boundaries_growth = ttk.Separator(master=self.frame, orient="horizontal")

        # ---------------- Groups 2 & 3: Unit Cell Growth | Miller Indices ----------------
        # These two are fully independent of each other (see UnitCellRegion's history -
        # Miller planes used to be nested under each growth row, no longer). Since neither
        # one relates to the other, they sit side by side as two parallel columns instead
        # of stacked, with a vertical separator between them - each block get its own
        # small sub-frame so it can be gridded as a single unit into its column.
        self.frm_growth_block = tk.Frame(master=self.frame, bg="#e0e0e0")
        self.frm_miller_block = tk.Frame(master=self.frame, bg="#e0e0e0")
        self.sep_growth_miller = ttk.Separator(master=self.frame, orient="vertical")

        # Unit Cell Growth: a plain, independent list of x/y/z growth sizes.
        # Buttons start disabled until the checkbox is on.
        self.lbl_growth_header = tk.Label(master=self.frm_growth_block, text="Unit Cell Growth",
                                          bg="#e0e0e0", fg='black', font=SECTION_HEADER_FONT)

        self.chk_allowGrowth = tk.Checkbutton(master=self.frm_growth_block, text="allow unit cell growth",
                                              fg='black', bg="#e0e0e0",
                                              variable=self.int_allowGrowth, command=self.growth_activator)
        CreateTooltip(self.chk_allowGrowth,
                      "Check to specify one or more unit cell growth sizes")

        self.growth_group = RepeatableRowGroup(
            parent=self.frm_growth_block,
            row_factory=lambda rows_container: LabeledComboRow(
                parent=rows_container,
                input_label_list=["x:", "y:", "z:"],
                option_ranges=[(1, 5), (1, 5), (1, 5)]
            ),
            group_label="Choose unit cell growth",
            group_tooltip="specify the number of repeating units per local axis",
            add_button_text="add cell growth",
            add_tooltip="Add a new unit cell growth size",
            remove_last_tooltip="Remove the most recently added unit cell growth",
            remove_all_tooltip="Remove every unit cell growth",
            start_enabled=False,
            row_spacing=ROW_SPACING
        )

        # Miller Indices: independent from unit cell growth - just its own list
        # of h/k/l planes.
        self.lbl_miller_header = tk.Label(master=self.frm_miller_block, text="Miller Indices",
                                          bg="#e0e0e0", fg='black', font=SECTION_HEADER_FONT)

        self.chk_allowMiller = tk.Checkbutton(master=self.frm_miller_block, text="allow Miller indices",
                                              fg='black', bg="#e0e0e0",
                                              variable=self.int_allowMiller, command=self.miller_activator)
        CreateTooltip(self.chk_allowMiller,
                      "Check to specify one or more Miller index planes to render")

        self.miller_group = RepeatableRowGroup(
            parent=self.frm_miller_block,
            row_factory=lambda rows_container: LabeledComboRow(
                parent=rows_container,
                input_label_list=["h:", "k:", "l:"],
                option_ranges=[(-9, 9), (-9, 9), (-9, 9)]
            ),
            group_label="Choose Miller planes",
            group_tooltip="specify the Miller numbers to render a plane",
            add_button_text="add plane",
            add_tooltip="Add a Miller plane (h, k, l)",
            remove_last_tooltip="Remove the most recently added Miller plane",
            remove_all_tooltip="Remove every Miller plane",
            start_enabled=False,
            row_spacing=ROW_SPACING
        )

        self.sep_miller_polyhedra = ttk.Separator(master=self.frame, orient="horizontal")

        # ---------------- Group 4: Coordination Polyhedra ----------------
        self.lbl_polyhedra_header = tk.Label(master=self.frame, text="Coordination Polyhedra",
                                             bg="#e0e0e0", fg='black', font=SECTION_HEADER_FONT)

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

        # ---------------- Shared clear button ----------------
        self.btn_clear = tk.Button(master=self.frame, text="Clear", command=self.clear_variables)

    def setup_layout(self):
        self.frame.grid(row=0, column=0, sticky="w")

        row = 0

        # Group 1: Unit Cell Boundaries
        self.lbl_boundaries_header.grid(row=row, column=0, sticky="w", pady=(4, 0))
        row += 1
        self.chk_unitCell.grid(row=row, column=0, sticky="w", pady=(0, 6))
        row += 1

        self.sep_boundaries_growth.grid(row=row, column=0, columnspan=3, sticky="ew", pady=6)
        row += 1

        # Groups 2 & 3: Unit Cell Growth | Miller Indices, side by side in the
        # same row - growth in column 0, a vertical separator in column 1,
        # Miller indices in column 2. Each block lays out its own header/
        # checkbox/row-list internally, same as every other group here.
        self.lbl_growth_header.grid(row=0, column=0, sticky="w", pady=(4, 0))
        self.chk_allowGrowth.grid(row=1, column=0, sticky="w")
        self.growth_group.frame.grid(row=2, column=0, sticky="w", pady=(2, 6))

        self.lbl_miller_header.grid(row=0, column=0, sticky="w", pady=(4, 0))
        self.chk_allowMiller.grid(row=1, column=0, sticky="w")
        self.miller_group.frame.grid(row=2, column=0, sticky="w", pady=(2, 6))

        self.frm_growth_block.grid(row=row, column=0, sticky="nw")
        self.sep_growth_miller.grid(row=row, column=1, sticky="ns", padx=15)
        self.frm_miller_block.grid(row=row, column=2, sticky="nw")
        row += 1

        self.sep_miller_polyhedra.grid(row=row, column=0, columnspan=3, sticky="ew", pady=6)
        row += 1

        # Group 4: Coordination Polyhedra
        self.lbl_polyhedra_header.grid(row=row, column=0, sticky="w", pady=(4, 0))
        row += 1
        self.chk_polyhedra.grid(row=row, column=0, sticky="w")
        row += 1
        self.frm_polyhedra_controls.grid(row=row, column=0, sticky="w", padx=5, pady=(4, 0))
        row += 1

        self.btn_add_center.grid(row=0, column=0, padx=(0, 4))
        self.btn_remove_center.grid(row=0, column=1)

        self.frm_polyhedra_rows.grid(row=row, column=0, sticky="w", padx=5)
        row += 1

        # Shared clear button
        self.btn_clear.grid(row=row, column=0, sticky="w", pady=(10, 4))

    def clear_variables(self):
        self.int_unitCell.set(0)
        self.int_allowGrowth.set(0)
        self.growth_group.remove_all()
        self.growth_group.set_enabled(False)
        self.int_allowMiller.set(0)
        self.miller_group.remove_all()
        self.miller_group.set_enabled(False)
        self._remove_all_center_rows()

    def unit_cell_activator(self):
        pass

    def growth_activator(self):
        """Enable or disable the unit cell growth controls based on the checkbox state."""
        if self.int_allowGrowth.get():
            self.growth_group.set_enabled(True)
        else:
            self.growth_group.set_enabled(False)
            self.growth_group.remove_all()

    def miller_activator(self):
        """Enable or disable the Miller indices controls based on the checkbox state."""
        if self.int_allowMiller.get():
            self.miller_group.set_enabled(True)
        else:
            self.miller_group.set_enabled(False)
            self.miller_group.remove_all()

    def get_unit_cell_repeats(self):
        """
        Returns a list of [x, y, z] unit cell growth sizes the user has added,
        e.g. [[2, 2, 2], [3, 3, 3]]. An empty list means no growth was requested.

        NOTE: this used to return a single [x, y, z] value. TheorChem2Blender.py's
        callers still expect the old single-value shape and have not been updated
        yet - that update, plus the matching changes in scripts/, is tracked as a
        follow-up task.
        """
        return self.growth_group.get_row_values()

    def get_miller_indices(self):
        """
        Returns a list of [h, k, l] Miller planes the user has added, e.g.
        [[1, 0, 0], [1, 1, 1]]. An empty list means no Miller planes were requested.
        Independent from get_unit_cell_repeats() - the two are no longer linked.

        NOTE: this used to return a single {"h":.., "k":.., "l":..} value.
        TheorChem2Blender.py's callers still expect the old single-value shape
        and have not been updated yet - tracked as a follow-up task, same as
        get_unit_cell_repeats() above.
        """
        return self.miller_group.get_row_values()

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
        self.frame.update_idletasks()

    def _remove_all_center_rows(self):
        """Remove all center atom rows."""
        for row in self.polyhedra_center_rows:
            row["frame"].destroy()
        self.polyhedra_center_rows.clear()
        self.frame.update_idletasks()

    def get_polyhedra_centers(self):
        """
        Returns the list of selected center element types if polyhedra
        building is enabled and at least one center is specified.

        :return: (list) Element symbols, e.g. ['V', 'Fe'], or empty list.
        """
        if not self.int_polyhedra.get():
            return []
        return [row["var"].get() for row in self.polyhedra_center_rows if row["var"].get()]
