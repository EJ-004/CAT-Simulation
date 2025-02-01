from tkinter import *
from tkinter.ttk import *
from utils import *
from ParameterFrame import *
from SimulationFrame import *
from SimulationParameterHandler import *

def main():
    root = Tk()
    root.geometry("700x500")
    root.title("CAT Simulation Program")
    style = Style()
    style.configure("TLabel", padding=5)
    style.configure("TEntry", padding=5)
    style.configure("TButton", padding=5)
    #style.configure("TRadiobutton", padding=5)
    style.configure("TFrame", borderwidth=2, relief="solid")
    main_simulation = SimulationParameterHandler(root)
    root.mainloop()

main()