from tkinter import *
from tkinter.ttk import *
import numpy as np
from utils import *


def main():
    root = Tk()
    root.geometry("1000x700")
    root.title("CAT Simulation Program")
    style = Style()
    style.configure("TLabel", padding=5)
    style.configure("TEntry", padding=5)
    style.configure("TButton", padding=5)
    style.configure("TFrame", borderwidth=2, relief="solid")
    my_parameter_frame = ParameterFrame(root, 0, 0)
    item_bank = ItemBank(my_parameter_frame.get_items())
    my_simulation_frame = SimulationFrame(root, 0, 2)
    root.mainloop()

class Question:
    def __init__(self, id, question="", choices=None, ans='', b=0.0, a=1.0, c=0.0, d=1.0):
        self.id = id
        self.question = question
        self.choices = choices if choices is not None else []
        self.answer = ans
        self.difficulty = b
        self.discrimination = a
        self.lower_asymptote = c
        self.upper_asymptote = d

class ItemBank:
    def __init__(self, items):
        self.items = items if items is not None else []

class Simulation:
    pass

class SimulationFrame:
    def __init__(self, root, row, col):
        self.parent = root
        self.frame = Frame(root, padding=10)
        self.frame.grid(row=row, column=col, sticky = "NEWS")
        self.curr_row = self.curr_col = 0

        # Text for "Simulation Parameters" Title
        Label(self.frame, text="Simulation Parameters").grid(row=self.curr_row, column=self.curr_col, columnspan=5)
        self.update_curr_grid(1, 5)
        self.reset_curr_col()

        # Text for "True Ability"
        Label(self.frame, text="True Ability").grid(row=self.curr_row, column=self.curr_col, columnspan=1)
        self.update_curr_grid(0, 1)
        #Entry for "True Ability"
        self.ability = 0.0
        self.float_entry_validation = (self.parent.register(float_entry), "%P", -3.0, 3.0)
        self.ability_entry = Entry(self.frame,
                                       validate="key",  # Validates every keypress (for checking if within range)
                                       validatecommand=(self.parent.register(float_entry), "%P", -3.0, 3.0),
                                       state="enabled", width=5)
        self.ability_entry.bind("<KeyRelease>", self.update_ability_value)  # For updating the class' own values
        self.ability_entry.grid(row=self.curr_row, column=self.curr_col, columnspan=1)
        self.update_curr_grid(0, 1)
        #Checkbox for Randomized Ability
        self.random_ability = IntVar(value = 0)
        Checkbutton(self.frame, text = "Random", variable=self.random_ability,
                    command=self.update_ability_states).grid(row = self.curr_row, column = self.curr_col,
                                                     columnspan = 2, sticky = "E")
        self.update_curr_grid(1, 1)
        self.reset_curr_col()

        # Text for "Ability Estimation:"
        Label(self.frame, text="Ability Estimation:").grid(row=self.curr_row, column=self.curr_col, columnspan=1)
        self.update_curr_grid(0, 1)
        # Radiobuttons for choosing the ability estimation algorithm
        self.estimation_algorithms = ["MLE", "EaP"] #Add more as needed, must correspond with the value
        self.estimation_algorithm = StringVar(value = "")
        # Radiobutton initialization
        for algorithm in self.estimation_algorithms:
            Radiobutton(self.frame, text=algorithm, variable=self.estimation_algorithm,
                        value=algorithm).grid(row=self.curr_row, column=self.curr_col, columnspan=1)
            self.update_curr_grid(0, 1)
        self.update_curr_grid(1, 1)
        self.reset_curr_col()

        # Text for "Item Selection:"
        Label(self.frame, text="Item Selection:").grid(row=self.curr_row, column=self.curr_col, columnspan=1)
        self.update_curr_grid(0, 1)
        # Radiobuttons for choosing the ability estimation algorithm
        self.item_selection_algorithms = ["MI"]  # Add more as needed, must correspond with the value
        self.item_selection_algorithm = StringVar(value="")
        # Radiobutton initialization
        for algorithm in self.item_selection_algorithms:
            Radiobutton(self.frame, text=algorithm, variable=self.item_selection_algorithm,
                        value=algorithm).grid(row=self.curr_row, column=self.curr_col, columnspan=1)
            self.update_curr_grid(0, 1)
        self.update_curr_grid(1, 1)
        self.reset_curr_col()

        # Text for "Termination Conditions:" Title
        Label(self.frame, text="Termination Conditions:").grid(row=self.curr_row, column=self.curr_col, columnspan=5)
        self.update_curr_grid(1, 5)
        self.reset_curr_col()

        #Termination Conditions RadioButtons
        self.is_variable_length = IntVar(value = 0)
        for i, option in enumerate(["Fixed Length", "Variable Length"]):
            Radiobutton(self.frame, text=option, variable=self.is_variable_length, value=i,
                        command=self.update_termination_condition_states).grid(row=self.curr_row, column=self.curr_col,
                                                         columnspan=1)
            self.update_curr_grid(1, 0)
        self.update_curr_grid(-2, 1)

        #Text for max items and min sem as termination conditions
        self.max_items = self.min_sem = 0
        for text in ["Max Items", "Min SEM"]:
            Label(self.frame, text=text).grid(row=self.curr_row, column=self.curr_col, columnspan=1)
            self.update_curr_grid(1, 0)
        self.update_curr_grid(-2, 1)

        #Entries for max items and min sem
        self.max_items_entry = Entry(self.frame,
                                   validate="key",  # Validates every keypress (for checking if within range)
                                   validatecommand=(self.parent.register(float_entry), "%P", 0, 9999999),
                                   state="enabled", width=5)
        self.max_items_entry.bind("<KeyRelease>", self.update_max_items)  # For updating the class' own values
        self.max_items_entry.grid(row=self.curr_row, column=self.curr_col, columnspan=1)
        self.update_curr_grid(1, 0)
        self.min_sem_entry = Entry(self.frame,
                                     validate="key",  # Validates every keypress (for checking if within range)
                                     validatecommand=(self.parent.register(float_entry), "%P", 0, 1.0),
                                     state="enabled", width=5)
        self.min_sem_entry.bind("<KeyRelease>", self.update_min_sem)  # For updating the class' own values
        self.min_sem_entry.grid(row=self.curr_row, column=self.curr_col, columnspan=1)
        self.update_curr_grid(1, 1)
        self.reset_curr_col()
        self.update_termination_condition_states()

        # Text for "Initial Ability Estimate: "
        Label(self.frame, text="Initial Ability Estimate: ").grid(row=self.curr_row, column=self.curr_col, columnspan=1)
        self.update_curr_grid(0, 1)
        # Entry for "Initial Ability Estimate"
        self.initial_estimate = 0.0
        self.initial_estimate_entry = Entry(self.frame,
                                   validate="key",  # Validates every keypress (for checking if within range)
                                   validatecommand=(self.parent.register(float_entry), "%P", -3.0, 3.0),
                                   state="enabled", width=5)
        self.initial_estimate_entry.bind("<KeyRelease>", self.update_initial_estimate)  # For updating the class' own values
        self.initial_estimate_entry.grid(row=self.curr_row, column=self.curr_col, columnspan=1)
        self.update_curr_grid(0, 1)
        # Checkbox for Randomized Ability
        self.random_initial_estimate = IntVar(value=0)
        Checkbutton(self.frame, text="Random", variable=self.random_initial_estimate,
                    command=self.update_initial_estimate_state).grid(row=self.curr_row, column=self.curr_col,
                                                             columnspan=2, sticky="E")
        self.update_curr_grid(1, 1)
        self.reset_curr_col()


    def update_curr_grid(self, row_incr, col_incr):
        self.curr_row += row_incr
        self.curr_col += col_incr

    def reset_curr_col(self):
        self.curr_col = 0

    def update_ability_value(self, event):
        try:
            ability = float(self.ability_entry.get())
        except ValueError:
            return

        # Final validation for not allowing temp values to accidentally go through
        if -3.0 <= ability <= 3.0:
            self.ability = ability

    def update_max_items(self, event):
        try:
            max_items = float(self.max_items_entry.get())
        except ValueError:
            return

        # Final validation for not allowing temp values to accidentally go through
        if 0 <= max_items <= 9999999:
            self.max_items = max_items

    def update_min_sem(self, event):
        try:
            min_sem = float(self.min_sem_entry.get())
        except ValueError:
            return

        # Final validation for not allowing temp values to accidentally go through
        if 0 <= min_sem <= 1.0:
            self.min_sem = min_sem

    def update_initial_estimate(self, event):
        try:
            initial_estimate = float(self.min_sem_entry.get())
        except ValueError:
            return

        # Final validation for not allowing temp values to accidentally go through
        if -3.0 <= initial_estimate <= 3.0:
            self.min_sem = initial_estimate

    def update_ability_states(self):
        if self.random_ability.get():
            self.ability_entry.delete(0, END)
            self.ability_entry.config(state = "disabled")
        else:
            self.ability_entry.config(state="normal")

    def update_termination_condition_states(self):
        if self.is_variable_length.get():
            self.max_items_entry.delete(0, END)
            self.max_items_entry.config(state="disabled")
            self.min_sem_entry.config(state="normal")
        else:
            self.min_sem_entry.delete(0, END)
            self.min_sem_entry.config(state="disabled")
            self.max_items_entry.config(state="normal")

    def update_initial_estimate_state(self):
        if self.random_initial_estimate.get():
            self.initial_estimate_entry.delete(0, END)
            self.initial_estimate_entry.config(state = "disabled")
        else:
            self.initial_estimate_entry.config(state="normal")



