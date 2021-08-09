import os
import sys
import subprocess

import tkinter as tk
from tkinter import filedialog

import Utility
utility = Utility.Utility

import CreateTooltip
tooltip = CreateTooltip.CreateTooltip

import BlenderPath
import AboutRegion
import InputRegion
import OutputRegion
import PrintRegion
import IonRegion
import IonConventions

#Root parameters
#region
root = tk.Tk()
root.title("Gaussian-2-Blender")
script_dir = os.path.dirname(os.path.realpath(__file__)) #stores the dir of this python script
#root.iconbitmap(utility.resource_path("icon.ico")) 
root.iconbitmap(script_dir+"\\icon.ico")
root.geometry('%dx%d+0+0' % (700, 600))
root.resizable(0,0)

bPathReg = BlenderPath.BlenderPath(root)
str_blenderPath = bPathReg.searchBlenderPath()
bPathReg.setBlenderPath(str_blenderPath)
aboutReg = AboutRegion.AboutRegion(root)
inputReg = InputRegion.InputRegion(root, script_dir)
outputReg = OutputRegion.OutputRegion(root, script_dir)
printReg = PrintRegion.PrintRegion(root)
ionReg = IonRegion.IonRegion(root)
codeReg = IonConventions.IonConventions(root)

#w_width, w_height = root.winfo_screenwidth(), root.winfo_screenheight()
#root.geometry('%dx%d+0+0' % (w_width, w_height))

#endregion


#Events
#region
def reset_to_defaults():
    bPathReg.var_blenderPath.set(str_blenderPath)
    outputReg.var_outputPath.set(outputReg.def_outputPath)
    inputReg.var_inputNames.set("")
    inputReg.lst_inputNames.clear()
    inputReg.var_inputPath.set("")
    ionReg.int_unitCell.set(0)
    ionReg.activator()
    ionReg.int_hasIons.set(0)
    ionReg.removeAllIons()
    printReg.clear_content()
               
def convert_manager():
    exec_loc = def_scriptsPath + '\ReadMolecules.bat'
    anim_frames_path = def_scriptsPath + '\\animation_frames.txt'
    b_path = bPathReg.var_blenderPath.get()
    i_path = inputReg.var_inputPath.get()
    i_names = inputReg.lst_inputNames
    model_type = inputReg.var_modelTypes.get()
    o_path = outputReg.ent_outputPath.get()
    o_type = outputReg.var_outputTypes.get()
    if exceptions_test_passed(b_path, i_names, o_path):
        params = assign_ionic_params()
        is_ionic = params[0]
        unit_cell = params[1]
        ion_list = params[2]
        str_ion_list = params[3]
        for i in range(len(i_names)):
            print("Converting", i+1, "of", len(i_names))
            individual_convert(exec_loc, b_path, i_path, i_names[i], model_type,
                               o_path, i_names[i].split(".")[0], o_type, is_ionic,
                               unit_cell, str_ion_list)     
    else:
        print("Cannot convert input to fbx animation, check console for errors")


def individual_convert(exec_loc, b_path, i_path, i_name, model_type, o_path, 
                       o_name, o_type, is_ionic, unit_cell, str_ion_list):
    overwrite_parameters_script(i_path, i_name, model_type, o_path, o_name, o_type, 
                                is_ionic, unit_cell, str_ion_list)
    subprocess.call([exec_loc, b_path])
 
def exceptions_test_passed(b_path, i_names, o_path):
    if utility.findFile("blender.exe", b_path) == False:
        print("The assigned blender path does not contain the blender.exe file")
        return False
    elif not i_names:
        print("Please select at least one gaussian input file to convert")
        return False
    elif not o_path:
        print("Please paste a path for the output file")
        return False
    elif os.path.exists(o_path) == False:
        print("Please paste a path that exists")
        return False
    elif os.path.isdir(o_path) == False:
        print("Please paste a folder path instead of a file path")
        return False
    else:
        return True

def assign_ionic_params():
    is_ionic = ionReg.int_hasIons.get()
    if not is_ionic:
        is_ionic = "0"
        str_ionList = "---"
    unit_cell = ionReg.int_unitCell.get()
    if not unit_cell:
        unit_cell = "0"
    ion_list = ionReg.lst_ions
    str_ionList = ""
    if is_ionic == 1:
        is_ionic = "1"
        if ion_list:
            for ion in ion_list:
                charge_coord = ion.var_chargeCoord.get().strip("()")
                lst_pair = charge_coord.split(',')
                str_charge = lst_pair[0]
                str_coord = lst_pair[1]
                str_ionList += "("
                str_ionList += ion.var_element.get()
                str_ionList += "_"
                str_ionList += str_charge
                str_ionList += "_"
                str_ionList += str_coord
                str_ionList += ")_"
            str_ionList = str_ionList[:-1]
            print(str_ionList)
        else:
            str_ionList = "---"
    else:
        str_ionList = "---"
    return is_ionic, unit_cell, ion_list, str_ionList

def overwrite_parameters_script(i_path, i_name, model_type, o_path, o_name, o_type, 
                              is_ionic, unit_cell, str_ion_list):
    """overwrites bat script to handle the export or animation of molecules"""
    lines = []
    params_script = def_scriptsPath + '\parameters.txt' #<------------------
    utility.clear_file_contents(params_script)
    lines.append(i_path)
    lines.append(i_name)
    lines.append(o_path)
    lines.append(o_name)
    lines.append(model_type)
    lines.append(o_type)
    lines.append(str(is_ionic))
    lines.append(str(unit_cell))
    lines.append(str_ion_list)
    utility.append_lines_to_file(params_script, lines)
#endregion

#Default path values
def_scriptsPath = script_dir + "\\scripts\\"

#Defining frames
frm_interact = tk.LabelFrame(master=root, text="Actions", fg="blue", relief=tk.GROOVE,  borderwidth=2)

#Frame order
frm_interact.grid(row=3, column=1, pady=2, sticky="se")

#Attributes in interact frame
#region
btn_convert = tk.Button(
    text="Convert!",
    width=20,
    master=frm_interact,
    command=convert_manager)
    
ttp_convert = tooltip(
    btn_convert,
    "Click here to convert the molecule(s) to the specified format")

btn_reset = tk.Button(
    text="Reset",
    width=20,
    master=frm_interact,
    command=reset_to_defaults)
    
ttp_reset = tooltip(
    btn_reset,
    "Click here to reset input values to default")

btn_reset.grid(row=0, column=1)
btn_convert.grid(row=0, column=2)
#endregion

root.mainloop()
