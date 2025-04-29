# a GUI for the homepage

# import the tkinter package
from tkinter import *
import customtkinter as ctk # for modern style widgets

# set mode and theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class Homepage:
    def __init__(self, root):
        # add title to window
        root.title("Stock Market")

        # define geometry of window
        root.geometry("500x500")

        # configure root so it stretches in all directions
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # add a mainframe which is sticky in all directions
        # add some padding (e.g. 5 pixels) to the frame
        mainframe = ctk.CTkFrame(root)
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

        # weight column to expand with the window
        mainframe.columnconfigure(0, weight=1)

        # define variables for home screen labels
        self.stock_ticker = StringVar()
        self.graph = StringVar()
        self.summary_stats = StringVar()

        # add a label in the GUI for the stock ticker
        label = ctk.CTkLabel(mainframe, text='Enter stock ticker:')
        label.grid(column=0, row=1, padx=20, pady=5)

        # add an Entry in the GUI for the stock ticker
        entry = ctk.CTkEntry(mainframe)
        entry.grid(column=0, row=2, padx=20, pady=5)

        # add a label in the GUI for the time range
        label = ctk.CTkLabel(mainframe, text='Choose time range:')
        label.grid(column=0, row=4, padx=20, pady=5)

        # add a ComboBox to the first frame and add it to the GUI
        combo = ctk.CTkComboBox(mainframe, values=['1 Day', '5 Days', '1 Month', '1 Year'])
        combo.grid(column=0, row=5, padx=20, pady=5)

        # add vertical space between Button and other widgets
        mainframe.rowconfigure(6, weight=1)

        # add a Button
        button = ctk.CTkButton(mainframe, text='Generate')
        button.grid(column=0, row=7, padx=20, pady=20)


# create a root Tk object
root = ctk.CTk()

# create an AddReturn object with the Tk root object as an argument
Homepage(root)

# call the mainloop method on the Tk root object
root.mainloop()