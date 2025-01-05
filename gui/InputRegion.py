import sys
import os

import tkinter as tk

from gui.CreateTooltip import CreateTooltip
#tooltip = CreateTooltip.CreateTooltip

class InputRegion(object):
    """Section of the app that receives the input for the file(s) to convert"""
    def __init__(self, parent, initial_dir):
        self.initialize_variables(initial_dir)
        self.setup_frame(parent)
        self.setup_canvas()
        self.add_widgets()
        self.position_widgets()

    def initialize_variables(self, initial_dir):
        """Initialize instance variables."""
        self.var_inputPaths = tk.StringVar()
        self.var_inputNames = tk.StringVar()
        self.var_modelTypes = tk.StringVar()
        self.var_inputPath = tk.StringVar()
        self.var_isAnimation = tk.BooleanVar(value=False)
        self.lst_inputNames = []
        self.initial_dir = initial_dir

    def clear_variables(self):
        """Clear input-related variables."""
        self.var_inputPaths.set("")
        self.var_inputNames.set("")
        self.var_modelTypes.set("")
        self.var_inputPath.set("")
        self.var_isAnimation.set(False)
        self.lst_inputNames.clear()

    def setup_frame(self, parent):
        """Set up the main frame."""
        self.frame = tk.LabelFrame(master=parent, padx=5, text="Input", fg="blue", relief=tk.GROOVE, borderwidth=2)

    def setup_canvas(self):
        """Set up the canvas and scrollable frame."""
        self.canvas = tk.Canvas(self.frame)
        self.frm_inside = tk.Frame(self.canvas)
        self.scrl_frame = tk.Scrollbar(master=self.frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrl_frame.set)
        self.scrl_frame.pack(side="right", fill="y")
        self.canvas.pack(side="left")
        self.canvas.create_window((0, 0), window=self.frm_inside, anchor='nw')
        self.frm_inside.bind("<Configure>", self.canvasConfig)

    def add_widgets(self):
        """Add and configure widgets."""
        self.btn_setInputPath = tk.Button(text="set", master=self.frm_inside)
        self.lbl_inputLabel = tk.Label(text="Input name(s)", master=self.frm_inside)
        CreateTooltip(self.lbl_inputLabel, "Name(s) of the file(s) to be converted")
        
        self.lbl_inputNames = tk.Label(textvariable=self.var_inputNames, master=self.frm_inside, fg="gray")
        CreateTooltip(self.lbl_inputNames, "List of input files with the correct extension")
        
        self.btn_setInputName = tk.Button(text="set", master=self.frm_inside, command=self.setInputName)
        CreateTooltip(self.btn_setInputName, "Select one or more '.com' gaussian input files")
        
        self.lbl_inputType = tk.Label(text="Model type", master=self.frm_inside)
        CreateTooltip(self.lbl_inputType, "Different representational models supported by Gaussian2Blender")
        
        self.lst_modelTypes = ["Ball-and-Stick", "Stick-only", "Van-der-Waals"]
        self.var_modelTypes.set("Ball-and-Stick")
        self.drp_modelTypes = tk.OptionMenu(self.frm_inside, self.var_modelTypes, 
                                            *self.lst_modelTypes, command=self.dropdouwn_callout)
        CreateTooltip(self.drp_modelTypes, "Choose one of the model representation options from this list")

        self.chk_isAnimation = tk.Checkbutton(master=self.frm_inside, text="is animation",
                                           variable=self.var_isAnimation, command=self.updateAnimationState)
        CreateTooltip(self.chk_isAnimation, "Check if the input files will serve as animation frames.")

    def position_widgets(self):
        """Position widgets in the frame."""
        self.lbl_inputLabel.grid(row=1, column=0)
        self.lbl_inputNames.grid(row=1, column=1, sticky="w")
        self.btn_setInputName.grid(row=1, column=2)
        self.lbl_inputType.grid(row=2, column=0, sticky="e")
        self.drp_modelTypes.grid(row=2, column=1, sticky="w")
        self.chk_isAnimation.grid(row=3, column=0)


    def updateAnimationState(self):
        if not self.var_isAnimation.get():
            print("The files will not be treated as animation.")
            return #this is called when che checkbox was checked, and is unchecked now
        if len(self.lst_inputNames) < 2:
            print("Error: There must be more than one file to implement animations.")
            self.var_isAnimation.set(False)  # Uncheck the checkbox if conditions are not met
            return
        print("At least two files are present as input. Make sure they have the same number of elements in the same order for the animation to work properly.")

        
    def allFilesHaveSameValidExtension(self, file_paths):
        """
        Checks if all files in the list have the same valid extension.
    
        :param file_paths: List of file paths.
        :return: True if all files have the same valid extension, False otherwise.
        """
        valid_extensions = {".com", ".xyz"}
        extensions = {os.path.splitext(path)[1].lower() for path in file_paths}
    
        if len(extensions) == 1 and extensions.pop() in valid_extensions:
            return True
        return False
        
    def setInputName(self):
        """
        opens a file dialog and allows to select one or more elements
        updates the input names list and depicts all the elements to convert in the GUI
        """
        str_paths = tk.filedialog.askopenfilenames(initialdir = self.initial_dir)
        if not str_paths:
            return #no files selected
        if self.allFilesHaveSameValidExtension(str_paths):
            self.updateInputNameList(str_paths)
            path = os.path.dirname(str_paths[0])
            print("##### SETTING INPUT FILES TO CONVERT ####")
            self.var_inputPath.set(path)
            for entry in str_paths:
                f_name = os.path.basename(entry)
                print(f_name, "has correct file extension")
        else:
            print("Not all selected files have the same valid extension. Please select files with either '.com' or '.xyz' extension.")

                
    def isValidExtension(self, file_path):
        """
        Checks if the file has an acceptable extension.
        Currently accepts '.com' and leaves a placeholder for '.xyz'.

        :param file_path: Path to the file.
        :return: True if the file has an accepted extension, False otherwise.
        """
        _, file_ext = os.path.splitext(file_path)
        if file_ext.lower() == ".com":
            return True
        elif file_ext.lower() == ".xyz":
            pass  # Placeholder for future implementation
        return False
                
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
