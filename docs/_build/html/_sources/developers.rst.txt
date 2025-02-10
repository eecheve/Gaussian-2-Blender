For Developers
==============

GUI overview:
-------------
The ``GaussianToBlender.py`` application provides a graphical user interface (GUI) for converting Gaussian input files into 3D object files using Blender's API. The main script, utilizing ``tkinter``, manages different regions and functionalities, including input, output, console, and ion management.

Key GUI Modules:
----------------
- ``Information.py``: Manages help and about sections, providing instructions and application details.
- ``BlenderPath.py``: Allows users to set the path to the Blender executable.
- ``InputRegion.py``: Handles input file selection and management.
- ``OutputRegion.py``: Manages output paths and file types.
- ``ConsoleRegion.py``: Displays console output and error messages.
- ``IonRegion.py``: Manages ion information for the molecules.
- ``IonConventions.py``: Displays ion coordination codes and their meanings.
- ``ActionsRegion.py``: Provides buttons for resetting values and initiating conversions.
- ``Utility.py``: Contains utility functions for file management.
- ``Coordinates.py``: Extracts Cartesian coordinates from molecular structure files.
- ``TextRedirector.py``: Redirects print statements to the console region within the GUI.

File structure
==============
For users interested in extending the functionality of the program. This project is organized into several directories and files as follows:

GaussianToBlender/
------------------
- ``LICENSE.txt``: License file
- ``README.md``: Project documentation in README form
- ``GaussianToBlender.exe``: Executable file created from GaussianToBlender.py
- ``GaussianToBlender.py``: Python script for converting Gaussian data to Blender models (with tkinter GUI)

gui/
---- 
Folder containing GUI-related scripts

- ``__init__.py``: Optional init file for the gui package
- ``Information.py``: Manages help and about sections, provides instructions and application details
- ``BlenderPath.py``: Allows users to set the path to the Blender executable
- ``InputRegion.py``: Handles input file selection and management
- ``OutputRegion.py``: Manages output paths and file types
- ``ConsoleRegion.py``: Displays console output and error messages
- ``IonRegion.py``: Manages ion information for the molecules
- ``IonConventions.py``: Displays ion coordination codes and their meanings
- ``ActionsRegion.py``: Provides buttons for resetting values and initiating conversions
- ``Utility.py``: Contains utility functions for file management
- ``Coordinates.py``: Extracts Cartesian coordinates from molecular structure files
- ``TextRedirector.py``: Redirects print statements to the console region within the GUI
- ... (Other GUI-related files)

scripts/
--------
Folder containing Blender API related scripts and modules

- ``__init__.py``: Optional init file for the scripts package
- ``Main_Body.py``: Main script that orchestrates the molecular data conversion process
- ``AtomData.py``: Stores atomic and ionic data (e.g., radii, colors)
- ``ImportData.py``: Extracts and filters molecular data from input files
- ``RefineData.py``: Refines molecular coordinates and connectivity data
- ``RefineElements.py``: Identifies unique elements, positions, and connectivity
- ``Create_Materials.py``: Manages materials for molecular elements in Blender
- ``Primitives.py``: Instantiates and manages 3D primitives for atoms and bonds
- ``Export_Data.py``: Exports Blender scenes and animations
- ``Ions.py``: Handles ionic data within molecular structures
- ``Instantiate_Molecules.py``: Instantiates 3D geometries from Cartesian coordinates
- ``Raw_Parameters.py``: Extracts and processes raw coordinates/connectivity
- ``Animate.py``: Manages animation of molecular structures
- ``Clear_Transforms.py``: Applies transformations to bonds and elements
- ``Receive_Parameters.py``: Extracts and processes parameter data into a dictionary
- ... (Other Blender-related scripts)

input_examples/
---------------
Folder containing example input files

- ``com_files/example1.com``: Example input file 1 (e.g., Gaussian .com format)
- ``xyz_files/example2.xyz``: Example input file 2 (e.g., xyz format)

output/
-------
Default folder for exporting molecules and animation results

- folder starts empty
