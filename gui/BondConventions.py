import tkinter as tk

from gui.CreateTooltip import CreateTooltip
#tooltip = CreateTooltip.CreateTooltip

class BondConventions(object):
    """region of the window that specifies meaning of some coordination values"""
    def __init__(self, parent):
        self.frame = tk.LabelFrame(master=parent,
                                      padx=5, 
                                      text="Bond text conventions", 
                                      fg="blue", 
                                      relief=tk.GROOVE, 
                                      borderwidth=2)

        self.lbl_singleBond = tk.Label(master=self.frame, text="single bond", fg="gray")
        self.lbl_sb_code = tk.Label(master=self.frame, text="- ", fg="black")

        self.lbl_doubleBond = tk.Label(master=self.frame, text="double bond", fg="gray")  
        self.lbl_db_code = tk.Label(master=self.frame, text="= ", fg="black")


        self.lbl_tripleBond = tk.Label(master=self.frame, text="triple bond", fg="gray")
        self.lbl_tb_code = tk.Label(master=self.frame, text="# ", fg="black")

        self.lbl_aromaticBond = tk.Label(master=self.frame, text="delocalized bond", fg="gray")
        self.lbl_ab_code = tk.Label(master=self.frame, text="% ", fg="black")

        self.lbl_singleBond.grid(row=0, column=1)
        self.lbl_sb_code.grid(row=0, column=0)
        self.lbl_doubleBond.grid(row=1, column=1)
        self.lbl_db_code.grid(row=1, column=0)
        self.lbl_aromaticBond.grid(row=2, column=1)
        self.lbl_ab_code.grid(row=2, column=0)
        self.lbl_tripleBond.grid(row=3, column=1)
        self.lbl_tb_code.grid(row=3, column=0)


        




