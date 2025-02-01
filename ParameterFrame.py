from tkinter import *
from utils import float_entry, BaseFrameManager, EntryHolder


class ParameterFrame(BaseFrameManager):
    def __init__(self, root, row, col):
        super().__init__(root, row, col)

        self.model = IntVar(value=1) # Needed for model radiobuttons
        self.init_gui()
        self.init_model_choice()
        self.init_param_gui()
        self.difficulty = self.discrimination = self.guessing = self.carelessness = None
        self.init_params()
        self.parameters = [self.difficulty, self.discrimination, self.guessing, self.carelessness]
        self.min_items, self.max_items, self.item_amount = 1, 9999999, 0
        self.item_entry = self.generate_button = None
        self.init_item_amount()

    def init_gui(self):
        # Item Bank Title
        self.create_label(text="Item Bank", row_incr=0, col_incr=5, rowspan=1, columnspan=5)
        self.new_row()

        # Manual Generation Title and Import Button
        self.create_label(text="Manual Generation", row_incr=0, col_incr=3, rowspan=1, columnspan=3)
        self.create_button(text="Import", row_incr=0, col_incr=2, rowspan=1, columnspan=2, command = self.import_item_bank)
        self.new_row()

    def init_model_choice(self):
        #Model Options
        self.create_label(text="Model:", row_incr=0, col_incr=1)
        self.create_radiobutton(self.model, text_list = ["1PL", "2PL", "3PL", "4PL"], value_list = [1, 2, 3, 4],
                                command = self.update_model_states)
        self.new_row()

    def init_param_gui(self):
        # Min and Max Text Indicators
        self.update_curr_grid(0, 2)
        self.create_label(text="Min", row_incr=0, col_incr=1)
        self.create_label(text="Max", row_incr=0, col_incr=1)
        self.new_row()

        # 1P - 4P indicators
        for i in range(1, 5):
            self.create_label(text=f"{i}P", row_incr=1, col_incr=0)
        self.update_curr_grid(-4, 1)

        # Parameter Labels
        for parameter in ["Difficulty", "Discrimination", "Guessing", "Carelessness"]:
            self.create_label(text=parameter, row_incr=1, col_incr=0, sticky="W")
        self.update_curr_grid(-4, 1)

    def init_params(self):
        # Declare the Parameters
        self.difficulty = Parameter(root=self.frame, row=self.curr_row, col=self.curr_col, min_limit=-3.0,
                                    max_limit=3.0, default_val=0.0, state = "normal")
        self.update_curr_grid(1, 0)

        self.discrimination = Parameter(root=self.frame, row=self.curr_row, col=self.curr_col, min_limit=-3.0,
                                    max_limit=3.0, default_val=0.0)
        self.update_curr_grid(1, 0)

        self.guessing = Parameter(root=self.frame, row=self.curr_row, col=self.curr_col, min_limit=-3.0,
                                    max_limit=3.0, default_val=0.0)
        self.update_curr_grid(1, 0)

        self.carelessness = Parameter(root=self.frame, row=self.curr_row, col=self.curr_col, min_limit=-3.0,
                                    max_limit=3.0, default_val=0.0)
        self.new_row()

    def init_item_amount(self):
        # For Item Amount:
        self.create_label(text=f"Item Amount:", row_incr=0, col_incr=1, columnspan = 2, sticky = "W")
        self.item_entry = EntryHolder(root = self.frame, min_val=self.min_items, max_val = self.max_items,
                                      initial_value= self.item_amount, row = self.curr_row, col = self.curr_col,
                                      colspan = 2, width = 8)
        self.update_curr_grid(0, 2)
        # Generate Button
        self.generate_button = self.create_button(text = "Generate", columnspan = 2, sticky = "E", command = self.generate)

    def update_item_amount(self, event, entry, min_limit, max_limit, var):
        if not self.item_entry.get():
            return
        val = int(self.item_entry.get())
        if self.min_items <= val <= self.max_items:
            self.item_amount = val

    def generate(self):
        pass

    def import_item_bank(self):
        pass

    def get_parameters(self):
        return self.parameters

    def update_model_states(self):
        current_model = self.model.get()
        prev_model = sum(parameter.is_enabled() for parameter in self.parameters)

        # If the new selected model has fewer parameters, disables the unselected ones
        if prev_model < current_model:
            for i in range(prev_model, current_model):
                self.parameters[i].enable()
        # If the new selected model has more parameters, enables the new ones
        elif prev_model > current_model:
            for i in range(prev_model - 1, current_model - 1, -1):
                self.parameters[i].disable()


