import os
import sys
import subprocess
import tkinter as tk
#from tkinter import *

window = tk.Tk()
window.title("Gaussian input Converter")

# Utility
def find_file(name, path):
    """
    returns true if there is a file with name <name> in <path>
    """
    for root, dirs, files in os.walk(path):
        if name in files:
            return True
        else:
            return False
    return False

#Events
def handle_btn_convert(event):
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
        if find_file("blender.exe", b_path) == False:
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
                    if find_file(i_name + ".com", i_path) == False:
                        print("There is no ", i_name, " in path ", i_path)
                    else:
                        export()

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
            exec_loc = script_dir + '\ReadMolecules.bat'
            subprocess.call([exec_loc, ent_blenderPath.get(), ent_inputPath.get(), ent_inputName.get(), ent_outputPath.get(), ent_outputName.get(), var_modelTypes.get(), var_outputTypes.get()])
            print("Export completed, please close the window now")                

script_dir = os.path.dirname(os.path.realpath(__file__)) #stores the dir of this python script

#defining frames
frm_instructions = tk.Frame(master=window, relief=tk.GROOVE, borderwidth=2)
frm_blender = tk.Frame(master=window, relief=tk.GROOVE, borderwidth=2)
frm_input = tk.Frame(master=window, relief=tk.GROOVE, borderwidth=2)
frm_output = tk.Frame(master=window, relief=tk.GROOVE, borderwidth=2)
frm_interact = tk.Frame(master=window, relief=tk.GROOVE, borderwidth=2)

#fame order
frm_instructions.grid(row=0, columnspan=3)
frm_blender.grid(row=1, columnspan=3, pady=3)
frm_input.grid(row=2, column=0, padx=3, pady=3)
frm_output.grid(row=2, column=1, pady=3)
frm_interact.grid(row=3, columnspan=3, pady=3)

#attributes in instructions frame
lbl_title = tk.Label(
    text="Instructions",
    font='bold',
    master=frm_instructions)

lbl_step1 = tk.Label(
    text="1: Paste or write the path where Blender is installed to the 'blender path' box",
    master=frm_instructions)

lbl_step2 = tk.Label(
    text="2: Paste or write the path location of the Gaussian input file",
    master=frm_instructions)

lbl_step3 = tk.Label(
    text="3: Paste or write the name of the Gaussian input file, including '.com' at the end",
    master=frm_instructions)

lbl_step4 = tk.Label(
    text="4: Select the type of representation in which the input will be rendered",
    master=frm_instructions)

lbl_step5 = tk.Label(
    text="5: Paste or write the desired location for the output file",
    master=frm_instructions)

lbl_step6 = tk.Label(
    text="6: Paste or write the desired name for the output file",
    master=frm_instructions)

lbl_step7 = tk.Label(
    text="7: Select the output file type",
    master=frm_instructions)

lbl_step8 = tk.Label(
    text="8: Click on 'Convert!'",
    master=frm_instructions)

lbl_title.pack()
lbl_step1.pack()
lbl_step2.pack()
lbl_step3.pack()
lbl_step4.pack()
lbl_step5.pack()
lbl_step6.pack()
lbl_step7.pack()
lbl_step8.pack()

#attributes in blender frame
lbl_blenderPath = tk.Label(
    text="blender path",
    master=frm_blender)

ent_blenderPath = tk.Entry(
    width=35,
    master=frm_blender)

lbl_blenderHelp = tk.Label(
    text="folder path for Blender your machine. Default: 'C:\Program Files\Blender Foundation\Blender 2.82'",
    foreground="gray",
    master=frm_blender)

lbl_blenderPath.grid(row=0, column=0)
ent_blenderPath.grid(row=0, column=1, sticky="w")
lbl_blenderHelp.grid(row=0, column=2)

#attributes in input_frame
lbl_inputPath = tk.Label(
    text="input path",
    master=frm_input)

ent_inputPath = tk.Entry(
    width=30,
    master=frm_input)

lbl_iPathHelp = tk.Label(
    text="folder path for the input file",
    foreground="gray",
    master=frm_input)

lbl_inputName = tk.Label(
    text="input name",
    master=frm_input)

ent_inputName = tk.Entry(
    width=30,
    master=frm_input)

lbl_iNameHelp = tk.Label(
    text="Gaussian '.com' input file",
    foreground="gray",
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

lbl_inputPath.grid(row=0,column=0)
ent_inputPath.grid(row=0,column=1)
lbl_iPathHelp.grid(row=0, column=2)

lbl_inputName.grid(row=1, column=0)
ent_inputName.grid(row=1, column=1, sticky="w")
lbl_iNameHelp.grid(row=1, column=2)

lbl_inputType.grid(row=2, column=0, sticky="e")
drp_modelTypes.grid(row=2, column=1, sticky="w")

#attributes in output frame
lbl_outputPath = tk.Label(
    text="output path",
    master=frm_output)

ent_outputPath = tk.Entry(
    width=30,
    master=frm_output)

lbl_oPathHelp = tk.Label(
    text="folder path for output file",
    foreground="gray",
    master=frm_output)

lbl_outputName = tk.Label(
    text="output name",
    master=frm_output)

ent_outputName = tk.Entry(
    width=30,
    master=frm_output)

lbl_oNameHelp = tk.Label(
    text="object output name",
    foreground="gray",
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

lbl_outputPath.grid(row=0, column=0)
ent_outputPath.grid(row=0, column=1)
lbl_oPathHelp.grid(row=0, column=2)

lbl_outputName.grid(row=1, column=0)
ent_outputName.grid(row=1, column=1, sticky="w")
lbl_oNameHelp.grid(row=1, column=2)

lbl_outputType.grid(row=2, column=0, sticky="e")
drp_outputTypes.grid(row=2, column=1, sticky="w")

#attributes in interact frame
btn_convert = tk.Button(
    text="Convert!",
    width=20,
    master=frm_interact)

btn_convert.grid(row=0, column=2)
btn_convert.bind("<Button-1>", handle_btn_convert)

window.mainloop()