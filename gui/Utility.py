import sys
import os

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