class ParameterFrame:
    def __init__(self, root, row, col):
        self.parent = root
        self.frame = Frame(root, padding = 10)
        self.frame.grid(row = row, column = col)
        self.curr_row = self.curr_col = 0

        #Text for "Item Bank" Title
        Label(self.frame, text="Item Bank").grid(row = self.curr_row, column = self.curr_col, columnspan = 5)
        self.update_curr_grid(1, 5)
        self.reset_curr_col()

        # Text for "Manual Generation"
        Label(self.frame, text="Manual Generation").grid(row=self.curr_row, column=self.curr_col, columnspan=3)
        self.update_curr_grid(0, 3)

        # Import Button
        import_button = Button(self.frame, text="Import", command=self.import_item_bank)
        import_button.grid(row=self.curr_row, column=self.curr_col, columnspan=2, sticky = "E")
        self.update_curr_grid(1, 2)
        self.reset_curr_col()

        # Text for "Model"
        Label(self.frame, text="Model:").grid(row=self.curr_row, column=self.curr_col, columnspan=1, sticky = "E")
        self.update_curr_grid(0, 1)

        #Creates the radiobuttons for choosing the model
        self.model = IntVar(value=1)
        for i in range(1, 5): # For ranges 1, 2, 3, 4, as model titles:
            Radiobutton(self.frame, text=f"{i}PL", variable=self.model, value=i,
                        command=self.update_states).grid(row=self.curr_row, column=self.curr_col,
                        columnspan=1)
            self.update_curr_grid(0, 1)
        self.update_curr_grid(1, 0)
        self.reset_curr_col()

        #Text for "Min" and "Max"
        for col, text in zip([2, 3], ["Min", "Max"]):
            Label(self.frame, text=text).grid(row=self.curr_row, column=col, columnspan = 1)
        self.update_curr_grid(1, 0)
        self.reset_curr_col()


        #Labels for the Parameters
        for i in range(4):
            Label(self.frame, text=f"{i}P").grid(row=self.curr_row + i, column=self.curr_col, columnspan = 1)
        self.update_curr_grid(0, 1)

        # Labels for the Parameters
        for i, text in zip(range(4), ["Difficulty", "Discrimination", "Guessing", "Carelessness"]):
            Label(self.frame, text=text).grid(row=self.curr_row + i, column=self.curr_col, columnspan = 1, sticky = "W")
        self.update_curr_grid(0, 1)


        #Difficulty Parameter
        self.difficulty = Parameter(self.frame, self.curr_row, self.curr_col, -3.0, 3.0, 0.0)
        self.difficulty.enable()
        self.update_curr_grid(1, 0)

        # Discrimination Parameter
        self.discrimination = Parameter(self.frame, self.curr_row, self.curr_col, 0.5, 2.0, 1.0)
        self.update_curr_grid(1, 0)

        # Guessing Parameter
        self.guessing = Parameter(self.frame, self.curr_row, self.curr_col, 0.0, 0.5, 0.0)
        self.update_curr_grid(1, 0)

        # Carelessness Parameter
        self.carelessness = Parameter(self.frame, self.curr_row, self.curr_col, 0.5, 1.0, 1.0)
        self.update_curr_grid(1, 0)
        self.reset_curr_col()

        self.parameters = [self.difficulty, self.discrimination, self.guessing, self.carelessness]
        self.update_states()

        #For Number of Items
        self.item_amount = 0
        self.float_entry_validation = (self.parent.register(float_entry), "%P", 1, 9999999)
        Label(self.frame, text="Item Amount:").grid(row=self.curr_row, column=self.curr_col, columnspan = 2, sticky = "W")
        self.update_curr_grid(0, 1)
        self.item_amount_entry = Entry(self.frame,
                                   validate="key", #Validates every keypress (for checking if within range)
                                   validatecommand=self.float_entry_validation,
                                   state = "enabled", width = 8)
        self.item_amount_entry.bind("<KeyRelease>", self.update_values) #For updating the class' own values
        self.item_amount_entry.grid(row = self.curr_row, column = self.curr_col, columnspan = 2)
        self.update_curr_grid(0, 2)

        #Generate Button
        self.generate_button = Button(self.frame, text="Generate", command = self.generate_item_bank)
        self.generate_button.grid(row = self.curr_row, column = self.curr_col, sticky = "E")

        self.items = []

    def update_curr_grid(self, row_incr, col_incr):
        self.curr_row += row_incr
        self.curr_col += col_incr

    def reset_curr_col(self):
        self.curr_col = 0

    def update_states(self):
        #Check what the model selected was before the change
        current_model = self.model.get()
        prev_model = sum(parameter.is_enabled() for parameter in self.parameters)

        #If the new selected model has fewer parameters, disables the unselected ones
        if prev_model < current_model:
            for i in range(prev_model, current_model):
                self.parameters[i].enable()
        # If the new selected model has more parameters, enables the new ones
        elif prev_model > current_model:
            for i in range(prev_model - 1, current_model - 1, -1):
                self.parameters[i].disable()


    def import_item_bank(self):
        pass

    def generate_item_bank(self):
        #First Step: Hella Validation
        #Validation 1, check if there is a minimum item amount set
        if self.item_amount_entry.get() == "":
            print("Invalid input in number of items")
            return
        # Validation 2, check every parameter if valid values are set
        if not all(self.parameters[i].validate() for i in range(self.model.get())):
            print("Not all parameters are valid")
            return

        #Generates the difficulty values, evenly spaced out through its specified range
        difficulty = np.linspace(self.difficulty.min_val, self.difficulty.max_val, self.item_amount)

        #Generates the discrimination values
        discrimination = np.random.choice(np.arange(self.discrimination.min_val, self.discrimination.max_val + 0.01, 0.01),
                                          size = self.item_amount)

        # Generates the guessing values
        guessing = np.random.choice(
            np.arange(self.guessing.min_val, self.guessing.max_val + 0.01, 0.01),
            size=self.item_amount)

        # Generates the carelessness values
        carelessness = np.random.choice(
            np.arange(self.carelessness.min_val, self.carelessness.max_val + 0.01, 0.01),
            size=self.item_amount)

        #Generates the item bank
        items = []
        for index, (b, a, c, d) in enumerate(zip(difficulty, discrimination, guessing, carelessness)):
            items.append(Question(index + 1, b, a, c, d))

        self.items = items

    def update_values(self, event):
        if self.item_amount_entry.get().isdecimal():
            self.item_amount = int(self.item_amount_entry.get())

    def get_items(self):
        return self.items


