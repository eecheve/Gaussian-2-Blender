# gui/Instructions.py

class Instructions:
    instructions = {
        "input": [
            ("Input \n", "bold"),
            ("1. The path to the Blender executable should be found in the default folder location.\n", "normal"),
            ("    1.1. If not found: Set the path to the Blender executable by navigating to the Blender installation directory.\n","italic"),
            ("2. Select the input file(s) that you want to convert.\n", "normal"),
            ("    2.1. The input can be either '.com', '.xyz', or '.mol2'.\n", "italic"),
            ("    2.2. If you select '.com', make sure the file includes connectivity after the atom coordinates\n", "italic"),
            ("    2.3. If you select '.xyz' or '.mol2', bonds will be rendered based on average covalent bond lengths\n", "italic"),
            ("    2.4. You can select more than one input file at a time, but all with the same extension\n", "italic"),
            ("3. If you select the 'is animation' box, make sure to follow these rules:\n", "normal"),
            ("    3.1. If the input is '.com':\n", "italic"),
            ("        3.1.1. In the 'input file(s)' section, select two or more '.com' files\n", "italic"),
            ("        3.1.2. All the input files must share the same atom identity, order and connectivity\n", "italic"),
            ("    3.2. If the input is '.xyz'\n", "italic"),
            ("        3.2.1. All the cartesian coordinates must be located in the same 'xyz' file\n", "italic"),
            ("        3.2.2. Make sure there is always the same number, identity, and order of atoms\n", "italic"),
            ("    3.3. At the moment, there is no animation possible with '.mol2' files.\n", "italic")
        ],
        "customization": [
            ("Customization \n", "bold"),
            ("4. Specify any bonds you would like to overwrite from the initial input file.\n", "normal"),
            ("    4.1. These are the characters that represent different bond orders\n", "italic"),
            ("        4.1.1. Bond order 0.5: '_'\n", "italic"),
            ("        4.1.2. Bond order 1: '-'\n", "italic"),
            ("        4.1.3. Bond order 1.5: '%'\n", "italic"),
            ("        4.1.4. Bond order 2: '='\n", "italic"),
            ("        4.1.5. Bond order 3: '#'\n", "italic"),
            ("    4.2. Type the bonds separated by semicolons like the example below:\n", "normal"),
            ("         C01-C02; C03=O04; O04_H27; H27_N09\n", "code"),
            ("5. Identify any atoms and/or bonds that you would like to highlight in the final 3D model.\n", "normal"),
            ("    5.1. Type the atoms separated by commas like the example below\n", "normal"),
            ("         O04, N09\n", "code"),
            ("    5.1. Type bonds separated by semicolons like the example below\n", "normal"),
            ("         O04_H27; H27_N09\n", "code")
        ],
        "ions": [
            ("Regarding Ions\n", "bold"),
            ("6. If the molecule to be rendered has ions, select the checkbox specifying that it has.\n","normal"),
            ("7. Click on add ion\n", "normal"),
            ("    7.1. From the drop down menu select the atom, and its charge/oxidation state\n","italic"),
            ("    7.2. Select the coordination number for the ion\n","italic"),
            ("    7.2. If there is more than one ion, click on add ion again\n","italic"),
            ("8. If you defined cell boundaries using a bond order of 0.5, check its corresponding box", "normal")
        ],
        "output": [
            ("About the output\n", "bold"),
            (" 9. Select the output path for the 3D object to be rendered\n", "normal"),
            ("10. Select the file type for the 3D object\n", "normal"),
            ("    10.1 If you chose 'is animation' in the input tab, you can only render as '.fbx' or '.glb'\n", "italic")
        ],
        "actions": [
            ("Actions you can do:\n", "bold"),
            ("11. Click on 'reset' to reset everything to the default values\n", "normal"),
            ("12. Click on 'convert' to convert your input into the 3D file according to what you selected\n", "normal")
        ]
        # Add more instruction sets here as needed
    }

    @classmethod
    def get(self, name):
        """
        Retrieve a list of instructions by name.

        :param name: The key for the instruction set (e.g., 'input', 'customization').
        :return: A list of (text, tag) tuples or an empty list if not found.
        """
        return self.instructions.get(name, [])
