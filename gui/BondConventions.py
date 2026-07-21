import tkinter as tk

from gui.CreateTooltip import CreateTooltip
from gui import Styles

# Shown on hover anywhere in this region - the frame itself and every label
# below all get this same tooltip, so there's no dead spot where hovering
# does nothing.
BOND_CODE_TOOLTIP = "Use these characters to specify the desired bond orders when forcing or highlighting bonds"

# (bond name, character code) pairs, in the order they're listed.
BOND_CONVENTIONS = [
    ("dashed bond", "_ "),
    ("single bond", "- "),
    ("double bond", "= "),
    ("delocalized bond", "% "),
    ("triple bond", "# "),
]


class BondConventions(object):
    """region of the window that specifies meaning of some coordination values"""
    def __init__(self, parent):
        self.frame = tk.LabelFrame(master=parent,
                                      padx=5,
                                      text="Bond text conventions",
                                      fg=Styles.TITLE_FG,
                                      bg=Styles.PANEL_BG,
                                      relief=Styles.FRAME_RELIEF,
                                      borderwidth=Styles.FRAME_BORDERWIDTH)
        CreateTooltip(self.frame, BOND_CODE_TOOLTIP)

        for row, (name, code) in enumerate(BOND_CONVENTIONS):
            lbl_code = tk.Label(master=self.frame, text=code, fg=Styles.TEXT_FG, bg=Styles.PANEL_BG)
            lbl_name = tk.Label(master=self.frame, text=name, fg=Styles.MUTED_FG, bg=Styles.PANEL_BG)
            lbl_code.grid(row=row, column=0)
            lbl_name.grid(row=row, column=1)
            CreateTooltip(lbl_code, BOND_CODE_TOOLTIP)
            CreateTooltip(lbl_name, BOND_CODE_TOOLTIP)