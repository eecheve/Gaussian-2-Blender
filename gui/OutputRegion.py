import tkinter as tk

import CreateTooltip
tooltip = CreateTooltip.CreateTooltip

class OutputRegion(object):
    """Section of the app that selects the output path for the converted file(s)"""
    def __init__(self, parent, initial_dir):
        self.def_outputPath = initial_dir + "\\output\\"
        self.initial_dir = initial_dir
        
        self.frm_output = tk.LabelFrame(master=parent, 
                                        padx=5, 
                                        text="Output", 
                                        fg="blue", 
                                        relief=tk.GROOVE, 
                                        width=325, 
                                        height=102, 
                                        borderwidth=2)
        self.frm_output.grid(row=1, column=1, sticky="SW")

        self.lbl_outputPath = tk.Label(text="Output path",
                                      master=self.frm_output)

        self.ttp_outputLabel = tooltip(self.lbl_outputPath,
                                      "Folder path where the output will be saved")

        self.var_outputPath = tk.StringVar()
        self.var_outputPath.set(self.def_outputPath)
        self.ent_outputPath = tk.Entry(width=35, 
                                       master=self.frm_output, 
                                       textvariable=self.var_outputPath)

        self.ttp_outputPath = tooltip(self.ent_outputPath,
                                      "Paste here the folder path where you want your output to be\
                                      or click on the 'set' button to do the same")

        self.btn_setOutputPath = tk.Button(text="set", 
                                           master=self.frm_output, 
                                           command=self.setOutputPath)

        self.ttp_setOutputPath = tooltip(self.btn_setOutputPath,
                                         "Select the folder path where you want your output to be")

        self.lbl_outputType = tk.Label(text="Output type", 
                                       master=self.frm_output)

        self.ttp_outputTypeLabel = tooltip(self.lbl_outputType,
                                           "Different rendering formats supported by Gaussian2Blender")

        self.lst_outputTypes = [".fbx", ".obj", ".dae", ".x3d", ".stl"]
        self.var_outputTypes = tk.StringVar()
        self.var_outputTypes.set(".fbx")
        self.drp_outputTypes = tk.OptionMenu(self.frm_output, 
                                        self.var_outputTypes, 
                                        *self.lst_outputTypes,
                                        command=self.dropdown_callout)

        self.ttp_outputTypes = tooltip(self.drp_outputTypes,
                                       "Choose one of the output types from this list")

        self.lbl_outputPath.grid(row=0, column=0)
        self.ent_outputPath.grid(row=0, column=1)
        self.btn_setOutputPath.grid(row=0, column=2)

        self.lbl_outputType.grid(row=2, column=0, sticky="e")
        self.drp_outputTypes.grid(row=2, column=1, sticky="w")

    def setOutputPath(self):
        str_path = tk.filedialog.askdirectory(initialdir = self.initial_dir)
        self.var_outputPath.set(str_path)
        print("#### OUTPUT PATH CHANGED ####")

    def dropdown_callout(self, event):
        print("#### OUTPUT TYPE UPDATED ####")


