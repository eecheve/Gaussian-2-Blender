import tkinter as tk

from gui.CreateTooltip import CreateTooltip

class IonConventions(object):
    """region of the window that specifies meaning of some coordination values"""
    def __init__(self, parent):
        self.frame = tk.LabelFrame(master=parent,
                                      padx=5, 
                                      text="Ion conventions", 
                                      fg="blue",
                                      bg="#e0e0e0",
                                      relief=tk.GROOVE, 
                                      borderwidth=2)

        self.lbl_hs = tk.Label(master=self.frame,
                                     text="hs: ",
                                     fg="black",
                                     bg="#e0e0e0")
        self.ttp_hs = CreateTooltip(self.lbl_hs,
                              "code")
        
        self.lbl_highSpin = tk.Label(master=self.frame,
                                     text="high spin",
                                     fg="gray",
                                     bg="#e0e0e0")
        self.ttp_highSpin = CreateTooltip(self.lbl_highSpin,
                                    "meaning")

        self.lbl_ls = tk.Label(master=self.frame,
                                     text="ls: ",
                                     fg="black",
                                     bg="#e0e0e0")
        self.ttp_ls = CreateTooltip(self.lbl_ls,
                              "code")
        
        self.lbl_lowSpin = tk.Label(master=self.frame,
                                     text="low spin",
                                     fg="gray",
                                     bg="#e0e0e0")
        self.ttp_lowSpin = CreateTooltip(self.lbl_lowSpin,
                                    "meaning")

        self.lbl_py = tk.Label(master=self.frame,
                                     text="PY:",
                                     fg="black",
                                     bg="#e0e0e0")
        self.ttp_py = CreateTooltip(self.lbl_py,
                                    "code")

        self.lbl_pyramidal = tk.Label(master=self.frame,
                                     text="pyramidal",
                                     fg="gray",
                                     bg="#e0e0e0")
        self.ttp_pyramidal = CreateTooltip(self.lbl_pyramidal,
                                    "meaning")

        self.lbl_sq = tk.Label(master=self.frame,
                                     text="SQ:",
                                     fg="black",
                                     bg="#e0e0e0")
        self.ttp_sq = CreateTooltip(self.lbl_sq,
                                    "code")

        self.lbl_square = tk.Label(master=self.frame,
                                     text="square-planar",
                                     fg="gray",
                                     bg="#e0e0e0")
        self.ttp_square = CreateTooltip(self.lbl_square,
                                    "meaning")

        self.lbl_hs.grid(row=0, column=0)
        self.lbl_highSpin.grid(row=0, column=1)
        self.lbl_ls.grid(row=1, column=0)
        self.lbl_lowSpin.grid(row=1, column=1)
        self.lbl_sq.grid(row=2, column=0)
        self.lbl_square.grid(row=2, column=1)
        self.lbl_py.grid(row=3, column=0)
        self.lbl_pyramidal.grid(row=3, column=1)
        




