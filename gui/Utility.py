import os
import sys
import time
import psutil
import tkinter as tk
from functools import wraps
from inspect import signature

class Utility(object):
    """Utility class holding functions used by several classes"""
    @staticmethod
    def redirect_print_to_log(logfile='output.log', mode='a'):
        """
        A decorator that redirects all print() statements within a function
        to a specified log file.
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                original_stdout = sys.stdout  # Save current stdout
                with open(logfile, mode) as f:
                    sys.stdout = f  # Redirect prints
                    try:
                        result = func(*args, **kwargs)
                    finally:
                        sys.stdout = original_stdout  # Restore stdout
                return result
            return wrapper
        return decorator

    @staticmethod
    def measure_memory(func):
        """
        Decorator to measure ant print the memory usage of a function
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            process = psutil.Process(os.getpid())
            start_mem = process.memory_info().rss / (1024 ** 2)  # MB before
            result = func(*args, **kwargs)
            end_mem = process.memory_info().rss / (1024 ** 2)    # MB after
            memory_used = end_mem - start_mem
            print(f"Approximate memory used: {memory_used:.2f} MB")
            return result
        return wrapper
    
    @staticmethod
    def time_function(func):
        """
        Decorator to measure and print the execution time usage of a function.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f"Function '{func.__name__}' completed in {elapsed_time:.2f} seconds")
            return result
        return wrapper
    
    @staticmethod
    def announce_conversion(func):
        """
        Decorator to print which molecule or file is currently being converted.
        It assumes the wrapped function has a parameter named 'i_name'.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Try to extract 'i_name' from either kwargs or positional args
            sig = signature(func)
            bound = sig.bind_partial(*args, **kwargs)
            bound.apply_defaults()
            i_name = bound.arguments.get("i_name", None)

            if i_name is not None:
                print(f"Currently converting {i_name}...")
            else:
                print("Currently converting: (unknown input)")

            return func(*args, **kwargs)
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