class Parameter:
    def __init__(self, parent, row, col, min_limit, max_limit, default_value):
        # Initialization of values
        self.curr_row = row
        self.curr_col = col
        self.min_limit = min_limit
        self.max_limit = max_limit
        self.min_val = min_limit
        self.max_val = max_limit
        self.default_value = default_value
        self.float_entry_validation = (parent.register(float_entry), "%P", self.min_limit, self.max_limit)


        #Entry for the Minimum Value
        self.min_val_entry = Entry(parent,
                                   validate="key", #Validates every keypress (for checking if within range)
                                   validatecommand=self.float_entry_validation,
                                   state = "disabled", width = 5)
        self.min_val_entry.bind("<FocusOut>", self.check_values) # Rechecking if within valid range
        self.min_val_entry.bind("<KeyRelease>", self.update_values) #For updating the class' own values
        self.min_val_entry.grid(row=self.curr_row, column=self.curr_col)
        self.update_curr_grid(0, 1)


        #Entry for the Maximum Value
        self.max_val_entry = Entry(parent,
                                   validate="key", #Validates every keypress (for checking if within range)
                                   validatecommand=self.float_entry_validation,
                                   state = "disabled", width = 5)
        self.max_val_entry.bind("<FocusOut>", self.check_values) # Rechecking if within valid range
        self.max_val_entry.bind("<KeyRelease>", self.update_values) #For updating the class' own values
        self.max_val_entry.grid(row=self.curr_row, column=self.curr_col)



    def update_curr_grid(self, row_incr, col_incr):
        self.curr_row += row_incr
        self.curr_col += col_incr

    def reset_curr_col(self):
        self.curr_col = 0

    def clear_entries(self):
        self.min_val_entry.delete(0, END)
        self.max_val_entry.delete(0, END)

    def check_values(self, event):
        #Checks for trailing decimal points
        if self.min_val_entry.get():
            if self.min_val_entry.get()[-1] == ".":
                self.min_val_entry.insert(END, "0")
        if self.max_val_entry.get():
            if self.max_val_entry.get()[-1] == ".":
                self.max_val_entry.insert(END, "0")
        #Checks if empty, and focus is out of widget
        if self.min_val_entry.get() == "" or self.max_val_entry.get() == "":
            return
        # Checks if negative sign, and focus is out of widget
        if self.min_val_entry.get() == "-" or self.max_val_entry.get() == "-":
            return
        # True validation when there are values, checks if it is within range

        if not float(self.min_val_entry.get()) <= float(self.max_val_entry.get()):
            self.clear_entries()

    def update_values(self, event):
        try:
            min_val = float(self.min_val_entry.get())
            max_val = float(self.max_val_entry.get())
        except ValueError:
            return

        #Final validation for not allowing temp values to accidentally go through
        if self.min_limit <= min_val <= self.max_limit:
            self.min_val = min_val
        if self.min_limit <= max_val <= self.max_limit:
            self.max_val = max_val

    def disable(self):
        #Resetting the values
        self.min_val = self.max_val = self.default_value
        #Clearing entries when disable
        self.clear_entries()
        #Updating the values back to the default display
        self.update_values(None)
        #Disabling the entry widgets
        self.min_val_entry.config(state="disabled")
        self.max_val_entry.config(state="disabled")

    def enable(self):
        self.min_val_entry.config(state="normal")
        self.max_val_entry.config(state="normal")
        self.min_val = self.min_limit
        self.max_val = self.max_limit

    def is_enabled(self):
        return True if str(self.min_val_entry.cget("state")) == "normal" else False

    def validate(self):
        #Final validation check, some checks are redundant, not sure which, since there are already validation checks
        #performed on every keypress and every focus out
        try:
            min_val = float(self.min_val_entry.get())
            max_val = float(self.max_val_entry.get())
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

main()