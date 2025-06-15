import tkinter as tk
from gui.Utility import Utility

class Tutorial(object):
    def __init__(self, action_buttons, descriptions, walkthroughRegion):
        """
        Initializes the tutorial with a list of actions, buttons, descriptions, and a walkthrough region.
        
        :param action_buttons: List of buttons that the user needs to press in order.
        :param descriptions: List of descriptions corresponding to each action.
        :param walkthroughRegion: Widget for updating the tutorial text (e.g., a label or text box).
        """
        if not isinstance(descriptions, list):
            raise TypeError("The 'descriptions' parameter must be a list of strings.")
              
        self.action_buttons = action_buttons
        self.walkthroughRegion = walkthroughRegion
        self.descriptions_list = descriptions

    def reset_buttons_to_default(self):
        """
        Resets the highlighted button and tutorial state to the initial condition.
        """
        for action_button in self.action_buttons:
            Utility.revert_widget(action_button)
        self.walkthroughRegion.revert_text_to_default()


    def highlight_desired_buttons(self):
        for i in range(0,len(self.action_buttons)):
            button = self.action_buttons[i]
            Utility.customize_widget(tk_object=button, color_string="#fcff70")

    def populate_walthrough_text(self):
        steps = '\n'.join(self.descriptions_list)
        self.walkthroughRegion.modify_guide_text(steps)


    def start_tutorial(self):
        """
        Starts the tutorial by initializing the state and showing the first step.
        """
        self.highlight_desired_buttons()
        self.populate_walthrough_text()
