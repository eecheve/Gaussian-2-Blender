import os
import tkinter as tk

from gui.CreateTooltip import CreateTooltip

class OutputRegion(object):
    """Section of the app that selects the output path for the converted file(s)"""
    def __init__(self, parent, initial_dir):
        self.def_outputPath = os.path.join(initial_dir, "output", "")
        self.initial_dir = initial_dir
        
        self.frame = tk.LabelFrame(master=parent, 
                                        padx=5, 
                                        text="Output", 
                                        fg="blue", 
                                        bg="#e0e0e0",
                                        relief=tk.GROOVE, 
                                        width=325, 
                                        height=102, 
                                        borderwidth=2)

        self.lbl_outputPath = tk.Label(text="Output path",
                                      master=self.frame,
                                      bg="#e0e0e0", fg='black')

        self.ttp_outputLabel = CreateTooltip(self.lbl_outputPath,
                                      "Folder path where the output will be saved")

        self.var_outputPath = tk.StringVar()
        self.var_outputPath.set(self.def_outputPath)
        self.ent_outputPath = tk.Entry(width=35, bg="#e0e0e0", fg='black',
                                       master=self.frame, 
                                       textvariable=self.var_outputPath)

        self.ttp_outputPath = CreateTooltip(self.ent_outputPath,
                                      "Paste here the folder path where you want your output to be\
                                      or click on the 'set' button to do the same")

        self.btn_setOutputPath = tk.Button(text="set", 
                                           master=self.frame, 
                                           command=self.setOutputPath)

        self.ttp_setOutputPath = CreateTooltip(self.btn_setOutputPath,
                                         "Select the folder path where you want your output to be")

        self.lbl_outputType = tk.Label(text="Output type", 
                                       master=self.frame,
                                       bg="#e0e0e0", fg='black')

        self.ttp_outputTypeLabel = CreateTooltip(self.lbl_outputType,
                                           "Different rendering formats supported by Gaussian2Blender")

        self.lst_outputTypes = [".fbx", ".obj", ".dae", ".glb", ".stl"]
        self.var_outputTypes = tk.StringVar()
        self.var_outputTypes.set(".glb")
        self.drp_outputTypes = tk.OptionMenu(self.frame, 
                                        self.var_outputTypes, 
                                        *self.lst_outputTypes,
                                        command=self.dropdown_callout)

        self.ttp_outputTypes = CreateTooltip(self.drp_outputTypes,
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

    def restrict_output_types_for_animation(self, is_animation):
        """
        Updates the list of selectable output file types based on whether animation is enabled.

        Parameters:
            is_animation (bool): Indicates whether the animation mode is active.

        Behavior:
            - Clears the current dropdown menu options.
            - Populates the menu with the appropriate list of file types.
            - Resets the selected output type if the current selection is no longer valid.
        """
        if is_animation:
            allowed = [".fbx", ".glb"]
        else:
            allowed = [".fbx", ".obj", ".dae", ".glb", ".stl"]

        menu = self.drp_outputTypes["menu"]
        menu.delete(0, "end")
        for opt in allowed:
            menu.add_command(label=opt, command=lambda value=opt: self.var_outputTypes.set(value))

        if self.var_outputTypes.get() not in allowed:
            self.var_outputTypes.set(allowed[0])


