class ComReader():
    """
    Reads atomic coordinates and connectivity straight out of a Gaussian
    .com file. Unlike XyzReader/VaspReader, no BondOrderCalculator is
    needed here - .com files carry their own explicit bond list and bond
    orders, the same way .mol2 files do, so there's nothing to infer from
    geometry.

    A .com file is laid out as: route section, blank line, title line,
    blank line, charge/multiplicity line, the atom coordinate block, a
    blank line, then the connectivity block (optionally followed by a
    trailing blank line at end of file).
    """

    def extract_coords_from_com_file(self, com_file_path):
        """
        Extracts atomic symbols and 3D coordinates from a .com file's
        coordinate block.

        :param com_file_path: (str) Path to the .com file.
        :return: (list) A list of [symbol, x, y, z] entries.
        """
        lines = self._read_tokenized_lines(com_file_path)
        coord_block, _ = self._locate_coord_and_connectivity_blocks(lines, com_file_path)

        coords = []
        for row in coord_block:
            if len(row) != 4:
                raise ValueError(f"Malformed coordinate line in '{com_file_path}': {row}")
            symbol, x, y, z = row
            coords.append([symbol, float(x), float(y), float(z)])
        return coords

    def obtain_all_bond_orders(self, coords, com_file_path):
        """
        Reads the connectivity block of a .com file and expands it into
        one (atom1, atom2, bond_symbol) entry per bond.

        :param coords: (list) [symbol, x, y, z] entries, from extract_coords_from_com_file -
                        used to translate the connectivity block's plain atom indices
                        (1, 2, 3, ...) into the same "symbol+index" labels
                        (e.g. "C01") the other readers use.
        :param com_file_path: (str) Path to the .com file.
        :return: (list) A list of (atom1_label, atom2_label, bond_symbol) tuples.
        """
        lines = self._read_tokenized_lines(com_file_path)
        _, connect_block = self._locate_coord_and_connectivity_blocks(lines, com_file_path)

        indexed_coords = self.assign_indices(coords)
        atom_index_map = {index + 1: atom[0] for index, atom in enumerate(indexed_coords)}

        bond_order_map = {
            '0.5': '_',    # transition/hydrogen bond
            '1.0': '-',    # single bond
            '1.5': 'res1', # resonance bond, between single and double
            '2.0': '=',    # double bond
            '2.5': 'res2', # resonance bond, between double and triple
            '3.0': '#',    # triple bond
        }

        bond_orders = []
        for atom1_index, atom2_index, order_code in self._expand_connectivity_lines(connect_block):
            bond_symbol = bond_order_map.get(order_code)
            if bond_symbol is None:
                print(f"ComReader: unrecognized bond order code '{order_code}' in '{com_file_path}', skipping.")
                continue

            atom1 = atom_index_map.get(int(atom1_index))
            atom2 = atom_index_map.get(int(atom2_index))
            if atom1 is None or atom2 is None:
                print(f"ComReader: connectivity entry ({atom1_index}, {atom2_index}) refers to an atom "
                      f"outside the coordinate block in '{com_file_path}', skipping.")
                continue

            bond_orders.append((atom1, atom2, bond_symbol))
        return bond_orders

    def assign_indices(self, raw_coords):
        """
        Assigns unique two-digit (or three-digit, for 100+ atoms) indices
        to atomic symbols. Same convention XyzReader/Mol2Reader/VaspReader
        use, so labels line up across every input type.

        :param raw_coords: (list) List of raw coordinates.
        :return: (list) A list of lists with atomic symbols assigned a unique index.
        """
        num_atoms = len(raw_coords)
        digits = 3 if num_atoms >= 100 else 2
        indexed_coords = []
        for index, entry in enumerate(raw_coords, start=1):
            new_entry = entry.copy()
            new_entry[0] = f"{entry[0]}{index:0{digits}d}"
            indexed_coords.append(new_entry)
        return indexed_coords

    def _read_tokenized_lines(self, com_file_path):
        """
        Reads a file and splits each line on whitespace, the same way
        Gaussian .com files are tokenized throughout this class. A blank
        line becomes an empty list.

        :param com_file_path: (str) Path to the file to read.
        :return: (list) One token list per line.
        """
        with open(com_file_path, 'r') as f:
            return [line.split() for line in f.readlines()]

    def _locate_coord_and_connectivity_blocks(self, lines, com_file_path):
        """
        Walks past the route section, title, and charge/multiplicity line
        (everything up to and including the second blank line, plus one
        more line) to find the coordinate block, then reads up to the
        blank line that separates it from the connectivity block, then
        reads the connectivity block up to its own trailing blank line
        (or end of file, if there isn't one).

        :param lines: (list) Tokenized lines, from _read_tokenized_lines.
        :param com_file_path: (str) Path to the file - only used for error messages.
        :return: (tuple) (coord_block, connect_block), each a list of tokenized lines.
        """
        coord_start = self._index_after_nth_blank_line(lines, blank_count=2, extra_lines=1, com_file_path=com_file_path)
        coord_block = self._lines_before_next_blank_line(lines[coord_start:])
        if not coord_block:
            raise ValueError(f"No atom coordinates found in '{com_file_path}'.")

        connect_start = coord_start + len(coord_block) + 1  # +1 to skip the blank separator line
        connect_block = self._lines_before_next_blank_line(lines[connect_start:])
        return coord_block, connect_block

    def _index_after_nth_blank_line(self, lines, blank_count, extra_lines, com_file_path):
        """
        Finds the index right after the blank_count-th blank line in
        `lines`, then skips `extra_lines` more lines past it.

        :param lines: (list) Tokenized lines to search.
        :param blank_count: (int) Which blank line to stop at (1st, 2nd, ...).
        :param extra_lines: (int) Extra lines to skip past that blank line.
        :param com_file_path: (str) Path to the file - only used for the error message.
        :return: (int) Index of the first line after the target blank line and offset.
        """
        blanks_seen = 0
        for index, line in enumerate(lines):
            if not line:
                blanks_seen += 1
                if blanks_seen == blank_count:
                    return index + 1 + extra_lines
        raise ValueError(
            f"Expected at least {blank_count} blank line(s) in '{com_file_path}', found {blanks_seen}. "
            "Is this a well-formed Gaussian .com file?"
        )

    def _lines_before_next_blank_line(self, lines):
        """
        Returns every line up to (but not including) the next blank line.
        If there's no further blank line, returns everything - a
        trailing blank line at end of file isn't required.

        :param lines: (list) Tokenized lines to search.
        :return: (list) Lines before the next blank line.
        """
        for index, line in enumerate(lines):
            if not line:
                return lines[:index]
        return lines

    def _expand_connectivity_lines(self, connect_block):
        """
        Expands Gaussian's compact per-atom connectivity lines - one atom
        index followed by (bonded_atom_index, bond_order_code) pairs -
        into one (atom_index, bonded_atom_index, bond_order_code) triple
        per bond. An atom with no new bonds to declare (just its own
        index, nothing after it) contributes nothing.

        :param connect_block: (list) Tokenized connectivity lines.
        :return: (list) [atom_index, bonded_atom_index, bond_order_code] triples (still strings).
        """
        triples = []
        for line in connect_block:
            if len(line) < 3:
                continue
            atom_index = line[0]
            pairs = line[1:]
            for i in range(0, len(pairs), 2):
                bonded_index, order_code = pairs[i], pairs[i + 1]
                triples.append([atom_index, bonded_index, order_code])
        return triples
