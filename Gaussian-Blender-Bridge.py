import os
import sys
import subprocess
import tkinter as tk
from tkinter import filedialog

#Root parameters
#region
root = tk.Tk()
root.title("Gaussian-Blender-Bridge")

script_dir = os.path.dirname(os.path.realpath(__file__)) #stores the dir of this python script
root.iconbitmap(script_dir + "\\misc\\icon.ico")
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
    str_path = tk.filedialog.askopenfilename()
    str_name = os.path.basename(str_path)
    var_inputName.set(str_name)

def setOutputPath(event):
    global var_outputPath
    str_path = tk.filedialog.askdirectory()
    var_outputPath.set(str_path)

def setOutputName(event):
    global var_outputName
    str_path = tk.filedialog.askopenfilename()
    str_name = os.path.basename(str_path)
    var_outputName.set(str_name)

def resetToDefaults(event):
    global var_blenderPath
    global var_inputPath
    global var_outputPath
    global var_inputName
    global var_outputName
    var_blenderPath.set(def_blenderPath)
    var_inputPath.set(def_inputPath)
    var_outputPath.set(def_outputPath)
    var_inputName.set("")
    var_outputName.set("")
           
def export():
    global script_dir
    o_name = ent_outputName.get()
    o_path = ent_outputPath.get()

    if not o_path:
        print("Please paste a path for the output file")
    elif os.path.exists(o_path) == False:
        print("Please paste a path that exists")
    elif os.path.isdir(o_path) == False:
        print("Please paste a folder path instead of a file path")
    else:
        if not o_name:
            print("Please write a name for the output file")
        else:
            print("Will export the object to the path: ", o_path)
            exec_loc = def_scriptsPath + '\ReadMolecules.bat'
            subprocess.call([exec_loc, ent_blenderPath.get(), ent_inputPath.get(), ent_inputName.get(), ent_outputPath.get(), ent_outputName.get(), var_modelTypes.get(), var_outputTypes.get()])
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
frm_definitions = tk.LabelFrame(master=root, padx=116, text="Definitions", relief=tk.GROOVE, borderwidth=2, labelanchor="n")
frm_instructions = tk.LabelFrame(master=root, padx=172, text="Instructions", relief=tk.GROOVE, borderwidth=2, labelanchor="n")
frm_blender = tk.Frame(master=root, padx=106, relief=tk.GROOVE, borderwidth=2)
frm_input = tk.Frame(master=root, padx=5, relief=tk.GROOVE, borderwidth=2)
frm_output = tk.Frame(master=root, padx=5, relief=tk.GROOVE, borderwidth=2)
frm_interact = tk.Frame(master=root, relief=tk.GROOVE, borderwidth=2)
#endregion

#Frame order
#region
frm_definitions.grid(row=0, columnspan=3)
frm_instructions.grid(row=1, columnspan=3, pady=3)
frm_blender.grid(row=2, columnspan=3, pady=3)
frm_input.grid(row=3, column=0, padx=3, pady=3)
frm_output.grid(row=3, column=1, pady=3)
frm_interact.grid(row=4, columnspan=3, pady=3)
#endregion

#Attributes in definition frame
#region
lbl_bPath = tk.Label(
    text="blender path",
    master=frm_definitions)

lbl_blenderHelp = tk.Label(
    text="folder path where Blender is installed in your machine.",
    foreground="#4d4d4d",
    master=frm_definitions)

lbl_iPath = tk.Label(
    text="input path",
    master=frm_definitions)

lbl_iPathHelp = tk.Label(
    text="folder path where the input file is stored.",
    foreground="#4d4d4d",
    master=frm_definitions)

lbl_iName = tk.Label(
    text="input name",
    master=frm_definitions)

lbl_iNameHelp = tk.Label(
    text="Gaussian '.com' input file name. (Including '.com')",
    foreground="#4d4d4d",
    master=frm_definitions)

lbl_oPath = tk.Label(
    text="output path",
    master=frm_definitions)

lbl_oPathHelp = tk.Label(
    text="folder path where the output file will be saved.",
    foreground="#4d4d4d",
    master=frm_definitions)

lbl_oName = tk.Label(
    text="output name",
    master=frm_definitions)

