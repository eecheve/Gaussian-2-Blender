import sys
import os

import tkinter as tk
import tkinter.ttk as ttk

from gui.TextRedirector import TextRedirector
#redirector = TextRedirector.TextRedirector

class PrintRegion(object):
    """GUI region that allows user to observe the print statements and the errors"""
    def __init__(self, parent):
        self.frm_print = tk.LabelFrame(master=parent,
                                      padx=5, 
                                      text="Console", 
                                      fg="blue", 
                                      relief=tk.GROOVE, 
                                      borderwidth=2)
        self.frm_print.grid(row=4, column=0, columnspan=3, pady=2, padx=2)

        self.text = tk.Text(master=self.frm_print, 
                            height=8,
                            width=80,
                            wrap="word")
        self.text.tag_configure("stderr", foreground="#b22222")
        self.text.config(state="disabled")

        self.scrl_text = ttk.Scrollbar(self.frm_print,
                                       command=self.text.yview)
      
        self.text.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
        self.scrl_text.grid(row=0, column=1, sticky="nsew")
        self.text['yscrollcommand'] = self.scrl_text.set

        sys.stdout = TextRedirector(self.text, "stdout")
        sys.stderr = TextRedirector(self.text, "stderr")

    def clear_content(self):
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.configure(state="disabled")


