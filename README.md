# Gaussian-2-Blender

Gaussian-2-Blender is a tool that allows users to convert a Gaussian input file into a 3D object for modeling, 3D printing, animations, and other 3D applications.

## PREREQUISITES:
- Install Blender on your machine. Link: https://www.blender.org/download/
- Install the latest version of Python. Link: https://www.python.org/downloads/
- No programming knowledge is required to use this tool.

## SETUP:
- If you install Blender in a non-default path on Windows, note the path as it will be needed.
- Download the entire 'Gaussian-2-Blender' package and unzip it to the desired location.
- The executable `Gaussian-2-Blender.exe` will be ready to use. Do not move, rename, or delete any files or folders included in the package.
- Click on this [YouTube link](https://youtu.be/w_bsJ7daaas) for a tutorial on using the tool.

## GUI OVERVIEW:
The `GaussianToBlender.py` application provides a graphical user interface (GUI) for converting Gaussian input files into 3D object files using Blender's API. The main script, utilizing `tkinter`, manages different regions and functionalities, including input, output, console, and ion management.

### Key GUI Modules:
- `Information.py`: Manages help and about sections, providing instructions and application details.
- `BlenderPath.py`: Allows users to set the path to the Blender executable.
- `InputRegion.py`: Handles input file selection and management.
- `OutputRegion.py`: Manages output paths and file types.
- `ConsoleRegion.py`: Displays console output and error messages.
- `IonRegion.py`: Manages ion information for the molecules.
- `IonConventions.py`: Displays ion coordination codes and their meanings.
- `ActionsRegion.py`: Provides buttons for resetting values and initiating conversions.
- `Utility.py`: Contains utility functions for file management.
- `Coordinates.py`: Extracts Cartesian coordinates from molecular structure files.
- `TextRedirector.py`: Redirects print statements to the console region within the GUI.

## EXAMPLE FILES:
- Example `.com` files are inside the `input_examples` folder, separated by categories.
- For example, the file `Ice.com` is located in the `input_examples\inorganic\` folder.
- The `output` folder starts empty and is the default location for 3D renderings from the tool.

## INSTRUCTIONS:
1. Double-click on the `Gaussian-Blender-Bridge.exe` file.
2. Select one or more `.com` files from the same folder.
3. To render using ionic radii, select the `Check for Ionic Radii` option.
4. Add each ion and select their charge, coordination, and spin multiplicity (when available).
5. Select `Is Animation` if the series of input selected are all different frames of the same dynamic process
5. Click on `Convert!` to convert the `.com` input into the desired output type.
6. Click on `Reset` to reset everything to their default values.

## RUNNING FROM THE CONSOLE:
To run the `Gaussian-2-Blender.py` Python script from the console:
1. Copy the `Gaussian-2-Blender.py` file to the `gui` folder.
2. Open a terminal in the `Blender-Gaussian-Bridge/` folder and run:
   ```bash
   python Gaussian-2-Blender.py
    ```

## FILE STRUCTURE:
For users interested in extending the functionality of the program. This project is organized into several directories and files as follows:

GaussianToBlender/
Gaussian-2-Blender/
- LICENSE.txt: License file
- README.md: Project documentation
- GaussianToBlender.exe: Executable file created from GaussianToBlender.py
- GaussianToBlender.py: Python script for converting Gaussian data to Blender models (with tkinter GUI)

- gui/: Folder containing GUI-related scripts
  - __init__.py: Optional init file for the gui package
  - Information.py: Manages help and about sections, provides instructions and application details
  - BlenderPath.py: Allows users to set the path to the Blender executable
  - InputRegion.py: Handles input file selection and management
  - OutputRegion.py: Manages output paths and file types
  - ConsoleRegion.py: Displays console output and error messages
  - IonRegion.py: Manages ion information for the molecules
  - IonConventions.py: Displays ion coordination codes and their meanings
  - ActionsRegion.py: Provides buttons for resetting values and initiating conversions
  - Utility.py: Contains utility functions for file management
  - Coordinates.py: Extracts Cartesian coordinates from molecular structure files
  - TextRedirector.py: Redirects print statements to the console region within the GUI
  - ... (Other GUI-related files)

- scripts/: Folder containing Blender API related scripts and modules
  - __init__.py: Optional init file for the scripts package
  - Main_Body.py: Main script that orchestrates the molecular data conversion process
  - AtomData.py: Stores atomic and ionic data (e.g., radii, colors)
  - ImportData.py: Extracts and filters molecular data from input files
  - RefineData.py: Refines molecular coordinates and connectivity data
  - RefineElements.py: Identifies unique elements, positions, and connectivity
  - Create_Materials.py: Manages materials for molecular elements in Blender
  - Primitives.py: Instantiates and manages 3D primitives for atoms and bonds
  - Export_Data.py: Exports Blender scenes and animations
  - Ions.py: Handles ionic data within molecular structures
  - Instantiate_Molecules.py: Instantiates 3D geometries from Cartesian coordinates
  - Raw_Parameters.py: Extracts and processes raw coordinates/connectivity
  - Animate.py: Manages animation of molecular structures
  - Clear_Transforms.py: Applies transformations to bonds and elements
  - Receive_Parameters.py: Extracts and processes parameter data into a dictionary
  - ... (Other Blender-related scripts)

- input_examples/: Folder containing example input files
  - example1.com: Example input file 1 (e.g., Gaussian .com format)
  - example2.xyz: Example input file 2 (e.g., XYZ format)
  - ... (Other example files)

- output/: Folder for exporting molecules and animation results
  - molecule1.fbx: Exported molecule file 1 (e.g., .fbx format)
  - animation1.mp4: Exported animation file 1 (e.g., .mp4 format)
  - ... (Other exported files)


## TECHNICAL REPORT PUBLICATION
Follow this [link](https://doi.org/10.1021/acs.jchemed.1c00515) from the `Journal of Chemical Education` to access the technical report for this project. 
    

### Copyright 2021 Emmanuel Echeverri

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
