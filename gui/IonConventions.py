import tkinter as tk

from gui.CreateTooltip import CreateTooltip
#tooltip = CreateTooltip.CreateTooltip

class IonConventions(object):
    """region of the window that specifies meaning of some coordination values"""
    def __init__(self, parent):
        self.frm_codes = tk.LabelFrame(master=parent,
                                      padx=5, 
                                      text="Ion conventions", 
                                      fg="blue", 
                                      relief=tk.GROOVE, 
                                      borderwidth=2)
        self.frm_codes.grid(row=2, column=1, padx=2, pady=2, sticky="W")

        self.lbl_hs = tk.Label(master=self.frm_codes,
                                     text="hs: ",
                                     fg="black")
        self.ttp_hs = CreateTooltip(self.lbl_hs,
                              "code")
        
        self.lbl_highSpin = tk.Label(master=self.frm_codes,
                                     text="high spin",
                                     fg="gray")
        self.ttp_highSpin = CreateTooltip(self.lbl_highSpin,
                                    "meaning")

        self.lbl_ls = tk.Label(master=self.frm_codes,
                                     text="ls: ",
                                     fg="black")
        self.ttp_ls = CreateTooltip(self.lbl_ls,
                              "code")
        
        self.lbl_lowSpin = tk.Label(master=self.frm_codes,
                                     text="low spin",
                                     fg="gray")
        self.ttp_lowSpin = CreateTooltip(self.lbl_lowSpin,
                                    "meaning")

        self.lbl_py = tk.Label(master=self.frm_codes,
                                     text="PY:",
                                     fg="black")
        self.ttp_py = CreateTooltip(self.lbl_py,
                                    "code")

        self.lbl_pyramidal = tk.Label(master=self.frm_codes,
                                     text="pyramidal",
                                     fg="gray")
        self.ttp_pyramidal = CreateTooltip(self.lbl_pyramidal,
                                    "meaning")

        self.lbl_sq = tk.Label(master=self.frm_codes,
                                     text="SQ:",
                                     fg="black")
        self.ttp_sq = CreateTooltip(self.lbl_sq,
                                    "code")

        self.lbl_square = tk.Label(master=self.frm_codes,
                                     text="square-planar",
                                     fg="gray")
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


        




