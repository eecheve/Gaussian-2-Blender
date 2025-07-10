import tkinter as tk
import webbrowser
from gui.CreateTooltip import CreateTooltip
from gui.Utility import Utility

class Information(object):
    """
    Region containing the instructions on how to use TheorChem2Blender
    """
    #def __init__(self, parent_class):
    def __init__(self, parent_class, instructions, title="Information", button_name="Help"):
        self.frame = tk.LabelFrame(master=parent_class,#parent_tk,
                                      padx=5, 
                                      text=title, 
                                      fg="blue",
                                      bg="#e0e0e0", 
                                      relief=tk.GROOVE, 
                                      borderwidth=2)
        self.instructions = instructions
        
        self.btn_about = tk.Button(text="About", width=20, master=self.frame, command=self.about)
        self.btn_about.grid(row=0, column=0)
        CreateTooltip(self.btn_about, "Click here to see the current version of TheorChem2Blender")
        
        self.btn_help = tk.Button(text=button_name, width=20, master=self.frame, command=self.help)
        self.btn_help.grid(row=0, column=1)
        CreateTooltip(self.btn_help, "Click here to open a new window with instructions on how to use TheorChem2Blender")
       
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

        text_widget = tk.Text(popup_window, wrap="word", bg="#e0e0e0", width=100, height=20)
        text_widget.tag_configure("normal", font=("Helvetica", 10))
        text_widget.tag_configure("bold", font=("Helvetica", 10, "bold"))
        text_widget.tag_configure("italic", font=("Helvetica", 10, "italic"))
        text_widget.tag_configure("code", font=("Courier", 10))
        
        for part, tag in self.instructions:
            text_widget.insert("end", part, tag)

        text_widget.config(state="disabled") # read-only
        text_widget.grid(row=0, column=0, padx=20, pady=20)

        btn_close = tk.Button(popup_window, text="Close", command=popup_window.destroy)
        btn_close.grid(row=1, column=0, pady=10)
        popup_window.geometry("800x500")

    def open_url(self):
        """Opens JCE seminal paper in a new web browser window"""
        webbrowser.open(self.url)
        
    def about(self):
        """Pops up a small window with version information about the program"""
        popup_window = tk.Toplevel(self.frame)
        popup_window.title("About")
        self._initialize_popup(popup_window)
        popup_window.geometry("800x200")