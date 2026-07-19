import tkinter as tk


class ProportionalContainer(object):
    """
    A container that always spans the full available width of its parent,
    and a height controlled entirely by a grid row weight - so it keeps
    the right proportions automatically whenever the window is resized,
    with no manual recalculating needed.

    This is the building block behind "every tab has three containers":
    an instructions container, a content container, and (shared across
    every tab, built separately - see ConsoleRegion) the console
    container. Each tab wraps its Information widget and its main region
    widget in one of these.

    Usage:
        container = ProportionalContainer(
            parent=self.unit_cell_tab, row=1,
            weight=ScreenSizeManager.CONTENT_HEIGHT_WEIGHT, enable_scrolling=True
        )
        self.unit_cell_region = UnitCellRegion(container.content_frame)

    The weight isn't a percentage by itself - it's relative to the
    weights given to whatever else shares the same parent's rows. See
    ScreenSizeManager for the actual weight constants used across the
    app (INFO_HEIGHT_WEIGHT, CONTENT_HEIGHT_WEIGHT, CONSOLE_HEIGHT_WEIGHT),
    chosen so they add up to 100 and read directly as percentages.
    """

    def __init__(self, parent, row, weight, enable_scrolling=False, bg="#e0e0e0"):
        """
        :param parent: The parent widget this container will be placed in.
                        Must have grid_columnconfigure(0, weight=1) set on it
                        (once, by whoever owns that parent) so this container
                        can actually stretch to full width.
        :param row: Which row of the parent's grid this container occupies.
        :param weight: This row's grid weight, relative to its sibling rows.
        :param enable_scrolling: If True, wraps the content area in a
                                  canvas + scrollbar, so content taller than
                                  the space available scrolls instead of
                                  getting clipped or forcing the window to grow.
                                  Leave off for small, fixed-size content
                                  (like the instructions container's buttons).
        :param bg: Background color.
        """
        parent.grid_rowconfigure(row, weight=weight)

        self.frame = tk.Frame(master=parent, bg=bg)
        self.frame.grid(row=row, column=0, sticky="nsew")
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        if enable_scrolling:
            self._setup_scrollable_content(bg)
        else:
            # content_frame is where the real widget (Information, a region, etc.)
            # gets built. Without scrolling, it's just a plain frame that fills
            # this container directly.
            self.content_frame = tk.Frame(master=self.frame, bg=bg)
            self.content_frame.grid(row=0, column=0, sticky="nsew")
            # Default to a single stretchy column, matching the scrollable branch,
            # so content spans full width without every caller having to set this
            # up themselves. A tab that needs a different column layout (e.g. the
            # Actions tab's bottom-right-anchored button area) can still add more
            # column/row configuration on top of this afterward.
            self.content_frame.grid_columnconfigure(0, weight=1)

    def _setup_scrollable_content(self, bg):
        """
        Wraps content_frame in a canvas + scrollbar, so whatever gets built
        inside it can grow taller than the container without being cut off -
        a scrollbar appears instead. The same pattern already used in
        InputRegion.py, IonRegion.py, and RepeatableRowGroup.py.
        """
        self.canvas = tk.Canvas(master=self.frame, bg=bg, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(master=self.frame, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.content_frame = tk.Frame(master=self.canvas, bg=bg)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

        # Whenever the content grows or shrinks, tell the canvas how much
        # there now is to scroll through.
        self.content_frame.bind("<Configure>", self._update_scroll_region)
        # Whenever the visible canvas area is resized (e.g. the window grows),
        # keep the content exactly as wide as that visible area.
        self.canvas.bind("<Configure>", self._sync_content_width)

    def _update_scroll_region(self, event=None):
        """Keeps the scrollable area matched to the content's actual size."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _sync_content_width(self, event):
        """Keeps the inner content frame exactly as wide as the visible canvas."""
        self.canvas.itemconfig(self.canvas_window, width=event.width)
