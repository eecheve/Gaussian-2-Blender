# Gaussian-2-Blender

Gaussian-2-Blender is a tool that allows users to convert a Gaussian input file into a 3D object for modeling, 3D printing, animations and other 3D applications.

## PREREQUISITES:
- Install Blender in your machine. Link: https://www.blender.org/download/
- Install the latest version of Python. Link: https://www.python.org/downloads/
- No programming-knowledge required to use this tool.

## SETUP:
- If you install Blender on a path which is not the Windows default, take note of the path as it will be needed.
- Download the whole 'Gaussian-2-Blender' package and unzip to its desired location.
- The executable `Gaussian-2-Blender.exe` will be ready to use. Do not move, rename nor delete any files or folders that come with the package.
- Click on this [YouTube link](https://youtu.be/w_bsJ7daaas) for a tutorial on how to use the tool.

## EXAMPLE FILES:
- The example .com files are inside the `input_examples` folder, separated by categories.
- For example: the file `Ice.com` is located in `input_examples\inorganic\` folder
- The `output` folder begins empty. Is the default location for the 3D rendering of the tool. 

## INSTRUCTIONS:
- Double-click on the `Gaussian-Blender-Bridge.exe` file.
- Select one or more '.com' files from the same folder.
- The default rendering radii are covalent. For rendering ionic radii select the `Check for Ionic Radii` option.
- Add each ion and select their charge, coordination and spin multiplicity (when available).
- Click on 'Convert!' to convert the .com input into de desired output type.
- Click on 'Reset' to reset everything to their default values.

## RUNNING FROM THE CONSOLE
If desired, you can run the `Gaussian-2-Blender.py` python script from the console.
- Copy the Gaussian-2-Blender.py file in the gui folder
- Open a terminal in the `Blender-Gaussian-Bridge/gui/` folder and type the next command:
```bash
python Gaussian-2-Blender.py
```

###Copyright 2021 Emmanuel Echeverri

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