class Parameter(BaseFrameManager):
    def __init__(self, root, row, col, min_limit, max_limit, default_val, state="disabled"):
        super().__init__(root, row, col)
        # Initialization of values
        self.curr_row = row
        self.curr_col = col
        self.min_limit = min_limit
        self.max_limit = max_limit
        self.min_val = min_limit
        self.max_val = max_limit
        self.default_val = default_val
        self.validate_command = (root.register(float_entry), "%P", self.min_limit, self.max_limit)

        # Min Entry Widget
        self.min_entry = self.create_entry(validate_command=self.validate_command, root=self.parent, state=state)
        self.min_entry.bind("<KeyRelease>", self.update_values)
        self.min_entry.bind("<FocusOut>", self.check_values)

        # Max Entry Widget
        self.max_entry = self.create_entry(validate_command=self.validate_command, root=self.parent, state=state)
        self.max_entry.bind("<KeyRelease>", self.update_values)
        self.max_entry.bind("<FocusOut>", self.check_values)


        self.entries = [self.min_entry, self.max_entry]

    def check_values(self, event):
        # Checks for trailing decimal points
        for entry in self.entries:
            if not entry.get():
                return
            if entry.get()[-1] == ".":
                entry.insert(END, "0")
            if entry.get() in ("", "-"):
                return
        # Check if values intersect
        if not float(self.min_entry.get()) <= float(self.max_entry.get()):
            self.clear_entries(entries = self.entries)

    def update_values(self, event):
        try:
            min_val = float(self.min_entry.get())
            max_val = float(self.max_entry.get())
        except ValueError:
            return

        #Final validation for not allowing temp values to accidentally go through
        if self.min_limit <= min_val <= self.max_limit:
            self.min_val = min_val
        if self.min_limit <= max_val <= self.max_limit:
            self.max_val = max_val

    def disable(self):
        #Resetting the values
        self.min_val = self.max_val = self.default_val
        #Clearing entries when disable
        self.clear_entries()
        #Disabling the entry widgets
        self.min_entry.config(state="disabled")
        self.max_entry.config(state="disabled")

    def enable(self):
        # Enabling the entry widgets
        self.min_entry.config(state="normal")
        self.max_entry.config(state="normal")
        # By default, upon being enabled, setting the values to their limits
        self.min_val = self.min_limit
        self.max_val = self.max_limit

    def is_enabled(self):
        # Checks if an entry's state is normal, can be any entry
        return True if str(self.min_entry.cget("state")) == "normal" else False

    def validate(self):
        #Final validation check, some checks are redundant, not sure which, since there are already validation checks
        #performed on every keypress and every focus out
        try:
            min_val = float(self.min_entry.get())
            max_val = float(self.max_entry.get())
        except ValueError:
            return False

        #Check if the entries and the actual values match
        if not (min_val == self.min_val and max_val == self.max_val):
            return False

        #Check if minimum value is lower than or equal to maximum value, as intended
        if not (self.min_val <= self.max_val):
            return False

        #Check if both values are within their limited range
        if not (self.min_limit <= self.min_val <= self.max_limit and self.min_limit <= self.max_val <= self.max_limit):
            return False

        #If all checks pass, then it is valid
        return True