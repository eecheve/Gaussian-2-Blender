import sys
import os
import tkinter as tk

class Utility(object):
    """Utility class holding functions used by several classes"""
    
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
        # Set the background color of the widget
        tk_object.config(bg=color_string)

    # def revert_widget(tk_object):
    #     original_colors = { #at the moment is the same color, but will store it differently for the future
    #         "Checkbutton": "#f0f0f0",
    #         "OptionMenu": "#f0f0f0",
    #         "Button": "#f0f0f0"
    #     }
        
    #     widget_type = tk_object.winfo_class() # Check the type of the tkinter object

    #     if widget_type in original_colors:
    #         tk_object.config(bg=original_colors[widget_type])
        
    #     if tk_object in original_colors: # Revert the background color to the original value
    #         tk_object.config(bg=original_colors[tk_object])
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
            tk_object.config(bg=original_colors[widget_type])