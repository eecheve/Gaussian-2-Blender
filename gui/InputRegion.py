import sys
import os

import tkinter as tk

import CreateTooltip
tooltip = CreateTooltip.CreateTooltip

class InputRegion(object):
    """Section of the app that receives the input for the file(s) to convert"""
    def __init__(self, parent):
        self.var_inputPaths = tk.StringVar()
        self.var_inputNames = tk.StringVar()
        self.var_modelTypes = tk.StringVar()
        self.var_inputPath = tk.StringVar()
        self.lst_inputNames = []
        
        self.frm_input = tk.LabelFrame(master=parent,
                                      padx=5, 
                                      text="Input", 
                                      fg="blue", 
                                      relief=tk.GROOVE, 
                                      borderwidth=2)
        self.frm_input.grid(row=1, column=0, padx=2, pady=2, sticky="W")

        self.canvas = tk.Canvas(self.frm_input)
        self.frm_inside = tk.Frame(self.canvas)
        self.scrl_frame = tk.Scrollbar(master=self.frm_input,
                                       orient="vertical",
                                       command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrl_frame.set)
        self.scrl_frame.pack(side="right",fill="y")
        self.canvas.pack(side="left")
        self.canvas.create_window((0,0), 
                                  window=self.frm_inside,
                                  anchor='nw')
        self.frm_inside.bind("<Configure>", self.canvasConfig)

        self.btn_setInputPath = tk.Button(text="set",
                                         master=self.frm_inside)
        
        self.lbl_inputLabel = tk.Label(text="Input name(s)",
                                      master=self.frm_inside)

        self.ttp_inputLabel = tooltip(self.lbl_inputLabel,
                                     "Name(s) of the file(s) to be converted")
        
        self.lbl_inputNames = tk.Label(textvariable=self.var_inputNames,
                                      master=self.frm_inside,
                                      fg="gray")

        self.ttp_inputNames = tooltip(self.lbl_inputNames,
                                      "List of input files with the correct extension")
        
        self.btn_setInputName = tk.Button(text="set",
                                         master=self.frm_inside, 
                                         command=self.setInputName)

        self.ttp_setInputName = tooltip(self.btn_setInputName, 
                                        "Select one or more '.com' gaussian input files")
        
        self.lbl_inputType = tk.Label(text="Model type",
                                     master=self.frm_inside)

        self.ttp_inputType = tooltip(self.lbl_inputType, 
                                     "Different representational models supported by Gaussian2Blender")
        
        self.lst_modelTypes = ["Ball-and-Stick", "Stick-only", "Van-der-Waals"]
        self.var_modelTypes.set("Ball-and-Stick")
        self.drp_modelTypes = tk.OptionMenu(self.frm_inside, 
                                            self.var_modelTypes, 
                                            *self.lst_modelTypes,
                                            command=self.dropdouwn_callout)

        self.ttp_modelTypes = tooltip(self.drp_modelTypes, 
                                      "Choose one of the model representation options from this list")
        
        self.lbl_inputLabel.grid(row=1, column=0)
        self.lbl_inputNames.grid(row=1, column=1, sticky="w")
        self.btn_setInputName.grid(row=1, column=2)
        self.lbl_inputType.grid(row=2, column=0, sticky="e")
        self.drp_modelTypes.grid(row=2, column=1, sticky="w")

    def setInputName(self):
        """
        opens a file dialog and allows to select one or more elements
        updates the input names list and depicts all the elements to convert in the GUI
        """
        str_paths = tk.filedialog.askopenfilenames()
        self.updateInputNameList(str_paths)
        path = os.path.dirname(str_paths[0])
        print("##### SETTING INPUT FILES TO CONVERT ####")
        self.var_inputPath.set(path)
        for entry in str_paths:
            if ".com" in entry:
                f_name = os.path.basename(entry)
                print(f_name, "has correct file extension")
                self.lst_inputNames.append(f_name)
            else:
                print(f_name, "is not a '.com' file and is not accepted as input")

    def updateInputNameList(self, string_list):
        self.lst_inputNames.clear()
        self.var_inputNames.set("")
        s = ""
        for entry in string_list:
            n = os.path.basename(entry)
            e = n + "\n"
            s += e
            self.lst_inputNames.append(n)
        self.var_inputNames.set(s)

    def canvasConfig(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"),
                              width=325, height=200)

    def dropdouwn_callout(self, event):
        print("#### REPRESENTATIONAL MODEL UPDATED ####")
