class TextRedirector(object):
    """To be able to see print statements in the GUI"""
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("1.0", str, (self.tag,)) #line that inserts print and errors at the top
        self.widget.configure(state="disabled")