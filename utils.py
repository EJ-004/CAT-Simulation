from tkinter import *
from tkinter.ttk import *
from functools import partial

def float_entry(val, min_limit, max_limit):
    #For setting the string values back to float
    min_limit = float(min_limit)
    max_limit = float(max_limit)

    # Validation if entry is empty
    if val == "":
        return True

    #Validation if negative numbers are allowed:
    if val == "-" and min_limit < 0:
        return True

    #Could add a validation for starting with "." and just add a 0 at the start, todo later

    #Disallow multiple zeroes
    if val[0] == "0" and len(val) > 1 and val[1] != ".":
        return False

    allow_temp = False #Declaration of boolean
    if ("." in str(min_limit)) or (len(str(abs(int(min_limit)))) > 2): #Checking if decimal, and if multiple numbers are required
        allow_temp = True #Allow temporary values for proper entries

    #Allows for only up to 2 decimal places
    if "." in val and len(val.split(".")[-1]) > 2:
        return False

    # Validation if the user has entered an actual integer
    try:
        value = float(val)
    except ValueError:
        return False

    if not allow_temp: #Check if it passes the vibe
        if min_limit <= value <= max_limit:
            return True
        else:
            return False

    #Everything after here is checked only if temp values are allowed
    if val == str(min_limit)[0]:
        return True

    # Check if it's the first value inputted and if it is inbetween the min and max value
    # Only works if both values are positive and are greater than 0, for values both negative, the system fails
    power = len(str(abs(int(min_limit))))
    minn = min_limit // (10**power)
    maxx = max_limit // (10**power)
    if len(val.replace("-", "")) == 1 and minn < value < maxx:
        return True

    # Check if whole value is still temp value
    if len(val.split(".")[0]) < len((str(abs(min_limit))).split(".")[0]):
        return True

    #Checks if entry is a decimal
    if "." in val:
        # Check if decimal value is still temp value
        if len(val.split(".")[1]) < len((str(abs(min_limit))).split(".")[1]):
            return True

    # Finally can perform vibe check
    if min_limit <= value <= max_limit:
        return True

    #Invalidate if conditions are not passed
    return False


class BaseFrameManager:
    def __init__(self, root, row, col):
        self.parent = root
        self.frame = Frame(root, padding=10)
        self.frame.grid(row=row, column=col, sticky="NEWS")
        self.curr_row = self.curr_col = 0

    def update_curr_grid(self, row_incr, col_incr):
        # To update grid values for easier placement management
        self.curr_row += row_incr
        self.curr_col += col_incr

    def new_row(self):
        # To reset the column whenever we increase row count
        self.curr_row += 1
        self.curr_col = 0

    def update_states(self):
        pass

    def clear_entries(self, entries=None):
        entries = entries if entries is not None else []
        for entry in entries:
            entry.delete(0, END)

    def create_label(self, text, root = None, row_incr=0, col_incr=1, rowspan=1, columnspan=1, sticky=""):
        root = self.frame if root is None else root
        # For easily creating labels
        Label(root, text=text).grid(
            row=self.curr_row, rowspan=rowspan, column=self.curr_col, columnspan=columnspan, sticky=sticky
        )
        self.update_curr_grid(row_incr, col_incr)

    def create_entry(self, validate_command, root=None, state="enabled", width=5, keyrelease_bind_event=None,
                     min_limit = None, max_limit = None,
                     focusout_bind_event=None, row_incr=0, col_incr=1, rowspan=1, columnspan=1, sticky=""):
        root = self.frame if root is None else root
        # For creating entry boxes
        entry = Entry(
            root,
            validate="key",
            validatecommand=validate_command,
            state=state,
            width=width,
        )
        if keyrelease_bind_event:
            entry.bind("<KeyRelease>", keyrelease_bind_event)
        if focusout_bind_event:
            entry.bind("<FocusOut>", focusout_bind_event)
        entry.grid(row=self.curr_row, rowspan=rowspan, column=self.curr_col, columnspan=columnspan, sticky=sticky)
        self.update_curr_grid(row_incr, col_incr)
        return entry

    def create_radiobutton(self, variable, root=None, text_list=None, value_list=None, row_incr_per_button=0,
                           rowspan=1, columnspan=1, col_incr_per_button=1, sticky="", command = None):
        root = self.frame if root is None else root
        # For easily creating radiobuttons
        text_list = text_list if not None else []
        value_list = value_list if not None else []
        for text, value in zip(text_list, value_list):
            Radiobutton(root, text=text, variable=variable, value=value, command = command).grid(
                row=self.curr_row, rowspan=rowspan, column=self.curr_col, columnspan=columnspan, sticky=sticky)
            self.update_curr_grid(row_incr_per_button, col_incr_per_button)

    def create_checkbox(self, text, variable, root=None, command=None, row_incr=0, rowspan=1, col_incr=1, columnspan=1,
                        sticky="", row = None, column = None):
        root = self.frame if root is None else root
        row = self.curr_row if row is None else row
        column = self.curr_col if row is None else column
        # For easily creating checkboxes
        Checkbutton(root, text=text, variable=variable, command=command).grid(
            row=row, rowspan=rowspan, column=column, columnspan=columnspan, sticky=sticky
        )
        self.update_curr_grid(row_incr, col_incr)

    def create_button(self, text, root=None, command = None, row_incr=0, col_incr=1, rowspan=1, columnspan=1, sticky=""):
        root = self.frame if root is None else root
        # For easily creating buttons
        button = Button(root, text=text, command = command)
        button.grid(row=self.curr_row, rowspan=rowspan, column=self.curr_col, columnspan=columnspan, sticky=sticky)
        self.update_curr_grid(row_incr, col_incr)
        return button


