import tkinter as tk

from gui.CreateTooltip import CreateTooltip
from gui.Ionic import IonData

class SelectedIon(object):
    """
    Ion data widget that contains the information for one ion.
    This widget allows the user to select an element, specify its charge,
    and coordination number based on predefined ionic radii data.
    """
    def __init__(self, parent, row_number, column_number):
        """
        Initialize the ion selection widget.

        :param parent: The parent tkinter widget where this widget will be placed.
        :param row_number: The row position in the parent layout.
        :param column_number: The column position in the parent layout.
        """
        self.var_ion = tk.StringVar()
        self.var_chargeCoord = tk.StringVar()
        self.var_charge = tk.StringVar()
        self.var_coordination = tk.StringVar()
        self.var_spin = tk.StringVar()

        self.frm_ion = tk.Frame(master=parent)
        self.frm_ion.grid(row=row_number, column=column_number, columnspan=4)
        
        self.lbl_element = tk.Label(master=self.frm_ion,
                                    text="Element")

        
        self.var_element = tk.StringVar(master=self.frm_ion)
        self.var_element.set("Element")
        self.opt_element = tk.OptionMenu(self.frm_ion,
                                         self.var_element,
                                         *IonData.IonicRadii)
        self.ttp_element = CreateTooltip(self.opt_element,
                                   "Select The element to specify charge and coordination")

        self.lbl_coordination = tk.Label(master=self.frm_ion,
                                         text="(charge, coordination)")
        self.ttm_coordination = CreateTooltip(self.lbl_coordination,
                                        "value couple: ion charge and its coordination")
        
        self.opt_charge = tk.OptionMenu(self.frm_ion,
                                        self.var_chargeCoord, [])
        self.ttp_charge = CreateTooltip(self.opt_charge,
                                  "Ionic charge for the selected element")
        
        self.var_element.trace('w', self.change_charge)
        self.var_chargeCoord.trace('w', self.select_pair)
        
        self.lbl_element.grid(column=0, row=0)
        self.opt_element.grid(column=1, row=0)
        self.lbl_coordination.grid(column=2, row=0)
        self.opt_charge.grid(column=3, row=0)

    def change_charge(self, *args):
        """
        Update the charge and coordination options when a new element is selected.
        """
        self.var_chargeCoord.set("")
        self.opt_charge['menu'].delete(0, 'end')
        for element in IonData.IonicRadii:
            if self.var_element.get() == element:
                dataSet = IonData.IonicRadii[element]
                l = []
                for dataPoint in dataSet:
                    charge = dataPoint.charge
                    coordination = dataPoint.coordination
                    str_charge = str(charge)
                    answer = "(" + str_charge + "," + coordination + ")"
                    l.append(answer)
                for item in l:
                    self.opt_charge['menu'].add_command(label=item,
                                                       command=tk._setit(self.var_chargeCoord, item))
                break
        
    def select_pair(self, *args):
        return
            
    def delete(self):
        """
        Remove this ion selection widget from the UI.
        """
        self.frm_ion.destroy()


