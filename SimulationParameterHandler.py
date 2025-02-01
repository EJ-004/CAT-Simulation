from tkinter import *
from tkinter.ttk import *
import numpy as np
from utils import float_entry, BaseFrameManager
from functools import partial
from ParameterFrame import *
from SimulationFrame import *
from ItemBank import *


class SimulationParameterHandler:
    def __init__(self, root):
        # Initialization of Item Bank Parameters Frame
        pframe = ParameterFrame(root, 0, 0)

        # Gathering Parameters from Parameter Frame
        self.difficulty, self.discrimination, self.guessing, self.carelessness = pframe.get_parameters()
        self.parameters = [self.difficulty, self.discrimination, self.guessing, self.carelessness]
        self.model = pframe.model

        #Getting Item Bank Amount from Parameter Frame
        self.item_amount = pframe.item_entry

        #Getting the Generate button and assigning own method
        self.generate_button = pframe.generate_button
        self.generate_button.config(command=self.generate_item_bank)

        # Initialization of Simulation Parameters Frame
        sframe = SimulationFrame(root, 0, 1)

        # Collecting the simulation parameters from Simulation Parameters Frame
        self.true_ability = sframe.ability_entry
        self.initial_estimate = sframe.initial_estimate_entry
        self.ability_estimation_algo = sframe.ability_estimation
        self.item_selection_algo = sframe.item_selection

        # Collecting the termination conditions
        self.exam_length_is_fixed = sframe.is_fixed_length
        self.max_items = sframe.max_items_entry
        self.min_sem = sframe.min_sem_entry

        # Getting Simulation Amount and Button
        self.simulation_amount = sframe.simulation_amount
        self.simulate_button = sframe.simulate_button
        self.simulate_button.config(command = self.simulate)

        # Initialization of Simulation Components
        self.item_bank = ItemBank()

    def generate_item_bank(self):
        # First Step: Hella Validation
        if not self.is_generation_valid(): # If various conditions aren't passed, unable to generate item bank
            print("Check Failed")
            return

        # Generates the difficulty values, evenly spaced out through its specified range
        difficulty = np.linspace(self.difficulty.min_val, self.difficulty.max_val, self.item_amount.value)

        # Generates the discrimination values
        discrimination = np.random.choice(
            np.arange(self.discrimination.min_val, self.discrimination.max_val + 0.01, 0.01),
            size=self.item_amount.value)

        # Generates the guessing values
        guessing = np.random.choice(
            np.arange(self.guessing.min_val, self.guessing.max_val + 0.01, 0.01),
            size=self.item_amount.value)

        # Generates the carelessness values
        carelessness = np.random.choice(
            np.arange(self.carelessness.min_val, self.carelessness.max_val + 0.01, 0.01),
            size=self.item_amount.value)

        # Generates the item bank
        items = []
        for index, (b, a, c, d) in enumerate(zip(difficulty, discrimination, guessing, carelessness)):
            items.append(Question(index + 1, b, a, c, d))

        self.item_bank.update(items)

        # For debugging
        print(items)

    def is_generation_valid(self):
        # Validation 1, check if there is a minimum item amount set
        if self.item_amount.entry.get() == "":
            print("Invalid input in number of items")
            return False
        # Validation 2, check every parameter if valid values are set
        if not all(self.parameters[i].validate() for i in range(self.model.get())):
            print("Not all parameters are valid")
            return False

        return True

    def simulate(self):
        if not self.is_simulation_valid():
            print("Invalid for Simulation")
            return
        print("Proceed with Simulation")

    def is_simulation_valid(self):
        # Check if item bank has items
        if not self.item_bank.has_items():
            print("No Item Bank")
            return False

        # Check if true ability entry isnt random and if it has a value
        if (not self.true_ability.is_randomized()) and (not self.true_ability.has_value()):
            print("No True Ability Value")
            return False

        # Check if initial ability estimate entry isnt random and if it has a value
        if (not self.initial_estimate.is_randomized()) and (not self.initial_estimate.has_value()):
            print("No Initial Ability Estimate Value")
            return False

        # Check if an ability estimation algorithm has been selected
        if self.ability_estimation_algo.get() == "":
            print("No Ability Estimation Algorithm set")
            return False

        # Check if there is a value for max items, if fixed length
        if self.exam_length_is_fixed.get() == 1:
            if not self.max_items.has_value():
                print("No Max Items set")
                return False
            else: # Check if the value is smaller than the item amount
                if self.max_items.value > self.item_bank.item_amount():
                    print("Max Items must be smaller than the ItemBank's Item Amount!")
                    return False
        else: #Else, check if there is a value for min sem, if variable length
            if not self.min_sem.has_value():
                print("No Min SEM set")
                return False



        # Check value of no. of simulations
        if not self.simulation_amount.has_value():
            print("No Simulation Amount set")
            return False

        # If all conditions are passed, return True, - is valid for simulation
        return True