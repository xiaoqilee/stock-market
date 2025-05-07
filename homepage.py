# a GUI for the homepage

# import the tkinter package
from tkinter import *
import customtkinter as ctk # for the modern twist!
from CTkMessagebox import CTkMessagebox
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# set mode and theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class Homepage:
    def __init__(self, root):
        # add title to window
        root.title("Stock Market Homepage")

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
        self.ticker = StringVar()
        self.graph = StringVar()
        self.stats = StringVar()

        # add a label in the GUI for the stock ticker
        ticker_label = ctk.CTkLabel(mainframe, text='Enter Stock Ticker(s):', text_color="#323339")
        ticker_label.grid(column=1, row=1, padx=20, pady=5, sticky="w")

        # add an Entry in the GUI for the stock ticker
        self.entry = ctk.CTkEntry(mainframe, textvariable=self.ticker, fg_color="#fdfaff",
                                  border_color="#ecaec5", text_color="#e26c99")
        self.entry.grid(column=1, row=2, padx=20, pady=5)
        self.entry.bind("<KeyRelease>", self.to_uppercase) # turns input to uppercase as User types

        # add a label in the GUI for the time range
        time_range_label = ctk.CTkLabel(mainframe, text='Select Time Range:', text_color="#323339")
        time_range_label.grid(column=1, row=3, padx=20, pady=5, sticky="w")

        # add a ComboBox to the first frame and add it to the GUI
        self.combo = ctk.CTkComboBox(mainframe, values=['1 Day', '5 Days', '1 Month', '1 Year'],
                                     fg_color="#fdfaff", border_color="#ecaec5", text_color="#e26c99")
        self.combo.grid(column=1, row=4, padx=20, pady=(5,15))

        # add a Button that fetches the stock data
        self.generate_button = ctk.CTkButton(mainframe, text="Generate", command=self.generate,
                                             fg_color="#ecaec5", text_color="#fdfaff")
        self.generate_button.grid(row=5, column=1, padx=20, pady=5)

        # add label for export
        format_label = ctk.CTkLabel(mainframe, text="Select Export Format:", text_color="#323339")
        format_label.grid(row=1, column=2, padx=20, pady=5, sticky="w")

        # add combo box with options of CSV or JSON
        self.format_combo = ctk.CTkComboBox(mainframe, values=["CSV", "JSON"], fg_color="#fdfaff",
                                            border_color="#ecaec5", text_color="#e26c99")
        self.format_combo.set("CSV")
        self.format_combo.grid(row=2, column=2, padx=20, pady=(5,10))

        # download button to download data in chosen data format
        self.download_button = ctk.CTkButton(mainframe, text="Download", command=self.download,
                                             fg_color="#ecaec5", text_color="#fdfaff")
        self.download_button.grid(row=3, column=2, padx=20, pady=5)

        # add a button to close the app
        self.close_button = ctk.CTkButton(mainframe, text="Close App", command=root.destroy,
                                          fg_color="#565b5e", text_color="#fdfaff")
        self.close_button.grid(row=5, column=2, padx=20, pady=10)


    '''
    This method automatically converts the User input for stock ticker to Uppercase.
    '''
    def to_uppercase(self, event):
        curr_ticker = self.ticker.get()
        self.ticker.set(curr_ticker.upper())

    '''
    This method gets the data from yfinance based on the inputted time range
    '''
    def generate(self):
        # change ticker to uppercase and get the selected range form the combo box   
        ticker_input = self.entry.get()
        split_tickers = ticker_input.split(',')
        self.tickers = []
        for ticker in split_tickers:
            self.tickers.append(ticker.strip())
       
        time_range = self.combo.get()

        # assign a period and interval based on the time range selected
        if time_range == '1 Day':
            period = '1d'
            self.frequency = '5m'  
        elif time_range == '5 Days':
            period = '5d'
            self.frequency = '30m' 
        elif time_range == '1 Month':
            period = '1mo'
            self.frequency = '4h'
        elif time_range == '1 Year':
            period = '1y'
            self.frequency = '1wk'
        else:
            period = '1d'
            self.frequency = '5m' 

        # get the data from yahoo finance
        try:
            # download data from yf as a pd df
            self.data = yf.download(self.tickers, period=period, interval=self.frequency)
            if self.data.empty:
                CTkMessagebox(title="Error Message", message="The stock tickers entered are invalid. Please try again.", icon="warning")
                return
            else:
                CTkMessagebox(title="Success", message="Data has been loaded", icon="check")

            # self.graph_and_stats(self.ticker, self.data)
        except Exception as e:
                CTkMessagebox(title="Error Message", message="Request could not be processed due to: {}".format(e), icon="warning")
    '''
    # open new window for graph and summary statistics
    def graph_and_stats(self, ticker, data):
        popup_window = ctk.CTkToplevel()

        # set title, size, and bg color of popup window
        popup_window.title(f"Graph & Summary Stats for {self.ticker}")
        popup_window.geometry("440x650")
        popup_window.configure(fg_color="#e6d8f3")

        # set font styles
        title_style = ("TkDefaultFont", 14, "bold")
        headers_style = ("TkDefaultFont", 12, "bold")
        values_style = ("TkDefaultFont", 12)

        # get summary stats (mean, max, min closing price)
        try:
            mean_close_price = "{:.2f}".format(data["Close", ticker].mean())
            max_close_price = "{:.2f}".format(data["Close", ticker].max())
            min_close_price = "{:.2f}".format(data["Close", ticker].min())
        except Exception as e:
            print("Error computing summary stats: ", e)

        # create labels for summary stats
        time_range = self.combo.get()
        label = ctk.CTkLabel(popup_window, text="Closing Price Summary ("+time_range+")",
                             text_color="#764c9f", font=title_style)
        label.grid(row=2, column=0, padx=20, pady=10, sticky="w")

        mean_label = ctk.CTkLabel(popup_window, text="Mean Price:", text_color="#323339",
                                  font=headers_style)
        mean_label.grid(row=3, column=0, padx=20, pady=5, sticky="w")

        max_label = ctk.CTkLabel(popup_window, text="Max Price:", text_color="#323339",
                                 font=headers_style)
        max_label.grid(row=4, column=0, padx=20, pady=5, sticky="w")

        min_label = ctk.CTkLabel(popup_window, text="Min Price:", text_color="#323339",
                                 font=headers_style)
        min_label.grid(row=5, column=0, padx=20, pady=5, sticky="w")

        # assign values to the respective labels
        mean_val = ctk.CTkLabel(popup_window, text='$'+mean_close_price, text_color="#323339",
                                font=values_style)
        mean_val.grid(row=3, column=1, padx=20, pady=5, sticky="w")

        max_val = ctk.CTkLabel(popup_window, text='$'+max_close_price, text_color="#323339",
                               font=values_style)
        max_val.grid(row=4, column=1, padx=20, pady=5, sticky="w")

        min_val = ctk.CTkLabel(popup_window, text='$'+min_close_price, text_color="#323339",
                               font=values_style)
        min_val.grid(row=5, column=1, padx=20, pady=5, sticky="w")

        # graph stock plot
        try:
            prices = data["Close", ticker]

            # calculate moving averages
            ma_20 = prices.rolling(20).mean() # for 1 Day & 1 Year
            ma_10 = prices.rolling(10).mean() # for 5 Days
            ma_5 = prices.rolling(5).mean()  # for 1 Month

            stock_fig, ax = plt.subplots(figsize=(4, 3.5))
            ax.plot(prices, label=ticker+" Close", color="black")

            # add moving averages (MA) based on selected time range
            if time_range == '1 Day':
                ax.plot(ma_20, label="20-period MA", color='orange', linestyle='--')
                ax.set_xlabel('Time')
            elif time_range == '5 Days':
                ax.plot(ma_10, label="10-period MA", color='orange', linestyle='--')
                ax.set_xlabel('Date')
            elif time_range == '1 Month':
                ax.plot(ma_5, label="5-period MA", color='orange', linestyle='--')
                ax.set_xlabel('Date')
            else:
                ax.plot(ma_20, label="20-period MA", color='orange', linestyle='--')
                ax.set_xlabel('Date')

            # set title, y-axis label, legend, and grid
            ax.set_title('{} Stock Price ({})'.format(ticker, time_range))
            ax.set_ylabel('Closing Price ($)')
            ax.legend()
            ax.grid(True, alpha=0.5, linestyle='--')

            # rotate x-axis labels
            plt.setp(ax.get_xticklabels(), rotation=45)
            stock_fig.tight_layout()

            # show plot in tkinter
            canvas = FigureCanvasTkAgg(stock_fig, master=popup_window)
            canvas.draw()
            canvas.get_tk_widget().grid(row=1, column=0, columnspan=2, padx=5, pady=10)

        except Exception as e:
            print("Error plotting data:", e)
 
        # add a button to close the window
        self.close_button = ctk.CTkButton(popup_window, text="Close Window", command=popup_window.destroy,
                                          fg_color="#debbe7", text_color="#fdfaff")
        self.close_button.grid(column=1, row=8, padx=20, pady=10, sticky="e")
    '''

    # download as csv or json into current directory based on chosen data format
    def download(self):
        try:
            if self.data.empty:
                CTkMessagebox(title="Error Message", message="Data cannot be downloaded. Ensure data has been generated and is valid.", icon="warning")
                return
        except AttributeError:
            CTkMessagebox(title="Error Message", message="Data cannot be downloaded. Ensure data has been generated and is valid.", icon="warning")
            return

        data_format = self.format_combo.get()
        time_range = self.combo.get().lower().replace(" ", "_")

        # if only one ticker was entered
        if len(self.tickers) == 1:
            t = self.tickers[0]
            filename = "{}_{} ({} freq)_data.{}".format(t, time_range, self.frequency, data_format.lower())
            try:         
                # Retrieve all columns for the specified ticker       
                ticker_data = self.data.xs(t, level=1, axis=1)
                if data_format == "CSV":
                    ticker_data.to_csv(filename)
                elif data_format == "JSON":
                    ticker_data.to_json(filename, orient='records')
                CTkMessagebox(title="Success", message="Data for {} has been exported".format(t), icon="check")
            except Exception as e:
                CTkMessagebox(title="Error Message", message="Request could not be processed due to: {}".format(e), icon="warning")
        else:
            # if multiple tickers are entered
            for t in self.tickers:
                filename = "{}_{} ({} freq)_data.{}".format(t, time_range, self.frequency, data_format.lower())
                try:
                    ticker_data = self.data.xs(t, level=1, axis=1)
                    if data_format == "CSV":
                        ticker_data.to_csv(filename)
                    elif data_format == "JSON":
                        ticker_data.to_json(filename, orient='records')
                    CTkMessagebox(title="Success", message="Data for {} has been exported".format(t), icon="check")
                except Exception as e:
                    CTkMessagebox(title="Error Message", message=f"Could not save data for {t}: {e}", icon="warning")

# create a root Tk object
root = ctk.CTk()

# create an AddReturn object with the Tk root object as an argument
Homepage(root)

# call the mainloop method on the Tk root object
root.mainloop()