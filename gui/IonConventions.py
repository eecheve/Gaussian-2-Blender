import tkinter as tk

from gui.CreateTooltip import CreateTooltip
from gui import Styles

# Shown on hover anywhere in this region - the frame itself and every label
# below all get this same tooltip, so there's no dead spot where hovering
# does nothing.
ION_CODE_TOOLTIP = "Use these codes to identify the ion's coordination geometry or spin state when selecting from the (charge, coordination) dropdown"

# (code, meaning) pairs, in the order they're listed.
ION_CONVENTIONS = [
    ("hs: ", "high spin"),
    ("ls: ", "low spin"),
    ("SQ: ", "square-planar"),
    ("PY: ", "pyramidal"),
]


class IonConventions(object):
    """region of the window that specifies meaning of some coordination values"""
    def __init__(self, parent):
        self.frame = tk.LabelFrame(master=parent,
                                      padx=5,
                                      text="Ion conventions",
                                      fg=Styles.TITLE_FG,
                                      bg=Styles.PANEL_BG,
                                      relief=Styles.FRAME_RELIEF,
                                      borderwidth=Styles.FRAME_BORDERWIDTH)
        CreateTooltip(self.frame, ION_CODE_TOOLTIP)

        for row, (code, meaning) in enumerate(ION_CONVENTIONS):
            lbl_code = tk.Label(master=self.frame, text=code, fg=Styles.TEXT_FG, bg=Styles.PANEL_BG)
            lbl_meaning = tk.Label(master=self.frame, text=meaning, fg=Styles.MUTED_FG, bg=Styles.PANEL_BG)
            lbl_code.grid(row=row, column=0)
            lbl_meaning.grid(row=row, column=1)
            CreateTooltip(lbl_code, ION_CODE_TOOLTIP)
            CreateTooltip(lbl_meaning, ION_CODE_TOOLTIP)