class EntryHolder:
    def __init__(self, root, min_val, max_val, initial_value, state = "normal", width = 5, row = 0, rowspan = 1,
                 col = 0, colspan = 1, sticky = ""):
        self.value = self.default_value = initial_value
        self.entry = Entry(
            root,
            validate="key",
            validatecommand=(root.register(float_entry), "%P", min_val, max_val),
            state=state,
            width=width,
        )
        self.entry.grid(row=row, rowspan=rowspan, column=col, columnspan=colspan, sticky=sticky)
        self.entry.bind("<KeyRelease>", self.update_values)
        self.entry.bind("<FocusOut>", self.check_values)

    def update_values(self, event):
        if self.entry.get() in ("", "-"):
            return
        if isinstance(self.value, int):
            val = int(self.entry.get())
        elif isinstance(self.value, float):
            val = float(self.entry.get())
        else:
            return
        self.value = val

    def check_values(self, event):
        if self.entry.get() in ("", "-"):
            return
        if self.entry.get()[-1] == ".":
            self.entry.insert(END, "0")

    def enable(self):
        self.entry.config(state="normal")

    def disable(self):
        self.entry.delete(0, END)
        self.value = self.default_value
        self.entry.config(state="disabled")

    def has_value(self):
        return True if self.entry.get() != "" else False


class EntryRandom(EntryHolder, BaseFrameManager):
    def __init__(self, root, min_val, max_val, initial_value, state = "normal", width = 5, row = 0, rowspan = 1,
                 col = 0, colspan = 1, sticky = ""):
        EntryHolder.__init__(self, root=root, min_val=min_val, max_val=max_val, initial_value=initial_value, state=state, width=width,
                    row=row, rowspan=rowspan,
                    col=col, colspan=colspan, sticky=sticky)

        BaseFrameManager.__init__(self, root=root, row=row, col=col)
        self.frame.destroy()

        self.is_random = IntVar(value=0)
        self.create_checkbox(text="Random", variable=self.is_random, root=root, command=self.update_entry_state,
                             sticky="E", row=row, column=col+1)

    def update_entry_state(self):
        # Updates the entry widget depending on the checkbox
        if self.is_random.get() == 1: #If Random is checked, disables the entry
            self.entry.delete(0, END)
            self.entry.config(state="disabled")

        else:
            self.entry.config(state="normal")

    def is_randomized(self):
        return True if self.is_random.get() == 1 else False


