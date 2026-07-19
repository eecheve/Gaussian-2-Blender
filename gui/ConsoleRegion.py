import sys
import os

import tkinter as tk
import tkinter.ttk as ttk

from gui.TextRedirector import TextRedirector
from gui.Utility import Utility

class ConsoleRegion(object):
    """
    GUI region that lets the user observe print statements and errors from
    both sides of the app: the GUI's own prints (via the sys.stdout/stderr
    redirect below) and Blender's prints, which arrive indirectly through
    output.log since Blender runs as a separate OS process - see
    poll_log_file().
    """

    # How often (ms) the console checks output.log for new content written
    # by the Blender subprocess, so long-running conversions (animations,
    # multi-file or multi-growth-cell batches) show progress as they happen
    # instead of the console appearing frozen until everything finishes.
    LOG_POLL_INTERVAL_MS = 500

    def __init__(self, parent, log_path):
        self.log_path = log_path

        # Start every app session with a clean log rather than appending
        # onto whatever a previous session left behind.
        Utility.clear_file_contents(self.log_path)

        # How many bytes of output.log this console has already displayed.
        # TextRedirector.write() advances this itself for the GUI's own
        # prints (it knows exactly what it just wrote); poll_log_file()
        # advances it for everything else, i.e. Blender's output. Together
        # these mean no line ever gets displayed twice.
        self.log_bytes_shown = 0

        self.frame = tk.LabelFrame(master=parent,
                                      padx=5,
                                      text="Console",
                                      fg="blue",
                                      bg="#e0e0e0",
                                      relief=tk.GROOVE,
                                      borderwidth=2)
        # height/width here are only the starting size the console asks for -
        # grid_rowconfigure/grid_columnconfigure below (plus sticky="nsew")
        # let it stretch to fill whatever space its container actually gives it.
        self.text = tk.Text(master=self.frame,
                            fg='black', bg="white",
                            height=8,
                            wrap="word")
        self.text.tag_configure("stderr", foreground="#b22222")
        self.text.config(state="disabled")

        self.scrl_text = ttk.Scrollbar(self.frame,
                                       command=self.text.yview)

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        self.text.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
        self.scrl_text.grid(row=0, column=1, sticky="nsew")
        self.text['yscrollcommand'] = self.scrl_text.set

        sys.stdout = TextRedirector(self.text, "stdout", log_path=self.log_path, console_region=self)
        sys.stderr = TextRedirector(self.text, "stderr", log_path=self.log_path, console_region=self)

        self.poll_log_file()

    def poll_log_file(self):
        """
        Reads whatever output.log has grown by since the last check and
        displays it. This is how Blender's print() statements reach the
        console: Blender runs as a separate OS process whose stdout is
        redirected straight to output.log (see
        TheorChem2Blender._run_blender_subprocess), so nothing in this GUI
        process ever sees them directly - polling the file is the only way
        to notice they arrived. Reschedules itself every
        LOG_POLL_INTERVAL_MS regardless of whether anything new was found.
        """
        try:
            with open(self.log_path, "r", encoding="utf-8", errors="replace") as f:
                f.seek(self.log_bytes_shown)
                new_text = f.read()
                self.log_bytes_shown = f.tell()
        except FileNotFoundError:
            new_text = ""

        if new_text:
            self.text.configure(state="normal")
            self.text.insert("1.0", new_text, ("stdout",))
            self.text.configure(state="disabled")

        self.text.after(self.LOG_POLL_INTERVAL_MS, self.poll_log_file)

    def clear_content(self):
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.configure(state="disabled")
