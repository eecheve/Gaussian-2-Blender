import tkinter as tk

class CreateTooltip(object): #https://stackoverflow.com/questions/3221956/how-do-i-display-tooltips-in-tkinter
    """
    A class to create tooltips for a given widget in Tkinter.

    This class binds event handlers to the widget to show and hide tooltips
    when the mouse hovers over or leaves the widget.
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 180   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        """
        Handles the mouse entering the widget. Schedules the tooltip to be shown.

        :param event: The event triggered by the mouse entering the widget.
        """
        self.schedule()

    def leave(self, event=None):
        """
        Handles the mouse leaving the widget. Unschedules and hides the tooltip.

        :param event: The event triggered by the mouse leaving the widget.
        """
        self.unschedule()
        self.hidetip()

    def schedule(self):
        """
        Schedules the tooltip to be shown after a delay.

        Cancels any previously scheduled tooltip and sets a new timer to show the tooltip.
        """
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        """
        Cancels any scheduled tooltip display.

        If there is an active scheduled tooltip, it will be cancelled.
        """
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        """
        Displays the tooltip near the widget.
        Creates a Toplevel window with the tooltip text and positions it near the widget.
        
        :param event: The event triggered by the mouse entering the widget.
        """
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength, foreground='black')
        label.pack(ipadx=1)

    def hidetip(self):
        """
        Hides the currently displayed tooltip.
        Destroys the Toplevel window containing the tooltip.
        """
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()


