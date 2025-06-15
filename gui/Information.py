import tkinter as tk
import webbrowser
from gui.CreateTooltip import CreateTooltip
from gui.Utility import Utility

class Information(object):
    """
    Region containing the instructions on how to use TheorChem2Blender
    """
    def __init__(self, parent_class, parent_tk):
        self.frame = tk.LabelFrame(master=parent_tk,
                                      padx=5, 
                                      text="TheorChem2Blender Information", 
                                      fg="blue",
                                      bg="#e0e0e0", 
                                      relief=tk.GROOVE, 
                                      borderwidth=2)
        
        self.btn_about = tk.Button(text="About", width=20, master=self.frame, command=self.about)
        self.btn_about.grid(row=0, column=0)
        CreateTooltip(self.btn_about, "Click here to see the current version of TheorChem2Blender")
        
        self.btn_help = tk.Button(text="Help", width=20, master=self.frame, command=self.help)
        self.btn_help.grid(row=0, column=1)
        CreateTooltip(self.btn_help, "Click here to open a new window with instructions on how to use TheorChem2Blender")

        self.btn_help_single = tk.Button(text="Guide: single convert", width=20, master=self.frame, 
                                         command=parent_class.help_single_convert)
        self.btn_help_single.grid(row=0, column=2, padx=(30, 0))
        CreateTooltip(self.btn_help_single, "Click here to for a guided walkthrough to convert a single molecule")

        self.btn_help_anim = tk.Button(text="Guide: animation convert", width=20, master=self.frame, 
                                         command=parent_class.help_animation_convert)
        self.btn_help_anim.grid(row=0, column=3)
        CreateTooltip(self.btn_help_anim, "Click here to for a guided walkthrough to make an animation")

        self.instructions_text = (
            "1. Set the path to the Blender executable by navigating to the Blender installation directory.\n\n"
            "2. Select the Gaussian input files that you want to convert.\n\n"
            "3. Choose the output directory where the converted files will be saved.\n\n"
            "4. Choose the type of model you want to export (e.g., ball-and-stick, van-der-Waals, etc.).\n\n"
            "5. Set up any ionic parameters if your molecule is ionic. You can add ions manually.\n\n"
            "6. Click 'Convert!' to start the conversion process. This will create the output files in the specified directory.\n\n"
            "7. If you need to reset the input fields, click 'Reset' to restore default values.\n\n"
            "8. Check the output console for progress and any error messages during the conversion process."
        )
        
        self.about_text = (
            "TheorChem2Blender was written and is maintained by Dr. Echeverri-Jimenez\n"
            "Please cite the following paper if you use this tool: J. Chem. Educ. 2021, 98(10), 3348-3355\n"
            "To access the original paper follow this url: https://pubs.acs.org/doi/10.1021/acs.jchemed.1c00515"
            )
               
    def _initialize_popup(self, popup):

        self.about_info = tk.Label(master=popup,
                                   text=self.about_text,
                                   bg="#e0e0e0",
                                   fg='black')
        self.lbl_ver = tk.Label(master=popup,
                                    text="version: ",
                                    bg="#e0e0e0",
                                    fg="black")
        self.lbl_version = tk.Label(master=popup,
                                    text="2025.1.0 ",
                                    bg="#e0e0e0",
                                    fg="gray")
        
        self.lbl_auth = tk.Label(master=popup,
                                 text="cer3D-Cayey Group",
                                 bg="#e0e0e0",
                                 fg="gray")

        self.about_info.grid(row=0, column=0, columnspan=2)
        self.lbl_ver.grid(row=1, column=0)
        self.lbl_version.grid(row=1, column=1)
        self.lbl_auth.grid(row=2, column=0, columnspan=2)

        self.btn_close = tk.Button(popup, text="Close", command=popup.destroy)
        self.btn_close.grid(row=3, column=0, pady=10)
       
    def help(self):
        """Pops up a small window specifying the isntructions on how to use the program"""
        popup_window = tk.Toplevel(self.frame)
        popup_window.title("Instructions")

        content = tk.Label(popup_window,
                           text=self.instructions_text,
                           fg="black",
                           bg="#e0e0e0",
                           padx=10, pady=10,
                           justify="left",  # Makes the text left-aligned
                           width=100, height=20,
                           wraplength=500)
        content.grid(row=0, column=0, padx=20, pady=20)
        btn_close = tk.Button(popup_window, text="Close", command=popup_window.destroy)
        btn_close.grid(row=1, column=0, pady=10)
        popup_window.geometry("800x500")  # Customize as needed

    def open_url(self):
        """Opens JCE seminal paper in a new web browser window"""
        webbrowser.open(self.url)
        
    def about(self):
        """Pops up a small window with version information about the program"""
        popup_window = tk.Toplevel(self.frame)
        popup_window.title("About")
        self._initialize_popup(popup_window)
        popup_window.geometry("800x200")  # Customize as needed