import tkinter as tk

class AboutRegion(object):
    """Region that specifies things about the app"""
    def __init__(self, parent):
        self.frame = tk.LabelFrame(master=parent,
                                      padx=5, 
                                      text="About", 
                                      fg="blue", 
                                      relief=tk.GROOVE, 
                                      borderwidth=2)

        #self.frame.grid(row=1, column=1, sticky="nw")
        
        self.lbl_ver = tk.Label(master=self.frame,
                                    text="version: ",
                                    fg="black")
        self.lbl_version = tk.Label(master=self.frame,
                                    text="2025.1.0 ",
                                    fg="gray")
        
        self.lbl_auth = tk.Label(master=self.frame,
                                 text="Echeverri-Jimenez CER3D Group",
                                 fg="gray")

        self.lbl_ver.grid(row=0, column=0)
        self.lbl_version.grid(row=0, column=1)
        self.lbl_auth.grid(row=1, column=0, columnspan=2)


