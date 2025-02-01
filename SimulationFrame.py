from tkinter import *
from tkinter.ttk import *
import numpy as np
from utils import float_entry, BaseFrameManager, EntryHolder, EntryRandom
from functools import partial

class SimulationFrame(BaseFrameManager):
    def __init__(self, root, row, col):
        super().__init__(root, row, col)

        # Simulation Parameters Title
        self.create_label(text="Simulation Parameters", row_incr=0, col_incr=3, rowspan=1, columnspan=3)
        self.new_row()

        # For True Ability
        self.create_label(text=f"True Ability:", sticky="E")
        self.ability_entry = EntryRandom(root=self.frame, min_val=-3.0, max_val=3.0, sticky = "W",
                                      initial_value=0.0, row=self.curr_row, col=self.curr_col, width=8)
        self.new_row()

        # For Initial Ability
        self.create_label(text=f"Initial Estimate:", sticky="E")
        self.initial_estimate_entry = EntryRandom(root=self.frame, min_val=-3.0, max_val=3.0, sticky="W",
                                         initial_value=0.0, row=self.curr_row, col=self.curr_col, width=8)
        self.new_row()

        # For Ability Estimation:
        self.create_label(text=f"Ability Estimation:", sticky="E")
        self.ability_estimation = StringVar(value="")
        self.create_radiobutton(variable = self.ability_estimation, text_list=("EaP", "MLE"), value_list=("EaP", "MLE"))
        self.new_row()

        # For Item Selection:
        self.create_label(text=f"Item Selection:", sticky="E")
        self.item_selection = StringVar(value="MI")
        self.create_radiobutton(variable=self.item_selection, text_list=["MI"], value_list=["MI"])
        self.new_row()

        # Termination Conditions Title
        self.create_label(text="Termination Conditions", row_incr=0, col_incr=3, rowspan=1, columnspan=3)
        self.new_row()

        # Radiobuttons for Exam Length
        self.is_fixed_length = IntVar(value=1)
        self.create_radiobutton(variable = self.is_fixed_length, text_list=("Fixed Length", "Variable Length"),
                                value_list=(1, 0), sticky = "W", row_incr_per_button=1, col_incr_per_button=0,
                                command=self.update_exam_length_entries)
        self.update_curr_grid(-2, 1)

        # Max Items Label and Entry
        self.create_label(text="Max Items")
        self.max_items_entry = EntryHolder(root=self.frame, min_val=1, max_val=9999999, initial_value=0,
                                           row = self.curr_row, col=self.curr_col)
        self.new_row()
        self.update_curr_grid(0, 1)

        # Min SEM Label and Entry
        self.create_label(text="Min SEM")
        self.min_sem_entry = EntryHolder(root=self.frame, min_val=0, max_val=1, initial_value=0.35,
                                           row=self.curr_row, col=self.curr_col, state="disabled")
        self.new_row()

        # No of Simulations Label and Entry
        self.create_label("No. of Simulations")
        self.simulation_amount = EntryHolder(root=self.frame, min_val=1, max_val=1000, initial_value=1,
                                           row = self.curr_row, col=self.curr_col)
        self.update_curr_grid(0, 1)

        # Simulate Button
        self.simulate_button = self.create_button(text = "Simulate", columnspan = 1, sticky = "E")



    def update_exam_length_entries(self):
        if self.is_fixed_length.get() == 1:
            self.max_items_entry.enable()
            self.min_sem_entry.disable()
        else:
            self.max_items_entry.disable()
            self.min_sem_entry.enable()


