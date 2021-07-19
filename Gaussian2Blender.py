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
root.geometry('%dx%d+0+0' % (800, 600))
root.resizable(0,0)

bPathReg = BlenderPath.BlenderPath(root)
str_blenderPath = bPathReg.searchBlenderPath()
bPathReg.setBlenderPath(str_blenderPath)
aboutReg = AboutRegion.AboutRegion(root)
inputReg = InputRegion.InputRegion(root)
outputReg = OutputRegion.OutputRegion(root, script_dir)
printReg = PrintRegion.PrintRegion(root)
ionReg = IonRegion.IonRegion(root)
codeReg = IonConventions.IonConventions(root)

#w_width, w_height = root.winfo_screenwidth(), root.winfo_screenheight()
#root.geometry('%dx%d+0+0' % (w_width, w_height))

#endregion


#Events
#region
def handle_convert_button(event):
    b_path = bPathReg.var_blenderPath.get()
    i_names = inputReg.lst_inputNames
    
    if utility.findFile("blender.exe", b_path) == False:
        print("The assigned blender path does not contain the blender.exe file")
    else:
        if not i_names:
            print("Please select at least one gaussian input file to convert")
        else:
            export(b_path, i_names)

def reset_to_defaults():
    bPathReg.var_blenderPath.set(str_blenderPath)
    outputReg.var_outputPath.set(outputReg.def_outputPath)
    inputReg.var_inputNames.set("")
    inputReg.lst_inputNames.clear()
    inputReg.var_inputPath.set("")
    #ionReg.int_hasIons.set(0)
    ionReg.int_unitCell.set(0)
    ionReg.activator()
    ionReg.int_hasIons.set(0)
    ionReg.removeAllIons()
    printReg.clear_content()
    #if not printReg.text.get(0): #<----------------------------------BUG!
    #    printReg.text.delete("0", tk.END) #<------------------------BUG!!!!
           
def export(b_path, i_names):
    global script_dir
    o_path = outputReg.ent_outputPath.get()

    if not o_path:
        print("Please paste a path for the output file")
    elif os.path.exists(o_path) == False:
        print("Please paste a path that exists")
    elif os.path.isdir(o_path) == False:
        print("Please paste a folder path instead of a file path")
    else:
        exec_loc = def_scriptsPath + '\ReadMolecules.bat' #<------------------
        i_path = inputReg.var_inputPath.get()
        print("Input path is: ", i_path)
        print()
        print("Output path is: ", o_path)
        print()
        m_type = inputReg.var_modelTypes.get()
        print("Representational model is: ", m_type)
        print()
        o_type = outputReg.var_outputTypes.get()
        print("Rendering as a: ", o_type)
        has_ions = ionReg.int_hasIons.get()
        unit_cell = ionReg.int_unitCell.get()
        if not unit_cell:
            unit_cell=0
        ion_list = ionReg.lst_ions
        str_ionList = ""
        if has_ions == 1:
            print("User chose to add ion information...")
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
                print("No ions specified...")
        else:
            has_ions = 0
            print("Ion information skipped")
        str_ion_and_cell = "(" + str(has_ions) + "_" + str(unit_cell) + ")"
        for i_name in i_names:
            o_name=i_name.split(".")[0]
            print("Building molecule ", o_name)
            subprocess.call([exec_loc, b_path, i_path, i_name, 
                             o_path, o_name, m_type, o_type, 
                             str_ion_and_cell, str_ionList])
            print("-----------------------------------------")
        print("Export of batch molecules completed, please click on 'Reset' to add new molecules")
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
    master=frm_interact)

btn_reset = tk.Button(
    text="Reset",
    width=20,
    master=frm_interact,
    command=reset_to_defaults)

btn_reset.grid(row=0, column=1)
btn_convert.grid(row=0, column=2)

#btn_reset.bind("<Button-1>", reset_to_defaults)
btn_convert.bind("<Button-1>", handle_convert_button)
#endregion

root.mainloop()
