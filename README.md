# TheorChem-2-Blender

TheorChem-2-Blender is a tool that allows users to convert a various computational chemistry input filse into 3D objects for modeling, 3D printing, animations, and other 3D applications.

## PREREQUISITES:
- Install Blender on your machine. Link: https://www.blender.org/download/
- Install the latest version of Python. Link: https://www.python.org/downloads/
- No programming knowledge is required to use this tool.

## SETUP:
- If you install Blender in a non-default path on Windows, note the path as it will be needed.
- Download the entire 'TheorChem-2-Blender' package and unzip it to the desired location.
- If you have a Windows machine, the executable `TheorChem2Blender.exe` will be ready to use. Do not move, rename, or delete any files or folders included in the package.
- Click on this [Documentation link](https://gaussian-2-blender.readthedocs.io/en/latest/index.html) for more information about the tool, its functions, and how to use it.

## INSTRUCTIONS (IF WINDOWS):
1. Double-click on the `TheorChem2Blender.exe` file.
2. The executable has various tabs: `Input`, `Customization`, `Ions`, `Output`, and `Convert!` 
2. Each tab has a `Help` button on its top right part of the screen. Click on the button to know how to use the tab.
3. (NOTE) If you plan to render an animation, make sure all the `.com` or `.xyz` files have the same atoms in the same order
7. Click on `Convert!` to convert the input into the desired output type.
8. Click on `Reset` to reset everything to their default values.

## INSTRUCTIONS (IF NOT WINDOWS)
1. Open a terminal in the `Blender-Gaussian-Bridge/` folder and run:
   ```bash
   python3 TheorChem2Blender.py
    ```
2. The rest of steps are the same as if you would have a windows machine.

## EXAMPLE FILES:
- There are `.com`, `.xyz`, and `.mol2` input files availables inside the `input_examples` folder. 
- For example, the file `Ice.com` is located in the `input_examples\com_files\inorganic\` folder.
- The `output` folder starts empty and is the default location for 3D renderings from the tool.

## FOR DEVELOPERS

### DOCUMENTATION:
- This [link](https://gaussian-2-blender.readthedocs.io/en/latest/index.html) contains a searchable directory for the must up-to-date documentation.

### GUI OVERVIEW:
The `TheorChem2Blender.py` application provides a graphical user interface (GUI) for converting Gaussian input files into 3D object files using Blender's API. The main script, utilizing `tkinter`, manages different regions and functionalities, including input, output, console, and ion management.

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
