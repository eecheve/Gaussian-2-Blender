# gui/Instructions.py

class Instructions:
    instructions = {
        "input": [
            ("Input \n", "bold"),
            ("1. The path to the Blender executable should be found automatically in the default installation folder.\n", "normal"),
            ("    1.1. If not found: click 'search' next to the Blender path and navigate to the folder that contains blender.exe (Windows) or Blender.app (macOS).\n", "italic"),
            ("2. Select the input file(s) that you want to convert.\n", "normal"),
            ("    2.1. The input can be '.com', '.xyz', '.mol2', or '.vasp'.\n", "italic"),
            ("    2.2. If you select '.com', make sure the file includes connectivity after the atom coordinates.\n", "italic"),
            ("    2.3. If you select '.xyz' or '.mol2', bonds will be rendered based on average covalent bond lengths.\n", "italic"),
            ("    2.4. If you select '.vasp', the 'Unit Cell' tab becomes available, where you can add unit cell growth, Miller planes, and coordination polyhedra.\n", "italic"),
            ("    2.5. You can select more than one input file at a time, but all of them must share the same extension.\n", "italic"),
            ("3. Choose a model type: 'Ball-and-Stick', 'Stick-only', or 'Van-der-Waals'.\n", "normal"),
            ("4. If you select the 'is animation' box, make sure to follow these rules:\n", "normal"),
            ("    4.1. If the input is '.com':\n", "italic"),
            ("        4.1.1. In the 'input file(s)' section, select two or more '.com' files.\n", "italic"),
            ("        4.1.2. All the input files must share the same atom identity, order and connectivity.\n", "italic"),
            ("    4.2. If the input is '.xyz':\n", "italic"),
            ("        4.2.1. All the cartesian coordinates must be located in the same '.xyz' file.\n", "italic"),
            ("        4.2.2. Make sure the file is a trajectory containing multiple frames, with the same number, identity, and order of atoms in each.\n", "italic"),
            ("    4.3. At the moment, there is no animation possible with '.mol2' or '.vasp' files.\n", "italic")
        ],
        "customization": [
            ("Customization \n", "bold"),
            ("5. Specify any bonds you would like to overwrite from the initial input file.\n", "normal"),
            ("    5.1. These are the characters that represent different bond orders:\n", "italic"),
            ("        5.1.1. Bond order 0.5: '_'\n", "italic"),
            ("        5.1.2. Bond order 1: '-'\n", "italic"),
            ("        5.1.3. Bond order 1.5: '%'\n", "italic"),
            ("        5.1.4. Bond order 2: '='\n", "italic"),
            ("        5.1.5. Bond order 3: '#'\n", "italic"),
            ("    5.2. Type the bonds separated by semicolons like the example below:\n", "normal"),
            ("         C01-C02; C03=O04; O04_H27; H27_N09\n", "code"),
            ("6. Check 'custom threshold' to bond atoms automatically whenever they fall within a set distance of each other, instead of (or in addition to) forcing individual bonds.\n", "normal"),
            ("    6.1. Click 'add' to create a new rule: choose Atom 1, Atom 2, a bond order (0-3), and a distance threshold in Angstroms.\n", "italic"),
            ("    6.2. Any pair of atoms of those two elements closer than the threshold will be bonded with that order. A bond order of 0 marks that pair as explicitly not bonded.\n", "italic"),
            ("    6.3. Click 'add' again for more rules, or 'remove' to delete the most recently added one.\n", "italic"),
            ("7. Identify any atoms and/or bonds that you would like to highlight in the final 3D model.\n", "normal"),
            ("    7.1. Type the atoms separated by commas like the example below:\n", "normal"),
            ("         O04, N09\n", "code"),
            ("    7.2. Type the bonds separated by semicolons like the example below:\n", "normal"),
            ("         O04_H27; H27_N09\n", "code")
        ],
        "ions": [
            ("Regarding Ions\n", "bold"),
            ("8. If the molecule to be rendered has ions, select the checkbox specifying that it has.\n", "normal"),
            ("9. Click on 'add'.\n", "normal"),
            ("    9.1. From the drop down menu select the element, and its charge/oxidation state.\n", "italic"),
            ("    9.2. Select the coordination number for the ion.\n", "italic"),
            ("    9.3. If there is more than one ion, click on 'add' again.\n", "italic"),
            ("    9.4. Click 'remove' to delete the most recently added ion.\n", "italic")
        ],
        "unit_cell": [
            ("Unit Cell \n", "bold"),
            ("This tab only becomes available when your input type (in the Input tab) is set to '.vasp'.\n", "italic"),
            ("10. If you defined cell boundaries in your input using a bond order of 0.5, check 'unit cell boundaries' to render them as solid unit cell edges.\n", "normal"),
            ("11. Check 'allow unit cell growth' to render one or more duplicated copies of the unit cell.\n", "normal"),
            ("    11.1. Click 'add cell growth', then choose how many times to repeat the cell along x, y, and z (1-5 each).\n", "italic"),
            ("    11.2. You can add more than one growth row to render several different supercell sizes in the same batch.\n", "italic"),
            ("12. Check 'allow Miller indices' to render crystallographic planes.\n", "normal"),
            ("    12.1. Click 'add plane', then choose h, k, and l (each from -9 to 9).\n", "italic"),
            ("    12.2. Every Miller plane you add is rendered on every unit cell growth size defined above.\n", "italic"),
            ("13. Check 'build polyhedra' to draw coordination polyhedra around selected center atoms.\n", "normal"),
            ("    13.1. Click 'add center', then choose the element that will act as the polyhedron center.\n", "italic"),
            ("    13.2. Any atom of that element with three or more bonded neighbors will get a convex-hull polyhedron built around it.\n", "italic"),
            ("14. Click 'Clear' to reset unit cell boundaries, growth, Miller planes, and polyhedra back to empty.\n", "normal")
        ],
        "output": [
            ("About the output\n", "bold"),
            ("15. Select the output path for the 3D object to be rendered.\n", "normal"),
            ("16. Select the file type for the 3D object: '.fbx', '.obj', '.dae', '.glb', '.stl', or '.usdz'.\n", "normal"),
            ("    16.1. If you chose 'is animation' in the input tab, you can only render as '.fbx', '.glb', or '.usdz'.\n", "italic")
        ],
        "actions": [
            ("Actions you can do:\n", "bold"),
            ("17. Click on 'Reset' to reset everything to the default values.\n", "normal"),
            ("18. Click on 'Convert!' to convert your input into the 3D file according to what you selected.\n", "normal")
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
