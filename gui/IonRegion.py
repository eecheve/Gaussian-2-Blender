import tkinter as tk

from gui.CreateTooltip import CreateTooltip
from gui.SelectedIon import SelectedIon
from gui import Styles

class IonRegion(object):
    """Section of the app that receives information about possible ions present"""
    def __init__(self, parent):
        self.initialize_variables()
        self.create_widgets(parent)
        self.setup_layout()

    def initialize_variables(self):
        """Initialize all variables used in the ion information section."""
        self.ionCount = 0
        self.lst_ions = []
        self.var_ionNames = tk.StringVar()
        self.int_hasIons = tk.IntVar()

    def clear_radii_variables(self):
        """Reset all variables and remove existing ions from the section."""
        self.removeAllIons()
        self.disable_ionic_buttons()
        self.var_ionNames.set("")
        self.int_hasIons.set(0)

    def create_widgets(self, parent):
        """Create all widgets and frames for the ion information section.

        These all live directly in self.frame - no inner canvas/scrollbar.
        The tab's own content container (see TheorChem2Blender.py) already
        provides scrolling if this ever grows taller than the space
        available, so a second, nested scrollable area here was redundant.

        Args:
            parent (tk.Widget): The parent widget that will contain this section.
        """
        self.frame = tk.LabelFrame(master=parent,
                                   padx=5,
                                   text="Ionic radii details",
                                   fg=Styles.TITLE_FG,
                                   bg=Styles.PANEL_BG,
                                   relief=Styles.FRAME_RELIEF,
                                   borderwidth=Styles.FRAME_BORDERWIDTH)

        self.chk_hasIons = tk.Checkbutton(master=self.frame, text="check for ionic radii",
                                          fg=Styles.TEXT_FG, bg=Styles.PANEL_BG,
                                          variable=self.int_hasIons, command=self.ionic_radii_activator)
        CreateTooltip(self.chk_hasIons, "Check if some elements radii are ionic radii instead of covalent radii")

        self.btn_addIon = tk.Button(text="add", master=self.frame,
                                    command=self.addIon, state=tk.DISABLED)
        CreateTooltip(self.btn_addIon, "Click here to add another ion to specify")
        self.btn_removeIon = tk.Button(master=self.frame, text="remove",
                                       command=self.removeIon, state=tk.DISABLED)
        CreateTooltip(self.btn_removeIon, "Click here to remove the last added ion")

    def setup_layout(self):
        """Arrange the widgets in the grid layout, matching the spacing
        rhythm used in UnitCellRegion.py."""
        self.chk_hasIons.grid(row=0, column=0, columnspan=2, sticky="w", pady=(2, 6))
        self.btn_addIon.grid(row=1, column=0, padx=(0, 4), pady=2)
        self.btn_removeIon.grid(row=1, column=1, pady=2)

    def addIon(self):
        """Add a new ion entry to the ion list."""
        ion = SelectedIon(self.frame, self.ionCount + 2, 0)
        self.lst_ions.append(ion)
        self.ionCount += 1

    def removeIon(self):
        """Remove the last added ion from the list, if available."""
        if self.lst_ions:  # Check if the ion list is not empty
            last_ion = self.lst_ions.pop()
            last_ion.delete()  # Assuming 'delete' is a method for the ion object
            if self.ionCount > 0:
                self.ionCount -= 1
            else:
                print("No more ions to remove.")

    def removeAllIons(self):
        """Remove all ion entries from the list."""
        for ion in self.lst_ions:
            ion.delete()
        self.lst_ions.clear()
        self.ionCount = 0

    def ionic_radii_activator(self):
        """Enable or disable ionic input options based on the checkbox state."""
        if self.btn_addIon['state'] == tk.DISABLED:
            self.btn_addIon['state'] = tk.NORMAL
            self.btn_removeIon['state'] = tk.NORMAL
            print("##### ACTIVATING IONS INFORMATION INPUT ####")
        else:
            self.btn_addIon['state'] = tk.DISABLED
            self.btn_removeIon['state'] = tk.DISABLED
            self.removeAllIons()
            print("#### DEACTIVATING ION INFORMATION INPUT ####")

    def unit_cell_activator(self):
        pass

    def disable_ionic_buttons(self):
        """Disable all ionic input buttons and remove existing ion entries."""
        self.btn_addIon['state'] = tk.DISABLED
        self.btn_removeIon['state'] = tk.DISABLED
        self.removeAllIons()