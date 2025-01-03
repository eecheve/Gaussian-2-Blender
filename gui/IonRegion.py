import tkinter as tk

from gui.CreateTooltip import CreateTooltip
from gui.SelectedIon import SelectedIon

class IonRegion(object):
    """Section of the app that receives information about possible ions present"""
    def __init__(self, parent):
        self.ionCount = 0
        self.lst_ions = []
        
        self.var_ionNames = tk.StringVar()
        self.int_hasIons = tk.IntVar()
        self.int_unitCell = tk.IntVar()

        self.frm_ions = tk.LabelFrame(master=parent,
                                      padx=5, 
                                      text="Ion information", 
                                      fg="blue", 
                                      relief=tk.GROOVE, 
                                      borderwidth=2)
        self.frm_ions.grid(row=2, column=0, padx=2, pady=2, sticky="W", rowspan=2)

        self.canvas = tk.Canvas(self.frm_ions)
        self.frm_inside = tk.Frame(self.canvas)
        self.scrl_frame = tk.Scrollbar(master=self.frm_ions,
                                       orient="vertical",
                                       command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrl_frame.set)
        self.scrl_frame.pack(side="right",fill="y")
        self.canvas.pack(side="left")
        self.canvas.create_window((0,0), 
                                  window=self.frm_inside,
                                  anchor='nw')
        self.frm_inside.bind("<Configure>", self.canvasConfig)

        self.chk_hasIons = tk.Checkbutton(master=self.frm_inside,
                                          text="check for ionic radii",
                                          variable=self.int_hasIons,
                                          command=self.activator)
        self.ttp_hasIons = CreateTooltip(self.chk_hasIons,
                                   "Check if some elements radii are ionic radii instead of covalent radii")
        
        self.btn_addIon = tk.Button(text="add",
                                    master=self.frm_inside,
                                    command=self.addIon,
                                    state=tk.DISABLED)
        self.ttp_addIon = CreateTooltip(self.btn_addIon,
                                  "Click here to add another ion to specify")

        self.btn_removeIon = tk.Button(master=self.frm_inside,
                                       text="remove",
                                       command=self.removeIon,
                                       state=tk.DISABLED)
        self.ttp_removeIon = CreateTooltip(self.btn_removeIon,
                                     "Click here to remove the last added ion")

        self.chk_unitCell = tk.Checkbutton(master=self.frm_inside,
                                          text="unit cell boundaries",
                                          variable=self.int_unitCell,
                                          state=tk.DISABLED)
        self.ttp_hasIons = CreateTooltip(self.chk_unitCell,
                                   "Check to replace dashed bonds with solid lines")

        self.chk_hasIons.grid(row=0, column=0)
        self.chk_unitCell.grid(row=0, column=1)
        self.btn_addIon.grid(row=1, column=0)
        self.btn_removeIon.grid(row=1, column=1)

    def addIon(self):
        ion = SelectedIon(self.frm_inside, self.ionCount + 2, 0)
        self.lst_ions.append(ion)
        self.ionCount += 1

    def removeIon(self):
        last_element = self.lst_ions.pop()
        last_element.delete()
        if self.ionCount > 0:
            self.ionCount -= 1

    def removeAllIons(self):
        for ion in self.lst_ions:
            ion.delete()
        self.lst_ions.clear()
        self.ionCount = 0

    def activator(self):
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

    def canvasConfig(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"),
                              width=325, height=125)