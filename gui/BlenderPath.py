import os
import tkinter as tk

import CreateTooltip
tooltip = CreateTooltip.CreateTooltip

import Utility
utility = Utility.Utility

class BlenderPath(object):
    """Section of the window used to search and set the path
    in which blender is installed"""
    def __init__(self, parent):
        self.var_blenderPath = tk.StringVar()
        
        self.frm_blender = tk.LabelFrame(master=parent,
                                           text="Blender executable location", 
                                           fg="blue", 
                                           relief=tk.GROOVE, 
                                           width=800, 
                                           height=170, 
                                           borderwidth=2)
        self.frm_blender.grid(row=0, column=0, columnspan=2, pady=2, padx=2, sticky="w")
        #self.frm_blender.grid_propagate(0)

        self.lbl_blenderLabel = tk.Label(
            text="Blender path",
            master=self.frm_blender)

        self.ttp_blenderLabel = tooltip(
            self.lbl_blenderLabel,
            "Folder path where Blender is installed in your machine")
    
        self.var_blenderPath.set("")
        self.lbl_blenderPath = tk.Label(
            textvariable = self.var_blenderPath,
            master=self.frm_blender,
            fg="gray")
    
        self.btn_setBlenderPath = tk.Button(
            text="search",
            master=self.frm_blender,
            command=self.lookForBlenderPath)
        self.ttp_setBlenderPath = tooltip(
            self.btn_setBlenderPath,
            "Click here to select blender.exe path if default is not found")
    
        self.lbl_blenderLabel.grid(row=0, column=0)
        self.lbl_blenderPath.grid(row=0, column=1, sticky="w")
        self.btn_setBlenderPath.grid(row=0, column=2, sticky="w")

    def searchBlenderPath(self):
        blender = "blender.exe"
        for root, dirs, files in os.walk("C:\\Program Files\\Blender Foundation"):
            for name in files:
                if name in files:
                    if name == blender:
                        #return os.path.abspath(os.path.join(root, name))
                        print("Blender executable found in", self.lbl_blenderPath, "the search for the blender path is not necessary")
                        return os.path.abspath(root)
                else:
                    print("blender.exe not found within Program_Files\Blender_Foundation")
                    print("please instal Blender before using Gaussian-2-Blender or set manually the path in which Blender is installed")
                    return "blender.exe not found"
                    #sys.stderr.write("blender.exe not found within Program_Files\\Blender_Foundation\n")
                    
    def lookForBlenderPath(self):
        str_path = tk.filedialog.askdirectory()
        if utility.findFile("blender.exe", str_path):
            self.var_blenderPath.set(str_path)
        else:
            #print(f"{bcolors.WARNING}Error: blender.exe not found in specified path. Please select the path in which is installed{bcolors.ENDC}")
            print("Error: blender.exe not found in specified path. Please select the path in which is installed")
            self.var_blenderPath.set("blender.exe not found")

    def setBlenderPath(self, str_path):
        self.var_blenderPath.set(str_path)

