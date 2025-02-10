# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
from pathlib import Path

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
    ]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
autosummary_generate = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
html_css_files = [
    'style.css',
]
