class ScreenSizeManager(object):
    """
    Reads the screen's width and height once, right when the app starts,
    and makes those values available anywhere in the app afterward. Also
    the single place where every window-size-related tuning constant
    lives, so they're easy to find and adjust later.

    Why this exists: several regions (like UnitCellRegion's scrollable
    growth list) need to know how big the screen is, but re-querying
    Tkinter for it in every widget is wasteful and easy to get wrong
    before the window is fully drawn. Instead, TheorChem2Blender.py calls
    initialize(root) exactly once, right after creating the root window,
    and every other module can just import this class and call its
    getters - no need to pass screen size through constructors.

    Usage:
        # once, in TheorChem2Blender.py, right after self.root = tk.Tk()
        ScreenSizeManager.initialize(self.root)
        self.root.minsize(ScreenSizeManager.MIN_WIDTH, ScreenSizeManager.MIN_HEIGHT)

        # anywhere else in the app
        from gui.ScreenSizeManager import ScreenSizeManager
        max_height = ScreenSizeManager.get_screen_height() * 0.2
    """

    # The window is never allowed to shrink smaller than this, no matter
    # how far the user drags its edges.
    MIN_WIDTH = 800
    MIN_HEIGHT = 600

    # Every tab is organized into three stacked containers: instructions
    # (About/Help), the tab's main content, and the shared console at the
    # bottom. These weights control how the vertical space is split
    # between them, and are set up so they read directly as percentages
    # of the whole window (they add up to 100). See ProportionalContainer
    # for how a container turns one of these weights into an actual
    # on-screen size.
    INFO_HEIGHT_WEIGHT = 4        # instructions container: ~5% of window height
    CONTENT_HEIGHT_WEIGHT = 71    # tab's main content container: ~70% of window height
    CONSOLE_HEIGHT_WEIGHT = 25    # console container: the remaining ~25%

    _screen_width = None
    _screen_height = None

    @classmethod
    def initialize(cls, root):
        """
        Reads and caches the screen's width and height, in pixels.

        Must be called once, before any code calls get_screen_width() or
        get_screen_height(). Safe to call again later (e.g. if the app
        ever needs to support moving between monitors), which simply
        refreshes the cached values.

        :param root: The Tk root window, used only to query the screen size.
        """
        cls._screen_width = root.winfo_screenwidth()
        cls._screen_height = root.winfo_screenheight()

    @classmethod
    def get_screen_width(cls):
        """Returns the cached screen width, in pixels."""
        if cls._screen_width is None:
            raise RuntimeError("ScreenSizeManager.initialize(root) must be called before get_screen_width().")
        return cls._screen_width

    @classmethod
    def get_screen_height(cls):
        """Returns the cached screen height, in pixels."""
        if cls._screen_height is None:
            raise RuntimeError("ScreenSizeManager.initialize(root) must be called before get_screen_height().")
        return cls._screen_height
