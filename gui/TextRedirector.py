class TextRedirector(object):
    """
    Sends print()/traceback output to the Console tab's Text widget, and -
    when a log_path is given - also appends it to output.log.

    That log file is what lets Blender's own print() statements reach the
    same console: Blender runs as a separate OS process (see
    TheorChem2Blender._run_blender_subprocess), so its output is invisible
    to this redirect and instead gets written straight to output.log by the
    OS. ConsoleRegion.poll_log_file() tails that file for content this
    class didn't already insert directly - see console_region below.
    """
    def __init__(self, widget, tag="stdout", log_path=None, console_region=None):
        self.widget = widget
        self.tag = tag
        self.log_path = log_path
        self.console_region = console_region

    def write(self, text):
        self.widget.configure(state="normal")
        self.widget.insert("1.0", text, (self.tag,)) #line that inserts print and errors at the top
        self.widget.configure(state="disabled")

        if self.log_path:
            # newline="" so the file's byte offsets are predictable (no
            # \n -> \r\n translation to account for) - poll_log_file() and
            # this write share the same file via those offsets.
            with open(self.log_path, "a", encoding="utf-8", newline="") as f:
                f.write(text)
                if self.console_region is not None:
                    self.console_region.log_bytes_shown = f.tell()

    def flush(self):
        """No-op: present so this object behaves like a real file for any
        code that calls sys.stdout.flush()/sys.stderr.flush() directly."""
        pass
