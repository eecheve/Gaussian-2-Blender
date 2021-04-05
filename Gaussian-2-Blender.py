import os
import sys
import subprocess
import tkinter as tk
from tkinter import filedialog

#Preprocess
# This allows using resources from global paths
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
#endPreprocess

#Root parameters
#region
root = tk.Tk()
root.title("Gaussian-2-Blender")

script_dir = os.path.dirname(os.path.realpath(__file__)) #stores the dir of this python script
root.iconbitmap(resource_path("icon.ico"))
root.resizable(width=0, height=0)
#endregion

#Utility
#region 
def findFile(name, path):
    """
    returns true if there is a file with name <name> in <path>
    """
    for root, dirs, files in os.walk(path):
        if name in files:
            return True
        else:
            return False
    return False

#endregion

#Events
#region
def handleConvertButton(event):
    b_path = ent_blenderPath.get()
    
    i_name = ent_inputName.get()
    i_path = ent_inputPath.get()
    
    if not b_path:
        print("Please paste the path for Blender in your machine")
    elif os.path.exists(b_path) == False:
        print("Please paste a blender path that exists")
    elif os.path.isdir(b_path) == False:
        print("Please paste a folder path, not a file path")
    else:
        if findFile("blender.exe", b_path) == False:
            print("This folder path does not contain the blender.exe file")
        else:
            if not i_path:
                print("Please paste a path for the input file")
            elif os.path.exists(i_path) == False:
                print("Please paste an input path that exists")
            elif os.path.isdir(i_path) == False:
                print("Please paste a folder path, not a file path")
            else:
                if not i_name:
                    print("Please write the name for the input file")
                else:
                    if findFile(i_name, i_path) == False:
                        print("There is no ", i_name, " in path ", i_path)
                    else:
                        export()

def setBlenderPath(event):
    global var_blenderPath
    str_path = tk.filedialog.askdirectory()
    var_blenderPath.set(str_path)

def setInputPath(event):
    global var_inputPath
    str_path = tk.filedialog.askdirectory()
    var_inputPath.set(str_path)

def setInputName(event):
    global var_inputName
    global lst_inputNames
    str_paths = tk.filedialog.askopenfilenames()
    updateInputNameList(str_paths)
    var_inputName.set(lst_inputNames[0])

def setOutputPath(event):
    global var_outputPath
    str_path = tk.filedialog.askdirectory()
    var_outputPath.set(str_path)

def updateInputNameList(string_list):
    global var_inputNameList
    global lst_inputNames
    lst_inputNames.clear()
    var_inputNameList.set("")
    s = ""
    for entry in string_list:
        n = os.path.basename(entry)
        e = n + "\n"
        s += e
        lst_inputNames.append(n)
    var_inputNameList.set(s)

def resetToDefaults(event):
    global var_blenderPath
    global var_inputPath
    global var_outputPath
    global var_inputName
    global var_inputNameList
    global lst_inputNames
    var_blenderPath.set(def_blenderPath)
    var_inputPath.set(def_inputPath)
    var_outputPath.set(def_outputPath)
    var_inputName.set("")
    lst_inputNames.clear()
    var_inputNameList.set("")
           
def export():
    global script_dir
    o_path = ent_outputPath.get()
    b_path = ent_blenderPath.get()

    if not o_path:
        print("Please paste a path for the output file")
    elif os.path.exists(o_path) == False:
        print("Please paste a path that exists")
    elif os.path.isdir(o_path) == False:
        print("Please paste a folder path instead of a file path")
    else:
        print("Will export the object to the path: ", o_path)
        exec_loc = def_scriptsPath + '\ReadMolecules.bat'
        i_path = ent_inputPath.get()
        m_type = var_modelTypes.get()
        o_type = var_outputTypes.get()
        if not lst_inputNames:
            i_name = var_inputName.get()
            o_name=i_name.split(".")[0]
            print("Building molecule ", o_name)
            subprocess.call([exec_loc, b_path, i_path, i_name, 
                             o_path, o_name, m_type, o_type])
            print("-----------------------------------------")
        else:
            for i_name in lst_inputNames:
                o_name=i_name.split(".")[0]
                print("Building molecule ", o_name)
                subprocess.call([exec_loc, b_path, i_path, i_name, 
                                 o_path, o_name, m_type, o_type])
                print("-----------------------------------------")
        print("Export completed, please close the window now")
#endregion

