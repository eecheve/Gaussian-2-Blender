import tkinter as tk

from gui.CreateTooltip import CreateTooltip
from gui.ScreenSizeManager import ScreenSizeManager


class RepeatableRowGroup(object):
    """
    Manages a labeled, repeatable list of rows: an optional header label,
    a container where rows stack vertically, and three buttons (add /
    remove last / remove all) that build and destroy rows on demand.

    This class does not know what a "row" looks like on the inside - it
    just needs a `row_factory` function that builds one and hands it back.
    Any row object handed back must provide:
        - a `.frame` attribute (the widget to display)
        - a `.destroy()` method (to remove it from the screen)
        - a `.get_values()` method (used by get_row_values() below)

    This same class is used twice in UnitCellRegion.py:
        - Once for the list of unit cell growth rows (with row spacing and
          scrolling turned on, since that list can grow tall)
        - Once more, nested inside each growth row, for that row's own
          list of Miller planes (left at its small default spacing, with
          scrolling turned off)
    """

    def __init__(self, parent, row_factory, group_label=None, group_tooltip=None,
                 add_button_text="add", remove_last_button_text="Remove Last",
                 remove_all_button_text="Remove All",
                 add_tooltip=None, remove_last_tooltip=None, remove_all_tooltip=None,
                 bg="#e0e0e0", fg="black", start_enabled=True,
                 row_spacing=1, enable_scrolling=False, max_height_fraction=0.2):
        """
        :param parent: The parent widget this group's frame will be placed in.
        :param row_factory: A function that takes one argument (the parent frame
                             to build the row inside) and returns a new row object.
                             Called once every time "add" is clicked.
        :param group_label: Optional header text shown above the row list.
        :param group_tooltip: Optional tooltip text attached to the header label.
        :param add_button_text: Text for the "add" button.
        :param remove_last_button_text: Text for the "remove last" button.
        :param remove_all_button_text: Text for the "remove all" button.
        :param add_tooltip: Optional tooltip text for the "add" button.
        :param remove_last_tooltip: Optional tooltip text for the "remove last" button.
        :param remove_all_tooltip: Optional tooltip text for the "remove all" button.
        :param bg: Background color used for the frame and labels.
        :param fg: Text color used for the header label.
        :param start_enabled: Whether the three buttons start out clickable (True)
                               or greyed out (False).
        :param row_spacing: Vertical gap, in pixels, placed between rows in the list.
        :param enable_scrolling: If True, the row list is wrapped in a scrollable
                                  area capped at max_height_fraction of the screen's
                                  height, with a scrollbar that appears once the rows
                                  grow taller than that. Requires
                                  ScreenSizeManager.initialize() to already have been
                                  called (done once, in TheorChem2Blender.py).
        :param max_height_fraction: Fraction (0-1) of the screen's height used as the
                                     scrollable area's maximum height. Only used when
                                     enable_scrolling is True.
        """
        self.row_factory = row_factory
        self.rows = []
        self.row_spacing = row_spacing
        self.enable_scrolling = enable_scrolling

        self.frame = tk.Frame(master=parent, bg=bg)

        current_row = 0

        if group_label:
            self.group_label_widget = tk.Label(master=self.frame, text=group_label, bg=bg, fg=fg)
            self.group_label_widget.grid(row=current_row, column=0, sticky="w")
            if group_tooltip:
                CreateTooltip(self.group_label_widget, group_tooltip)
            current_row += 1

        if self.enable_scrolling:
            current_row = self._setup_scrollable_rows_container(current_row, bg, max_height_fraction)
        else:
            # Rows get added here, one on top of the other, as they're created.
            self.rows_container = tk.Frame(master=self.frame, bg=bg)
            self.rows_container.grid(row=current_row, column=0, sticky="w", pady=(2, 2))
            current_row += 1

        self.buttons_frame = tk.Frame(master=self.frame, bg=bg)
        self.buttons_frame.grid(row=current_row, column=0, sticky="w")

        initial_state = tk.NORMAL if start_enabled else tk.DISABLED

        self.btn_add = tk.Button(master=self.buttons_frame, text=add_button_text,
                                  command=self.add_row, state=initial_state)
        self.btn_add.grid(row=0, column=0, padx=(0, 4))
        if add_tooltip:
            CreateTooltip(self.btn_add, add_tooltip)

        self.btn_remove_last = tk.Button(master=self.buttons_frame, text=remove_last_button_text,
                                          command=self.remove_last, state=initial_state)
        self.btn_remove_last.grid(row=0, column=1, padx=(0, 4))
        if remove_last_tooltip:
            CreateTooltip(self.btn_remove_last, remove_last_tooltip)

        self.btn_remove_all = tk.Button(master=self.buttons_frame, text=remove_all_button_text,
                                         command=self.remove_all, state=initial_state)
        self.btn_remove_all.grid(row=0, column=2)
        if remove_all_tooltip:
            CreateTooltip(self.btn_remove_all, remove_all_tooltip)

    def _setup_scrollable_rows_container(self, current_row, bg, max_height_fraction):
        """
        Builds rows_container inside a scrollable canvas instead of placing it
        directly in self.frame. The canvas grows with its contents up to
        max_height_fraction of the screen's height, then a scrollbar takes
        over. Mirrors the canvas+scrollbar pattern already used elsewhere in
        this app (see InputRegion.py / IonRegion.py).

        Returns the next free grid row in self.frame, for the buttons below it.
        """
        self.max_scroll_height = int(ScreenSizeManager.get_screen_height() * max_height_fraction)

        self.canvas = tk.Canvas(master=self.frame, bg=bg, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(master=self.frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.rows_container = tk.Frame(master=self.canvas, bg=bg)
        self.canvas.create_window((0, 0), window=self.rows_container, anchor="nw")
        self.rows_container.bind("<Configure>", self._update_scroll_region)

        self.canvas.grid(row=current_row, column=0, sticky="w", pady=(2, 2))
        self.scrollbar.grid(row=current_row, column=1, sticky="ns", pady=(2, 2))
        return current_row + 1

    def _update_scroll_region(self, event=None):
        """
        Resizes the scrollable canvas to fit its current contents, up to the
        height cap computed in _setup_scrollable_rows_container(). Runs
        automatically every time a row is added or removed, since that
        changes the size of rows_container and triggers its <Configure> event.
        """
        bbox = self.canvas.bbox("all")
        if bbox is None:
            return
        content_width = bbox[2] - bbox[0]
        content_height = bbox[3] - bbox[1]
        display_height = min(content_height, self.max_scroll_height)
        self.canvas.configure(scrollregion=bbox, width=content_width, height=display_height)

    def add_row(self):
        """Builds one new row via row_factory and adds it to the bottom of the list."""
        new_row = self.row_factory(self.rows_container)
        new_row.frame.grid(row=len(self.rows), column=0, sticky="w", pady=self.row_spacing)
        self.rows.append(new_row)
        return new_row

    def remove_last(self):
        """Removes the most recently added row, if any."""
        if not self.rows:
            return
        row = self.rows.pop()
        row.destroy()
        self.frame.update_idletasks()

    def remove_all(self):
        """Removes every row, resetting this group back to empty."""
        for row in self.rows:
            row.destroy()
        self.rows.clear()
        self.frame.update_idletasks()

    def set_enabled(self, enabled):
        """
        Enables or disables the add/remove buttons. Does not touch existing rows -
        call remove_all() separately if the rows themselves should also be cleared.
        """
        state = tk.NORMAL if enabled else tk.DISABLED
        self.btn_add.config(state=state)
        self.btn_remove_last.config(state=state)
        self.btn_remove_all.config(state=state)

    def get_row_values(self):
        """Returns a list built from calling .get_values() on every current row, in order."""
        return [row.get_values() for row in self.rows]
