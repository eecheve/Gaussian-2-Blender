import os
import platform
import tkinter as tk

from gui.CreateTooltip import CreateTooltip
from gui.Utility import Utility

class BlenderPath(object):
    """
    A section of the window used to search and set the path
    where Blender is installed on the user's machine.
    This class provides a graphical user interface (GUI) element
    where the user can see the Blender executable path and select
    it if it is not already set. The path is stored and can be
    used by the program to interface with Blender.
    """
    def __init__(self, parent):
        """
        Initialize the BlenderPath GUI section.
    
        :param parent: The parent widget in which this section will be placed.
        """ 
        self.var_blenderPath = tk.StringVar()
        
        self.frame = tk.LabelFrame(master=parent,
                                           text="Blender executable location", 
                                           fg="blue", 
                                           relief=tk.GROOVE, 
                                           width=800, 
                                           height=170, 
                                           borderwidth=2)

        self.lbl_blenderLabel = tk.Label(
            text="Blender path",
            master=self.frame)

        self.ttp_blenderLabel = CreateTooltip(
            self.lbl_blenderLabel,
            "Folder path where Blender is installed in your machine")
    
        self.var_blenderPath.set("")
        self.lbl_blenderPath = tk.Label(
            textvariable = self.var_blenderPath,
            master=self.frame,
            fg="gray")
    
        self.btn_setBlenderPath = tk.Button(
            text="search",
            master=self.frame,
            command=self.lookForBlenderPath)
        self.ttp_setBlenderPath = CreateTooltip(
            self.btn_setBlenderPath,
            "Click here to select blender.exe path if default is not found")
    
        self.lbl_blenderLabel.grid(row=0, column=0)
        self.lbl_blenderPath.grid(row=0, column=1, sticky="w")
        self.btn_setBlenderPath.grid(row=0, column=2, sticky="w")

    def searchBlenderPath(self):
        """
        Searches the default installation directory for Blender's excecutable.
        The search path is different depending on the machine's operating system.

        :return: The path to the Blender installation directory or a failure message.
        :rtype: str
        """
        os_config = {
            "Windows": {
                "default_path": "C:\\Program Files\\Blender Foundation",
                "executable": "blender.exe"
            },
            "Darwin": {
                "default_path": "/Applications/Blender.app",
                "executable": "Blender"
            }
        }
        
        current_os = platform.system()

        if current_os not in os_config:
            return f"Unsupported OS: {current_os}"
        
        config = os_config[current_os]
        blender_exec = config["executable"]
        search_path = config["default_path"]

        if current_os == "Windows":
            print("Windows OS detected. Proceeding to search for Blender executable")
            for root, _, files in os.walk(search_path):
                if blender_exec in files:
                    print(f"Blender executable found in {root}. The search for the Blender path is not necessary")
                    return os.path.abspath(root)
                
        else:
            exec_path = os.path.join(search_path, "Contents", "MacOS")
            bundle = os.path.join(exec_path, "Blender")
            if os.path.isfile(bundle):
                print(f"Blender application found in {exec_path}. The search for Blender path is not necessary")
                return os.path.abspath(exec_path)
            
        print("If Blender is installed, please find its correct location and specify it in the Blender path")
        response = f"{blender_exec} not found"
        print(response)
        return response
                
        
        # blender = "blender.exe"
        # for root, dirs, files in os.walk("C:\\Program Files\\Blender Foundation"):
        #     for name in files:
        #         if name in files:
        #             if name == blender:
        #                 #return os.path.abspath(os.path.join(root, name))
        #                 print("Blender executable found in", self.lbl_blenderPath, "the search for the blender path is not necessary")
        #                 return os.path.abspath(root)
        #         else:
        #             print("blender.exe not found within Program_Files\Blender_Foundation")
        #             print("please instal Blender before using Gaussian-2-Blender or set manually the path in which Blender is installed")
        #             return "blender.exe not found"
                    #sys.stderr.write("blender.exe not found within Program_Files\\Blender_Foundation\n")
                    
    def lookForBlenderPath(self):
        """
        Opens a file dialog for the user to manually select the Blender installation path.
        :return: None
        """
        str_path = tk.filedialog.askdirectory()
        if Utility.findFile("blender.exe", str_path):
            self.var_blenderPath.set(str_path)
        else:
            #print(f"{bcolors.WARNING}Error: blender.exe not found in specified path. Please select the path in which is installed{bcolors.ENDC}")
            print("Error: blender.exe not found in specified path. Please select the path in which is installed")
            self.var_blenderPath.set("blender.exe not found")

    def setBlenderPath(self, str_path):
        """
        Set the Blender path to the specified value.
        :param str_path: The full path to the Blender installation directory.
        :type str_path: str
        """
        self.var_blenderPath.set(str_path)