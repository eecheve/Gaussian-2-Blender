import os
import sys
import time
import psutil
import tkinter as tk
from functools import wraps

class Utility(object):
    """Utility class holding functions used by several classes"""
    @staticmethod
    def benchmark(func):
        """
        Decorator to measure and print the execution time and memory usage of a function.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            process = psutil.Process(os.getpid())
            start_time = time.time()
            start_mem = process.memory_info().rss / (1024 ** 2)  # MB

            result = func(*args, **kwargs)

            end_time = time.time()
            end_mem = process.memory_info().rss / (1024 ** 2)
            memory_used = end_mem - start_mem
            elapsed_time = end_time - start_time

            print(f"Function '{func.__name__}' completed in {elapsed_time:.2f} seconds")
            print(f"Approximate memory used: {memory_used:.2f} MB")

            return result
        return wrapper

    
    def findFile(name, path):
        """
        returns true if there is a file with name <name> in <path>
        """
        for root, dirs, files in os.walk(path):
            if name in files:
                return True
            else:
                return False
        return False

    def resource_path(relative_path):
        """
        This allows using resources from global paths
        """
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    def clear_file_contents(file_name):
        with open(file_name, 'w') as f:
            f.close()

    def append_lines_to_file(file_name, lines):
        with open(file_name, 'w') as f:
            for line in lines:
                f.writelines(line + '\n')

    def append_lines_to_file(file_name, lines):
        with open(file_name, 'w') as f:
            for line in lines:
                # Convert boolean to string if line is boolean
                if isinstance(line, bool):
                    line = "1" if line else "0" #makes the line 1 if line is True, 0 otherwise
                f.writelines(line + '\n')

    def customize_widget(tk_object, color_string):  
        """Set the background color of the widget"""
        tk_object.config(bg=color_string)

    def set_bg_color(widget, bg_color):
        """
        Recursively set the bg color for a widget and all its children

        :param widget: The parent widget
        :param bg_color: the bg color to set
        """
        try:
            widget.configure(bg=bg_color)
        except tk.TclError:
            pass
        for child in widget.winfo_children():
            try:
                child.configure(bg=bg_color)
            except tk.TclError:
                pass

    def revert_widget(tk_object):
        """
        Reverts a widget's appearance (background color) to its default state.
        """
        # Define the original colors for supported widget types
        original_colors = {
            "Checkbutton": "#f0f0f0",
            "Menubutton": "#f0f0f0",
            "Button": "#f0f0f0"
        }

        # Identify the widget's class type
        widget_type = tk_object.winfo_class()

        # Revert the background color for the main widget
        if widget_type in original_colors:
            tk_object.config(bg=original_colors[widget_type],
                             fg='black')