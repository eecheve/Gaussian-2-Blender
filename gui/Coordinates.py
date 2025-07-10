class Coordinates():
    def __init__(self):
        """
        Initializes the Coordinates object, setting up a mapping for newline characters
        based on the operating system (Windows, Unix, Mac).
        """
        self.newline_char_map = { 
            "windows": '\r\n',
            "unix": '\n',
            "mac": '\r'
        }

    def get_coordinates_line_numbers(self, file_lines):
        """
        Finds the line numbers where the Cartesian coordinates are located in the file.

        :param file_lines: List of lines read from the molecular structure file.
        :type file_lines: list of str
        :param extension: File extension to check (default is ".com").

        :return: A tuple (start_line, end_line), where start_line is the first line
                    containing coordinates and end_line is the line after the last coordinate.
        :rtype: tuple
        """
        newline_chars = set(self.newline_char_map.values()) #include new line chars
        start_line = 0
        end_line = 0
        newlines_count = 0
        # Find the start of the coordinates section
        for i,line in enumerate(file_lines):
            if line in newline_chars or line.strip() == "": #if line is empty or is new line char
                    newlines_count += 1
                    if newlines_count == 2: #when the second newline is found
                        start_line = i+2 #starting line is inclusive
                    elif newlines_count == 3: #third line
                        end_line = i #end line is exclusive
                        break
        return (start_line, end_line)


    def extract_cartesian_coordinates(self, file_path):
        """
        Extracts Cartesian coordinates from a molecular structure file.

        :param file_path: The path to the file containing the molecular structure.
        :type file_path: str

        :return: A list of tuples, where each tuple contains:
                 - atom_id (str): The atomic symbol with an element index (e.g., "C01" for carbon).
                 - x (float): The x-coordinate of the atom.
                 - y (float): The y-coordinate of the atom.
                 - z (float): The z-coordinate of the atom.
        :rtype: list of tuple
        """
        with open(file_path, 'r', newline=None) as f:
            lines = f.readlines()

        line_numbers = self.get_coordinates_line_numbers(lines) #start and end points of the cartesian coordinates in the list
        lines = lines[line_numbers[0]:line_numbers[1]] #raw cartesian coordinates, separated by spaces

        # Extract the coordinates
        coordinates = []
        element_count = 1
        for i in range(len(lines)): #relevant file line indices
             line = lines[i].strip()
             parts = line.split()
             if len(parts) == 4:
                 element, x, y, z = parts
                 indexed_element = f"{element}{element_count:02d}" #make sure I'm counting the elements
                 coordinates.append((indexed_element, x, y, z))
                 element_count += 1
        return coordinates 

    def check_newline_characters(self, file_path):
        """
        Checks the newline character type used in a file.

        :param file_path: The path to the file to check.
        :type file_path: str

        :return: The newline type used in the file: 'windows', 'unix', or 'mac'.
        :rtype: str or None
        """
        with open(file_path, 'rb') as f:
            content = f.read()
        if b'\r\n' in content:
            #print(f"The file {file_path} uses Windows-style newlines (CRLF).")
            return "windows"
        elif b'\n' in content:
            #print(f"The file {file_path} uses Unix/Linux-style newlines (LF).")
            return "unix"
        elif b'\r' in content:
            #print(f"The file {file_path} uses old Mac-style newlines (CR).")
            return "mac"
        else:
            #print(f"No standard newline characters found. Please check if {file_path} has the correct content")
            return

    def check_animationframes(self, file_paths):
        """
        Checks whether all animation frames (molecular structure files) have the same number 
        and identity of elements.

        1. Gets the first element of every tuple in the first coordinate set.
        2. Creates a list 'coord' of coordinates for every file_path in the list.
        3. Compares the values in ref_elements (from the first file) with those in all_elements.
        4. Returns True if all elements match, otherwise returns False.

        :param file_paths: List of file paths to the molecular structure files.
        :type file_paths: list of str

        :return: True if all files have the same number and identity of elements, False otherwise.
        :rtype: bool
        """
        print("Checking animation frames...")
        ref_elements = [] #reference elements to compare
        ref_coord = self.extract_cartesian_coordinates(file_paths[0])
        for entry in ref_coord:
            ref_elements.append(entry[0]) #gets the first element of the first tuple list

        all_elements = []

        for i in range(1,len(file_paths)): #does not count the first element as is the ref to compare
            coord = self.extract_cartesian_coordinates(file_paths[i]) #coordinates for each file path
            element_list = [] #reset element_list for each iteration
            for c in coord:
                element_list.append(c[0]) #each element for each file path
            all_elements.append(element_list) #compiling the list of elements to compare

        for elements in all_elements:
            if elements != ref_elements:
                print("Error: at least one file has a different number and identity of elements. Cannot proceed")
                return False
        print("All files have the same number and identity of elements")
        return True

    def combine_animation_frames(self, file_paths):
        """
        Combines Cartesian coordinates from multiple molecular structure files into a single list of tuples.

        :param file_paths: A list of strings containing the paths to the files representing different frames.
        :type file_paths: list of str

        :return: A list of tuples, where each tuple contains:
                 - atom_id (str): The identifier of the atom (e.g., "C01" for carbon).
                 - coordinates (float, float, ..., float): The Cartesian coordinates for the atom across all frames.
        :rtype: list of tuple
        """
        print("combining animation frames...")
        if self.check_animationframes(file_paths):
            all_coords = []
            combined = []
            for path in file_paths:
                coord = self.extract_cartesian_coordinates(path)
                all_coords.append(coord)
            for i in range(len(all_coords[0])): #combines all cartesian coordinates for all elements into the same line
                atom_id = all_coords[0][i][0]
                coordinates = [c for sublist in all_coords for c in sublist[i][1:]]  # Flatten all coordinates
                combined.append((atom_id, *coordinates))
            print("animation frames combined")
            return combined