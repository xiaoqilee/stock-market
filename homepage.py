# a GUI for the homepage

# import the tkinter package
from tkinter import *
import customtkinter as ctk # for modern style widgets
import yfinance as yf
import pandas as pd

# set mode and theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class Homepage:
    def __init__(self, root):
        # add title to window
        root.title("Stock Market")

        # define geometry of window
        root.geometry("375x250")

        # configure root so it stretches in all directions
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # add a mainframe which is sticky in all directions
        # add some padding (e.g. 5 pixels) to the frame
        mainframe = ctk.CTkFrame(root, fg_color="#f2deea")
        mainframe.grid(column=0, row=0, sticky="news")

        # weight column to expand with the window
        mainframe.columnconfigure(0, weight=1)

        # define variables for home screen labels
        self.stock_ticker = StringVar()
        self.graph = StringVar()
        self.summary_stats = StringVar()

        # add a label in the GUI for the stock ticker
        label = ctk.CTkLabel(mainframe, text='Enter Stock Ticker:', text_color="#565b5e")
        label.grid(column=1, row=1, padx=20, pady=5)

        # add an Entry in the GUI for the stock ticker
        self.entry = ctk.CTkEntry(mainframe, textvariable=self.stock_ticker, fg_color="#fdfaff", border_color="#ecaec5", text_color="#e26c99")
        self.entry.grid(column=1, row=2, padx=20, pady=5)

        # add a label in the GUI for the time range
        label = ctk.CTkLabel(mainframe, text='Select Time Range:', text_color="#565b5e")
        label.grid(column=1, row=3, padx=20, pady=5)

        # add a ComboBox to the first frame and add it to the GUI
        self.combo = ctk.CTkComboBox(mainframe, values=['1 Day', '5 Days', '1 Month', '1 Year'], fg_color="#fdfaff", border_color="#ecaec5", text_color="#e26c99")
        self.combo.grid(column=1, row=4, padx=20, pady=(5,15))

        # add spacing above and below Button/Widgets in 8th row
        mainframe.rowconfigure(8, weight=1)

        # add a Button (atm just fetches the data)
        self.generate_button = ctk.CTkButton(mainframe, text="Generate", command=self.generate, fg_color="#ecaec5", text_color="#fdfaff")
        self.generate_button.grid(row=5, column=1, padx=20, pady=5)

        # add spacing above and below Button/Widgets in 8th row
        mainframe.rowconfigure(8, weight=1)

        # add label for export
        format_label = ctk.CTkLabel(mainframe, text="Select Export Format:", text_color="#565b5e")
        format_label.grid(row=2, column=2, padx=20, pady=5)

        # add combo box with options of CSV or JSON
        self.format_combo = ctk.CTkComboBox(mainframe, values=["CSV", "JSON"], fg_color="#fdfaff", border_color="#ecaec5", text_color="#e26c99")  # Adjust width as needed
        self.format_combo.set("CSV")
        self.format_combo.grid(row=3, column=2, padx=20, pady=(5,10))

        # download button to download data in chosen data format
        self.download_button = ctk.CTkButton(mainframe, text="Download", command=self.download, fg_color="#ecaec5", text_color="#fdfaff")
        self.download_button.grid(row=4, column=2, padx=20, pady=5)


    def generate(self):
        # change ticker to uppercase and get the selected range form the combo box 
        self.ticker = self.entry.get().upper() 
        time_range = self.combo.get()

        # assign a period and interval based on the time range selected
        if time_range == '1 Day':
            period = '1d'
            frequency = '5m'  
        elif time_range == '5 Days':
            period = '5d'
            frequency = '30m' 
        elif time_range == '1 Month':
            period = '1mo'
            frequency = '4h'
        elif time_range == '1 Year':
            period = '1y'
            frequency = '1wk'
        else:
            period = '1d'
            frequency = '5m' 

        # get the data from yahoo finance
        try:
            self.data = yf.download(self.ticker, period=period, interval=frequency) # download data from yf as a pd df
            self.stats(self.ticker, self.data)
        except Exception as e:
                pass
        
    # open new window for stats
    def stats(self, ticker, data):
        popup_window = ctk.CTkToplevel()
        popup_window.title(f"Statistics for {self.ticker}")
        
        ctk.CTkLabel(popup_window, text="temp").pack(padx=20, pady=20)

        label = ctk.CTkLabel(popup_window, text="Temp placeholder")
        label.grid(column=0, row=2, sticky="news")

    # download as csv or json into current directory based on chosen data format
    def download(self):
        data_format = self.format_combo.get()
        filename = "{} stock data.{}".format(self.ticker, data_format.lower())

        try:
            if data_format == "CSV":
                self.data.to_csv(filename)
            elif data_format == "JSON":
                self.data.to_json(filename, orient='records')
        except Exception as e:
            pass

# create a root Tk object
root = ctk.CTk()

# create an AddReturn object with the Tk root object as an argument
Homepage(root)

# call the mainloop method on the Tk root object
root.mainloop()