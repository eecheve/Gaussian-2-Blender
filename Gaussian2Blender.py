import os
import sys
import subprocess

import tkinter as tk
from tkinter import filedialog

#utility modules
from gui.Utility import Utility
from gui.CreateTooltip import CreateTooltip

#gui modules
from gui.BlenderPath import BlenderPath
from gui.AboutRegion import AboutRegion
from gui.InputRegion import InputRegion
from gui.OutputRegion import OutputRegion
from gui.PrintRegion import PrintRegion
from gui.IonRegion import IonRegion
from gui.IonConventions import IonConventions
from gui.ActionsRegion import ActionsRegion

class GaussianToBlenderApp:
    def __init__(self):
        self.root = tk.Tk()
        self.script_dir = os.path.dirname(os.path.realpath(__file__)) #stores the dir of this python script
        #self.def_scriptsPath = script_dir + "\\scripts\\"
        self.def_scriptsPath = os.path.join(self.script_dir, "scripts")
        self._configure_root()
        self._initialize_regions()

    def _configure_root(self):
        self.root.title("Gaussian-2-Blender")
        self.root.iconbitmap(Utility.resource_path("icon.ico")) #comment line while Gaussian2Blender.py is inside gui folder
        #self.root.iconbitmap(script_dir+"\\icon.ico") #uncomment line when Gaussian2Blender.py is outside gui folder
        self.root.geometry('700x600')
        self.root.resizable(0,0)

    def _initialize_regions(self):
        self.bPathReg = BlenderPath(self.root)
        self.str_blenderPath = self.bPathReg.searchBlenderPath()
        self.bPathReg.setBlenderPath(self.str_blenderPath)
        self.aboutReg = AboutRegion(self.root)
        self.inputReg = InputRegion(self.root, self.script_dir)
        self.outputReg = OutputRegion(self.root, self.script_dir)
        self.printReg = PrintRegion(self.root)
        self.ionReg = IonRegion(self.root)
        self.codeReg = IonConventions(self.root)
        self.actionReg = ActionsRegion(parent=self.root, 
                                       on_reset=self.reset_to_defaults, 
                                       on_convert=self.convert_manager)
        self.actionReg.place(row=3, column=1, pady=2, sticky="se")

    def reset_to_defaults(self):
        self.bPathReg.var_blenderPath.set(self.str_blenderPath)
        self.outputReg.var_outputPath.set(self.outputReg.def_outputPath)
        self.inputReg.var_inputNames.set("")
        self.inputReg.lst_inputNames.clear()
        self.inputReg.var_inputPath.set("")
        self.ionReg.int_unitCell.set(0)
        self.ionReg.activator()
        self.ionReg.int_hasIons.set(0)
        self.ionReg.removeAllIons()
        self.printReg.clear_content()

    def exceptions_test_passed(self, b_path, i_names, o_path):
        """
        Validates input parameters for the conversion process.
    
        This function checks whether the required paths and files are valid 
        before running the `convert_manager` function.

        Args:
            b_path (str): Path to the Blender executable.
            i_names (list): List of Gaussian input file names to convert.
            o_path (str): Output directory path.

        Returns:
            bool: True if all tests pass, False otherwise.
        """
        tests = [
            (not Utility.findFile("blender.exe", b_path), 
                "The assigned blender path does not contain the blender.exe file"),
            (i_names is None or not i_names, 
                "Please select at least one Gaussian input file to convert"),
            (not o_path, 
                "Please paste a path for the output file"),
            (not os.path.exists(o_path), 
                "Please paste a path that exists"),
            (not os.path.isdir(o_path), 
                "Please paste a folder path instead of a file path")
        ]
        for condition, error_message in tests:
            if condition:
                print(error_message)
                return False
        return True
        
    def overwrite_parameters_script(self, i_path, i_name, model_type, o_path, o_name, o_type, 
                              is_ionic, unit_cell, str_ion_list):
        """
        overwrites bat script to handle the export or animation of molecules
    
        :param i_path: Input file path
        :param i_name: Input file name
        :param model_type: Type of model to export
        :param o_path: Output directory path
        :param o_name: Output file name
        :param o_type: Output type
        :param is_ionic: Whether the input is ionic
        :param unit_cell: Whether the input contains a unit cell
        :param str_ion_list: List of ions in string format
        """
        g2b_path = os.path.dirname(os.path.realpath(__file__)) #Gaussian2Blender base directory
        params_script = os.path.join(g2b_path, "scripts", "parameters.txt")

        if not os.path.exists(params_script):
            raise FileNotFoundError(f"Cannot find 'parameters.txt' at {params_script}")

        Utility.clear_file_contents(params_script)
        lines = [
            i_path,
            i_name,
            o_path,
            o_name,
            model_type,
            o_type,
            str(is_ionic),
            str(unit_cell),
            str_ion_list,
        ]
        Utility.append_lines_to_file(params_script, lines)
    
    def individual_convert(self, exec_loc, b_path, i_path, i_name, model_type, o_path, 
                       o_name, o_type, is_ionic, unit_cell, str_ion_list):
        """ 
        Function to execute bat file that communicates with blender's python API 
    
        :param excec_loc: path to the ReadMolecules.bat file which communicates with python
        :param b_path: location of the blender executable
        :param i_path: list of input specifications
        :param i_name: list of input names to be converted into 3D objects
        :param model_type: type of model to export
        :param o_path: output path
        :param o_name: output names
        :param o_type: output type
        :param is_ionic: boolean specifyig wether the input is ionic
        :param unit_cell: boolean specifying whether the input contains a unit cell
        :param str_ion_list: list of strings containing all the ions within the input
        """
        self.overwrite_parameters_script(i_path, i_name, model_type, o_path, o_name, o_type, 
                                    is_ionic, unit_cell, str_ion_list)
        subprocess.call([exec_loc, b_path])
    
    def assign_ionic_params(self):
        is_ionic = self.ionReg.int_hasIons.get()
        if not is_ionic:
            is_ionic = "0"
            str_ionList = "---"
        unit_cell = self.ionReg.int_unitCell.get()
        if not unit_cell:
            unit_cell = "0"
        ion_list = self.ionReg.lst_ions
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
        
    def convert_manager(self):
        """
        Manages the process of converting Gaussian input files to 3D object files using Blender's API.

        The function performs the following steps:
        1. Collects necessary paths and parameters for the conversion process.
        2. Validates the inputs using the `exceptions_test_passed` function.
        3. If validation succeeds:
            - Retrieves ionic parameters.
            - Iterates through the list of input files and calls the `individual_convert` function to process each file.
        4. If validation fails, outputs relevant error messages to the console.
        """
        exec_loc = self.def_scriptsPath + '\ReadMolecules.bat' #excecutable location
        anim_frames_path = self.def_scriptsPath + '\\animation_frames.txt' #animation frmaes location
        b_path = self.bPathReg.var_blenderPath.get() #blender path
        i_path = self.inputReg.var_inputPath.get() #input specifications
        i_names = self.inputReg.lst_inputNames #files to convert
        model_type = self.inputReg.var_modelTypes.get() #model specifications
        o_path = self.outputReg.ent_outputPath.get() #output path
        o_type = self.outputReg.var_outputTypes.get() #output type
        if self.exceptions_test_passed(b_path, i_names, o_path): 
            params = self.assign_ionic_params()
            is_ionic = params[0]
            unit_cell = params[1]
            ion_list = params[2]
            str_ion_list = params[3]
            for i in range(len(i_names)):
                print("Converting", i+1, "of", len(i_names))
                self.individual_convert(exec_loc, b_path, i_path, i_names[i], model_type,
                                    o_path, i_names[i].split(".")[0], o_type, is_ionic,
                                    unit_cell, str_ion_list)     
        else:
            print("Cannot convert input to fbx animation, check console for errors")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = GaussianToBlenderApp()
    app.run()