import tkinter as tk
from tkinter import ttk

from gui.CreateTooltip import CreateTooltip


class LabeledComboRow(object):
    """
    Builds one row of labeled dropdowns: an optional group label on top,
    followed by pairs of small field-labels and comboboxes.

    This is a small reusable building block used by UnitCellRegion.py in
    two ways:
        - A single instance for "unit cell growth" (x, y, z)
        - One instance per row for each Miller plane (h, k, l), created
          and destroyed dynamically by the "add plane" / "Remove Last" /
          "Remove All" buttons.
    """

    def __init__(self, parent, input_label_list, option_ranges,
                 group_label=None, group_tooltip=None, field_tooltips=None,
                 bg="#e0e0e0", fg="black", padx=2, pady=2, combobox_width=5):
        """
        :param parent: The parent widget this row's frame will be placed in.
        :param input_label_list: Small label text for each field, e.g. ["x:", "y:", "z:"].
        :param option_ranges: List of (min, max) tuples, one per field. Defines the
                               values shown in that field's dropdown, e.g. [(1, 5), (1, 5), (1, 5)].
        :param group_label: Optional header text shown above the row, e.g. "Choose unit cell growth".
                             If None, no header is shown (used for repeated rows like Miller planes).
        :param group_tooltip: Optional tooltip text attached to the group_label.
        :param field_tooltips: Optional list of tooltip strings, one per field. Leave as None
                                to skip per-field tooltips (only the group_tooltip is shown).
        :param bg: Background color used for the frame and labels.
        :param fg: Text color used for the labels.
        :param padx: Horizontal padding around each field.
        :param pady: Vertical padding around each field.
        :param combobox_width: Width of each dropdown, in characters.
        """
        if len(input_label_list) != len(option_ranges):
            raise ValueError("input_label_list and option_ranges must be the same length")

        self.frame = tk.Frame(master=parent, bg=bg)

        self.field_vars = []       # one StringVar per field, same order as input_label_list
        self.field_widgets = []    # the actual Combobox widgets, same order as input_label_list

        current_row = 0

        # Optional header label, e.g. "Choose unit cell growth"
        if group_label:
            self.group_label_widget = tk.Label(master=self.frame, text=group_label, bg=bg, fg=fg)
            self.group_label_widget.grid(row=current_row, column=0,
                                          columnspan=len(input_label_list) * 2, sticky="w")
            if group_tooltip:
                CreateTooltip(self.group_label_widget, group_tooltip)
            current_row += 1

        # Build one small label + combobox pair per field
        for index, field_label_text in enumerate(input_label_list):
            low, high = option_ranges[index]
            values = [str(v) for v in range(low, high + 1)]

            field_label = tk.Label(master=self.frame, text=field_label_text, bg=bg, fg=fg)
            field_label.grid(row=current_row, column=index * 2, padx=(padx, 2), pady=pady)

            # Default to 0 when it's a valid option (matches the old single-value defaults),
            # otherwise fall back to the lowest value in range.
            default_value = 0 if low <= 0 <= high else low
            field_var = tk.StringVar(value=str(default_value))
            field_combobox = ttk.Combobox(master=self.frame, textvariable=field_var,
                                           values=values, width=combobox_width, state="readonly")
            field_combobox.grid(row=current_row, column=index * 2 + 1, padx=(0, padx), pady=pady)

            if field_tooltips:
                CreateTooltip(field_combobox, field_tooltips[index])

            self.field_vars.append(field_var)
            self.field_widgets.append(field_combobox)

    def get_values(self):
        """
        Returns the current values of every field in this row, as a list of ints.
        Example: [1, 1, 1] for a unit cell growth row, or [1, 0, 0] for a Miller plane row.
        """
        return [int(field_var.get()) for field_var in self.field_vars]

    def set_values(self, values):
        """
        Sets the current values of every field in this row.

        :param values: A list of ints, one per field, in the same order as input_label_list.
        """
        for field_var, value in zip(self.field_vars, values):
            field_var.set(str(value))

    def destroy(self):
        """Removes this row's widgets from the screen."""
        self.frame.destroy()