#Default path values
#region
def_blenderPath = "C:\Program Files\Blender Foundation\Blender 2.82"
def_inputPath = script_dir + "\\input_examples\\inorganic\\"
def_outputPath = script_dir + "\\output\\"
def_scriptsPath = script_dir + "\\scripts\\"
#endregion

#Defining frames
#region
frm_definitions = tk.LabelFrame(master=root, text="Definitions", fg="blue", relief=tk.GROOVE, width=650, height=170, borderwidth=2)
frm_blender = tk.LabelFrame(master=root, text="Blender path", fg="blue", relief=tk.GROOVE, borderwidth=2)
frm_input = tk.LabelFrame(master=root, padx=5, text="Input", fg="blue", relief=tk.GROOVE, borderwidth=2)
frm_output = tk.LabelFrame(master=root, padx=5, text="Output", fg="blue", relief=tk.GROOVE, width=325, height=102, borderwidth=2)
frm_interpreted = tk.LabelFrame(master=root, text="Molecule(s)", fg="blue", padx=5, relief=tk.GROOVE, borderwidth=2)
frm_interact = tk.LabelFrame(master=root, text="Actions", fg="blue", relief=tk.GROOVE,  borderwidth=2)
#endregion

#Frame order
#region
frm_definitions.grid(row=0, columnspan=3)
frm_definitions.grid_propagate(0)
frm_blender.grid(row=1, columnspan=3, pady=3)
frm_input.grid(row=2, column=0, padx=3, pady=3)
frm_output.grid(row=2, column=1, pady=3)
frm_output.grid_propagate(0)
frm_interpreted.grid(row=3, column=0, pady=3)
frm_interact.grid(row=3, column=1, pady=3)
#endregion

#Attributes in definition frame
#region
lbl_bPath = tk.Label(
    text="Blender path",
    master=frm_definitions)

lbl_blenderHelp = tk.Label(
    text="Folder path where Blender is installed in your machine.",
    foreground="#4d4d4d",
    master=frm_definitions)

lbl_iPath = tk.Label(
    text="Input path",
    master=frm_definitions)

lbl_iPathHelp = tk.Label(
    text="Folder path where the input file is stored.",
    foreground="#4d4d4d",
    master=frm_definitions)

lbl_iName = tk.Label(
    text="Input name",
    master=frm_definitions)

lbl_iNameHelp = tk.Label(
    text="Gaussian '.com' input file name. (Including '.com')",
    foreground="#4d4d4d",
    master=frm_definitions)

lbl_oPath = tk.Label(
    text="Output path",
    master=frm_definitions)

lbl_oPathHelp = tk.Label(
    text="Folder path where the output file will be saved.",
    foreground="#4d4d4d",
    master=frm_definitions)

lbl_oName = tk.Label(
    text="Output name",
    master=frm_definitions)

lbl_oNameHelp = tk.Label(
    text="Object output name, do not specify file type in the name.",
    foreground="#4d4d4d",
    master=frm_definitions)

lbl_bConvert = tk.Label(
    text="Convert!",
    master=frm_definitions)

lbl_bConvertHelp = tk.Label(
    text="To convert from .com to specified file type",
    foreground="#4d4d4d",
    master=frm_definitions)

lbl_bReset = tk.Label(
    text="Reset",
    master=frm_definitions)

lbl_bResetHelp = tk.Label(
    text="To reset the folder paths to the default values",
    foreground="#4d4d4d",
    master=frm_definitions)

lbl_bPath.grid(row=0, column=0, sticky="e")
lbl_blenderHelp.grid(row=0, column=1, sticky="w")
lbl_iPath.grid(row=1, column=0, sticky="e")
lbl_iPathHelp.grid(row=1, column=1, sticky="w")
lbl_iName.grid(row=2, column=0, sticky="e")
lbl_iNameHelp.grid(row=2, column=1, sticky="w")
lbl_oPath.grid(row=3, column=0, sticky="e")
lbl_oPathHelp.grid(row=3, column=1, sticky="w")
lbl_oName.grid(row=4, column=0, sticky="e")
lbl_oNameHelp.grid(row=4, column=1, sticky="w")
lbl_bConvert.grid(row=5, column=0, sticky="e")
lbl_bConvertHelp.grid(row=5, column=1, sticky="w")
lbl_bReset.grid(row=6, column=0, sticky="e")
lbl_bResetHelp.grid(row=6, column=1, sticky="w")
#endregion

