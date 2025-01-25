import tkinter as tk

class WalkthroughRegion(object):
    def __init__(self, parent):
        self.frame = tk.LabelFrame(master=parent,
                                padx=5, 
                                text="Guided walkthrough", 
                                fg="blue", 
                                relief=tk.GROOVE, 
                                borderwidth=2,
                                width=390,  
                                height=180) 
        self.frame.grid_propagate(False)

        self.default_text = "Click on 'Guide: single convert' or 'Guide: animation convert' for a guided tutorial on how to use this tool"
        self.guide_widget = tk.Label(master=self.frame,
                                     text=self.default_text,
                                     fg="black",
                                     wraplength=370)
        self.guide_widget.grid(row=0, column=0)

    def revert_text_to_default(self):
        self.guide_widget.config(text=self.default_text)

    def modify_guide_text(self, new_text):
        self.guide_widget.config(text=new_text)