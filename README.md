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

## EXAMPLE FILES:
- The example .com files are inside the `input_examples` folder, separated by categories.
- For example: the file `Ice.com` is located in `input_examples\inorganic\` folder
- The `output` folder begins empty. Is the default location for the 3D rendering of the tool. 

## INSTRUCTIONS:
- Double-click on the `Gaussian-Blender-Bridge.exe` file.
- Default values are already placed in both 'input path' and 'output path'
- There are two alternatives to replace the default values: either (a) Set the folder paths by clicking on the 'set' button and selecting the adequate paths, or (b) Copy and paste the folder paths to the text box next to the label.
- Either write or set the input file name. Don't forget the '.com' extension
- Either write or set the output file name. Setting it will replace the file.
- Click on 'Convert!' to convert the .com input into de desired output type.
- Click on 'Reset' to reset everything to their default values.

## RUNNING FROM THE CONSOLE
If desired, you can run the `Gaussian-2-Blender.py` python script from the console.
Open a terminal in the `Blender-Gaussian-Bridge/` folder and type the next command:
```bash
python Gaussian-2-Blender.py
```