#Attributes in blender frame
#region
lbl_blenderPath = tk.Label(
    text="Blender path",
    master=frm_blender)

var_blenderPath = tk.StringVar()
var_blenderPath.set(def_blenderPath)
ent_blenderPath = tk.Entry(
    width=50,
    master=frm_blender,
    textvariable=var_blenderPath)

btn_setBlenderPath = tk.Button(
    text="set",
    master=frm_blender)

lbl_blenderPath.grid(row=0, column=0)
ent_blenderPath.grid(row=0, column=1, sticky="w")
btn_setBlenderPath.grid(row=0, column=2, sticky="w")

btn_setBlenderPath.bind("<Button-1>", setBlenderPath)
#endregion

#Attributes in input_frame
#region
lbl_inputPath = tk.Label(
    text="Input path",
    master=frm_input)

var_inputPath = tk.StringVar()
var_inputPath.set(def_inputPath)
ent_inputPath = tk.Entry(
    width=35,
    master=frm_input,
    textvariable=var_inputPath)

btn_setInputPath = tk.Button(
    text="set",
    master=frm_input)

lbl_inputName = tk.Label(
    text="Input name(s)",
    master=frm_input)

var_inputName = tk.StringVar()
var_inputName.set("")
ent_inputName = tk.Entry(
    width=35,
    master=frm_input,
    textvariable=var_inputName)

btn_setInputName = tk.Button(
    text="set",
    master=frm_input)

lbl_inputType = tk.Label(
    text="Model type",
    master=frm_input)

lst_modelTypes = [
    "Ball-and-Stick",
    "Stick-only",
    "Van-der-Waals"]
var_modelTypes = tk.StringVar()
var_modelTypes.set("Ball-and-Stick")
drp_modelTypes = tk.OptionMenu(
    frm_input,
    var_modelTypes, 
    *lst_modelTypes)

btn_setInputPath.bind("<Button-1>", setInputPath)
btn_setInputName.bind("<Button-1>", setInputName)

lbl_inputPath.grid(row=0,column=0)
ent_inputPath.grid(row=0,column=1)
btn_setInputPath.grid(row=0, column=2)

lbl_inputName.grid(row=1, column=0)
ent_inputName.grid(row=1, column=1, sticky="w")
btn_setInputName.grid(row=1, column=2)

lbl_inputType.grid(row=2, column=0, sticky="e")
drp_modelTypes.grid(row=2, column=1, sticky="w")
#endregion

#Attributes in interpreted frame
#region
lst_inputNames = []
var_inputNameList = tk.StringVar()
var_inputNameList.set("")
lbl_inputNameList = tk.Label(
    textvariable=var_inputNameList,
    master=frm_interpreted,
    width=35,
    foreground="#4d4d4d")

lbl_inputNameList.grid(row=0, column=0, sticky="w")
#endregion

#Attributes in output frame
#region
lbl_outputPath = tk.Label(
    text="Output path",
    master=frm_output)

var_outputPath = tk.StringVar()
var_outputPath.set(def_outputPath)
ent_outputPath = tk.Entry(
    width=35,
    master=frm_output,
    textvariable=var_outputPath)

btn_setOutputPath = tk.Button(
    text="set",
    master=frm_output)

lbl_outputType = tk.Label(
    text="Output type",
    master=frm_output)

lst_outputTypes = [
    ".fbx",
    ".obj",
    ".dae",
    ".x3d"]
var_outputTypes = tk.StringVar()
var_outputTypes.set(".fbx")
drp_outputTypes = tk.OptionMenu(
    frm_output,
    var_outputTypes, 
    *lst_outputTypes)

btn_setOutputPath.bind("<Button-1>", setOutputPath)

lbl_outputPath.grid(row=0, column=0)
ent_outputPath.grid(row=0, column=1)
btn_setOutputPath.grid(row=0, column=2)

lbl_outputType.grid(row=2, column=0, sticky="e")
drp_outputTypes.grid(row=2, column=1, sticky="w")
#endregion

#Attributes in interact frame
#region
btn_convert = tk.Button(
    text="Convert!",
    width=20,
    master=frm_interact)

btn_reset = tk.Button(
    text="Reset",
    width=20,
    master=frm_interact)

btn_reset.grid(row=0, column=1)
btn_convert.grid(row=0, column=2)

btn_reset.bind("<Button-1>", resetToDefaults)
btn_convert.bind("<Button-1>", handleConvertButton)
#endregion

root.mainloop()