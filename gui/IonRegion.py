import tkinter as tk

from gui.CreateTooltip import CreateTooltip
from gui.SelectedIon import SelectedIon

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
        self.int_unitCell = tk.IntVar()

    def clear_variables(self):
        """Reset all variables and remove existing ions from the section."""
        self.removeAllIons()
        self.disable_ionic_buttons()
        self.var_ionNames.set("")
        self.int_hasIons.set(0)
        self.int_unitCell.set(0)

    def create_widgets(self, parent):
        """Create all widgets and frames for the ion information section.
        
        Args:
            parent (tk.Widget): The parent widget that will contain this section.
        """
        self.frame = tk.LabelFrame(master=parent,
                                   padx=5,
                                   text="Ion information",
                                   fg="blue",
                                   bg="#e0e0e0",
                                   relief=tk.GROOVE,
                                   borderwidth=2)

        self.canvas = tk.Canvas(self.frame, bg="#e0e0e0")
        self.frm_inside = tk.Frame(self.canvas, bg="#e0e0e0")
        self.scrl_frame = tk.Scrollbar(master=self.frame,
                                       orient="vertical",
                                       command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrl_frame.set)
        self.canvas.create_window((0, 0),
                                  window=self.frm_inside,
                                  anchor='nw')
        self.frm_inside.bind("<Configure>", self.canvasConfig)

        self.chk_hasIons = tk.Checkbutton(master=self.frm_inside, text="check for ionic radii",
                                          fg='black', bg="#e0e0e0",
                                          variable=self.int_hasIons, command=self.activator)
        CreateTooltip(self.chk_hasIons, "Check if some elements radii are ionic radii instead of covalent radii")

        self.chk_unitCell = tk.Checkbutton(master=self.frm_inside, text="unit cell boundaries",
                                           fg='black', bg="#e0e0e0",
                                           variable=self.int_unitCell, state=tk.DISABLED)
        CreateTooltip(self.chk_unitCell, "Check to replace dashed bonds with solid lines")

        self.btn_addIon = tk.Button(text="add", master=self.frm_inside,
                                    command=self.addIon, state=tk.DISABLED)
        CreateTooltip(self.btn_addIon, "Click here to add another ion to specify")
        self.btn_removeIon = tk.Button(master=self.frm_inside, text="remove",
                                       command=self.removeIon, state=tk.DISABLED)
        CreateTooltip(self.btn_removeIon, "Click here to remove the last added ion")

    def setup_layout(self):
        """Arrange the widgets and frames in the grid layout."""
        self.scrl_frame.pack(side="right", fill="y")
        self.canvas.pack(side="left")
        self.chk_hasIons.grid(row=0, column=0)
        self.chk_unitCell.grid(row=0, column=1)
        self.btn_addIon.grid(row=1, column=0)
        self.btn_removeIon.grid(row=1, column=1)

    def addIon(self):
        """Add a new ion entry to the ion list."""
        ion = SelectedIon(self.frm_inside, self.ionCount + 2, 0)
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

    def activator(self):
        """Enable or disable ionic input options based on the checkbox state."""
        if self.btn_addIon['state'] == tk.DISABLED:
            self.btn_addIon['state'] = tk.NORMAL
            self.btn_removeIon['state'] = tk.NORMAL
            self.chk_unitCell['state'] = tk.NORMAL
            print("##### ACTIVATING IONS INFORMATION INPUT ####")
        else:
            self.btn_addIon['state'] = tk.DISABLED
            self.btn_removeIon['state'] = tk.DISABLED
            self.chk_unitCell['state'] = tk.DISABLED
            self.removeAllIons()
            print("#### DEACTIVATING ION INFORMATION INPUT ####")
         
    def disable_ionic_buttons(self):
        """Disable all ionic input buttons and remove existing ion entries."""
        self.btn_addIon['state'] = tk.DISABLED
        self.btn_removeIon['state'] = tk.DISABLED
        self.chk_unitCell['state'] = tk.DISABLED
        self.removeAllIons()

    def canvasConfig(self, event):
        """Configure the canvas scroll region based on the frame size.
        
        Args:
            event (tk.Event): The event triggered by frame resizing.
        """
        self.canvas.configure(scrollregion=self.canvas.bbox("all"),
                              width=325, height=125)