lbl_oNameHelp = tk.Label(
    text="object output name, do not specify file type in the name.",
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

lbl_bPath.grid(row=0, column=0, sticky="w")
lbl_blenderHelp.grid(row=0, column=1, sticky="w")
lbl_iPath.grid(row=1, column=0, sticky="w")
lbl_iPathHelp.grid(row=1, column=1, sticky="w")
lbl_iName.grid(row=2, column=0, sticky="w")
lbl_iNameHelp.grid(row=2, column=1, sticky="w")
lbl_oPath.grid(row=3, column=0, sticky="w")
lbl_oPathHelp.grid(row=3, column=1, sticky="w")
lbl_oName.grid(row=4, column=0, sticky="w")
lbl_oNameHelp.grid(row=4, column=1, sticky="w")
lbl_bConvert.grid(row=5, column=0, sticky="w")
lbl_bConvertHelp.grid(row=5, column=1, sticky="w")
lbl_bReset.grid(row=6, column=0, sticky="w")
lbl_bResetHelp.grid(row=6, column=1, sticky="w")
#endregion

#Attributes in instructions frame
#region
lbl_index0 = tk.Label(
    text="0:",
    master=frm_instructions)

lbl_index1 = tk.Label(
    text="1:",
    master=frm_instructions)

lbl_index2 = tk.Label(
    text="2:",
    master=frm_instructions)

lbl_index3 = tk.Label(
    text="3:",
    master=frm_instructions)

lbl_index4 = tk.Label(
    text="4:",
    master=frm_instructions)

lbl_step0 = tk.Label(
    text="Default values for folder paths are already set.",
    master=frm_instructions,
    fg="#4d4d4d")

lbl_step1 = tk.Label(
    text="If needed, set folder paths to their new location",
    master=frm_instructions,
    fg="#4d4d4d")

lbl_step2 = tk.Label(
    text="Set the input file or write the file name",
    master=frm_instructions,
    fg="#4d4d4d")

lbl_step3 = tk.Label(
    text="Write the output file name",
    master=frm_instructions,
    fg="#4d4d4d")

lbl_step4 = tk.Label(
    text="Click on 'Convert!'",
    master=frm_instructions,
    fg="#4d4d4d")

lbl_index0.grid(row=0, column=0)
lbl_step0.grid(row=0, column=1, sticky="w")

lbl_index1.grid(row=1, column=0)
lbl_step1.grid(row=1, column=1, sticky="w")

lbl_index2.grid(row=2, column=0)
lbl_step2.grid(row=2, column=1, sticky="w")

lbl_index3.grid(row=3, column=0)
lbl_step3.grid(row=3, column=1, sticky="w")

lbl_index4.grid(row=4, column=0)
lbl_step4.grid(row=4, column=1, sticky="w")

#endregion

#Attributes in blender frame
#region
lbl_blenderPath = tk.Label(
    text="blender path",
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
    text="input path",
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
    text="input name",
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
    text="model type",
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

#Attributes in output frame
#region
lbl_outputPath = tk.Label(
    text="output path",
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

lbl_outputName = tk.Label(
    text="output name",
    master=frm_output)

var_outputName = tk.StringVar()
var_outputName.set("")
ent_outputName = tk.Entry(
    width=35,
    master=frm_output,
    textvariable=var_outputName)

btn_setOutputName = tk.Button(
    text="set",
    master=frm_output)

lbl_outputType = tk.Label(
    text="output type",
    master=frm_output)

lst_outputTypes = [
    ".fbx",
    ".obj",
    ".dae"]
var_outputTypes = tk.StringVar()
var_outputTypes.set(".fbx")
drp_outputTypes = tk.OptionMenu(
    frm_output,
    var_outputTypes, 
    *lst_outputTypes)

btn_setOutputPath.bind("<Button-1>", setOutputPath)
btn_setOutputName.bind("<Button-1>", setOutputName)

lbl_outputPath.grid(row=0, column=0)
ent_outputPath.grid(row=0, column=1)
btn_setOutputPath.grid(row=0, column=2)

lbl_outputName.grid(row=1, column=0)
ent_outputName.grid(row=1, column=1, sticky="w")
btn_setOutputName.grid(row=1, column=2)

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