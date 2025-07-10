import tkinter as tk
from gui.CreateTooltip import CreateTooltip

class ActionsRegion:
    def __init__(self, parent, on_reset, on_convert, current_os, g2b_path):
        """
        Initializes the interact frame.

        :param parent: The parent widget (e.g., the root or a frame).
        :param on_reset: Callback function to reset the interface to defaults.
        :param on_convert: Callback function to manage the conversion process.
        """
        self.current_os = current_os
        self.g2b_path = g2b_path
        self.frame = tk.LabelFrame(master=parent, text="Actions", fg="blue", bg="#e0e0e0", relief=tk.GROOVE, borderwidth=2)
        self.on_reset = on_reset
        self.on_convert = on_convert
        self._create_widgets()

    def _create_widgets(self):
        """Creates and positions the buttons within the interact frame."""
        # Reset button
        self.btn_reset = tk.Button(text="Reset", width=20, master=self.frame, command=self.on_reset)
        CreateTooltip(self.btn_reset, "Click here to reset input values to default")
        self.btn_reset.grid(row=0, column=1)

        # Convert button
        self.btn_convert = tk.Button(text="Convert!", width=20, master=self.frame, command=self.on_convert)
        CreateTooltip(self.btn_convert, "Click here to convert the molecule(s) to the specified format")
        self.btn_convert.grid(row=0, column=2)