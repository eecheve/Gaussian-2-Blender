"""
Shared style constants for the GUI.

Every region module (InputRegion, OutputRegion, UnitCellRegion, etc.) builds
its widgets with the same handful of colors and fonts - the panel gray, the
blue section titles, the black/gray text tiers, and so on. Centralizing them
here means a widget's `bg=`/`fg=`/`font=` kwargs read as
`bg=Styles.PANEL_BG` instead of a repeated literal, and a future palette
change only touches this file.

Import the whole module (``from gui import Styles``) and reference constants
as ``Styles.PANEL_BG`` rather than importing individual names, so call sites
stay self-documenting about where the value comes from.
"""

# ---------------- Panel / frame styling ----------------
# The background used by virtually every widget in the app, and the
# relief/borderwidth pairing every top-level LabelFrame uses to get its
# boxed-section look.
PANEL_BG = "#e0e0e0"
FRAME_RELIEF = "groove"
FRAME_BORDERWIDTH = 2

# ---------------- Text color tiers ----------------
# TITLE_FG is used for LabelFrame `text=` titles (the bold-ish blue label
# tkinter draws on the frame's border). TEXT_FG is the default body/label
# text color. MUTED_FG is for secondary or dimmed text, such as resolved
# paths, version/author info, and legend labels.
TITLE_FG = "blue"
TEXT_FG = "black"
MUTED_FG = "gray"

# ---------------- Fonts ----------------
# Bold section headers used to divide a LabelFrame into logical groups
# (first introduced in UnitCellRegion, now shared wherever a frame needs
# the same treatment).
SECTION_HEADER_FONT = ("Helvetica", 9, "bold")

# ---------------- One-off semantic colors ----------------
# Colors tied to a specific meaning rather than the general panel/text
# palette above. Kept here too so they're not scattered as bare literals.
CONVERT_BUTTON_BG = "#b7ffc8"   # ActionsRegion's "Convert!" button (pale green)
STDERR_FG = "#b22222"           # ConsoleRegion's stderr text tag (firebrick)
TOOLTIP_BG = "#ffffff"          # CreateTooltip's popup background

# ---------------- Default widget backgrounds ----------------
# Utility.py restores these after temporarily recoloring widgets (e.g. to
# flash a validation error) - kept as the stock tk background per widget
# class rather than a single shared constant
DEFAULT_WIDGET_BG = {
    "Checkbutton": "#f0f0f0",
    "Menubutton": "#f0f0f0",
    "Button": "#f0f0f0",
}
