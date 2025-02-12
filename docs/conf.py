# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
from pathlib import Path
from unittest.mock import MagicMock #to avoid importing bpy

#------------------------------------------------------------------------------------
# Mock modules to avoid sphinx from crashing due to it not recognizing bpy
class BpyMock(MagicMock):
    @classmethod
    def __getattr__(cls, name):
        """
        Mock module for the bpy that scaffolds the Blender Python API. This file will grow.
        """
        if name == "data":
                return MagicMock(filepath="C:/Documents/Gaussian-2-Blender/dummy.blend")  # Return valid path
        return MagicMock()

MOCK_MODULES = ['bpy', 'bpy.types', 'bpy.props', 'bpy.utils', 'bpy.data', 'mathutils']
sys.modules.update((mod_name, BpyMock()) for mod_name in MOCK_MODULES)
#-------------------------------------------------------------------------------------

# Get the absolute path of the project root
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add paths to sys.path
sys.path.insert(0, root_dir)          # root/
sys.path.insert(0, os.path.join(root_dir, "scripts"))  # root/scripts
sys.path.insert(0, os.path.join(root_dir, "gui"))      # root/gui

project = 'Gaussian-2-Blender'
copyright = '2025, Emmanuel Echeverri-Jimenez'
author = 'Emmanuel Echeverri-Jimenez'
release = '2025.2'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.duration', # Shows expected read time
    'sphinx.ext.doctest', #to create doctests
    'sphinx.ext.autodoc',    # Automatically generate documentation from docstrings
    'sphinx.ext.napoleon',    # Support for Google-style and NumPy-style docstrings
    'sphinx.ext.viewcode',    # Adds links to source code in documentation
    'sphinx.ext.autosummary', #To make automatic summaries for each function
    'sphinx.ext.graphviz', #to make connections between modules and scripts
    'sphinx.ext.inheritance_diagram', #to build an inheritance diagram
    ]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
autosummary_generate = True
graphviz_output_format = 'svg'
graphviz_dot = 'C:/Program Files/Graphviz/bin/dot.exe'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
