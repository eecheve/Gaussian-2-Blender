import tkinter as tk
from gui.CreateTooltip import CreateTooltip

class Instructions(object):
    """
    Region containing the instructions on how to use Gaussian2Blender
    """
    def __init__(self, parent):
        self.frame = tk.LabelFrame(master=parent,
                                      padx=5, 
                                      text="How to use Gaussian2Blender", 
                                      fg="blue", 
                                      relief=tk.GROOVE, 
                                      borderwidth=2)
        
        self.btn_help = tk.Button(text="Help", width=20, master=self.frame, command=self.help)
        self.btn_help.grid(row=0, column=0)
        CreateTooltip(self.btn_help, "Click here to open a new window with instructions on how to use Gaussian2Blender")

        # Numbered list of instructions
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

    def help(self):
        """Pops up a small window specifying the isntructions on how to use the program"""
        popup_window = tk.Toplevel(self.frame)
        popup_window.title("Instructions")

        content = tk.Label(popup_window,
                           text=self.instructions_text,
                           fg="black",
                           padx=10, pady=10,
                           justify="left",  # Makes the text left-aligned
                           width=100, height=20,
                           wraplength=500)
        content.grid(row=0, column=0, padx=20, pady=20)
        btn_close = tk.Button(popup_window, text="Close", command=popup_window.destroy)
        btn_close.grid(row=1, column=0, pady=10)
        popup_window.geometry("800x500")  # Customize as needed