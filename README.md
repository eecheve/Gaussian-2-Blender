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
- Click on this [YouTube link](https://youtu.be/w_bsJ7daaas) for a tutorial on using the tool. NOTE: YouTube tutorial does not include information on animations.

## INSTRUCTIONS:
1. Double-click on the `Gaussian-Blender-Bridge.exe` file.
2. Select one or more `.com` or `.xyz` files from the same folder.
3. To render using ionic radii, select the `Check for Ionic Radii` option.
4. Add each ion and select their charge, coordination, and spin multiplicity (when available).
5. Select `Is Animation` if the series of input selected are all different frames of the same dynamic process
6. If you plan to render an animation, make sure all the `.com` or `.xyz` files have the same atoms in the same order
7. Click on `Convert!` to convert the `.com` input into the desired output type.
8. Click on `Reset` to reset everything to their default values.

## EXAMPLE FILES:
- Example `.com` files are inside the `input_examples` folder, separated by categories.
- For example, the file `Ice.com` is located in the `input_examples\inorganic\` folder.
- The `output` folder starts empty and is the default location for 3D renderings from the tool.

## FOR DEVELOPERS

### RUNNING FROM THE CONSOLE:
To run the `Gaussian-2-Blender.py` Python script from the console:
1. Copy the `Gaussian-2-Blender.py` file to the `gui` folder.
2. Open a terminal in the `Blender-Gaussian-Bridge/` folder and run:
   ```bash
   python Gaussian-2-Blender.py
    ```

### DOCUMENTATION:
A Microsoft Word file called `Gaussian-2-Blender documentation.docx` can be found in the `docs/` folder.

### GUI OVERVIEW:
The `GaussianToBlender.py` application provides a graphical user interface (GUI) for converting Gaussian input files into 3D object files using Blender's API. The main script, utilizing `tkinter`, manages different regions and functionalities, including input, output, console, and ion management.

#### Key GUI Modules:
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

### FILE STRUCTURE:
For users interested in extending the functionality of the program. This project is organized into several directories and files. Please follow this [link](https://gaussian-2-blender.readthedocs.io/en/latest/index.html) to read the latest documentation for the program.


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
