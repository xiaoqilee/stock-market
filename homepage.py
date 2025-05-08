# a GUI for the homepage

# import the tkinter package
from tkinter import *
import customtkinter as ctk # for the modern twist!
from CTkMessagebox import CTkMessagebox
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates

# set mode and theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class Homepage:
    def __init__(self, root):
        # add title to window
        root.title("Stock Market Homepage")

        # define geometry of window
        root.geometry("365x225")

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

        # check to see if User entered more than 3 tickers
        if len(self.tickers) > 3:
            CTkMessagebox(title="Invalid Number of Tickers",
                          message="Please enter no more than 3 tickers, separated by commas.",
                          icon="warning")
            return
       
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
                CTkMessagebox(title="Invalid Stock Ticker",
                              message="Ensure stock tickers are entered correctly and separated by a comma.",
                              icon="warning")
                return
            self.graph_and_stats(self.tickers, self.data)
        except Exception as e:
                CTkMessagebox(title="Error Message", message="Request could not be processed due to: {}".format(e),
                              icon="warning")


    # open new window for graph and summary statistics
    def graph_and_stats(self, ticker_list, data):
        # set title, size, and bg color of popup window
        popup_window = ctk.CTkToplevel()
        popup_window.title("Graph & Summary Stats")
        popup_window.geometry("800x625") # (width, height)
        popup_window.configure(fg_color="#e6d8f3")

        # set font styles
        title_style = ("TkDefaultFont", 12, "bold")
        headers_style = ("TkDefaultFont", 11, "bold")
        values_style = ("TkDefaultFont", 11)

        time_range = self.combo.get()

        # create one plot
        stock_fig, ax = plt.subplots(figsize=(6, 4))
        line_colors = ['black', 'blue', 'purple']
        ma_colors = ['orange', 'cyan', 'yellow']
        x_label = 'Date'

        # track min/max values of all stocks
        all_prices = []

        # iterate through list
        for i, ticker in enumerate(ticker_list):
            try:
                prices = data["Close", ticker]
                all_prices.extend(prices)

                # get summary stats (mean, max, min closing price)
                mean_val = prices.mean()
                max_val = prices.max()
                min_val = prices.min()
                max_time = prices.idxmax() # time corresponding to max point
                min_time = prices.idxmin() # time corresponding to min point

                # summary stats (str)
                mean_close_price = "{:.2f}".format(mean_val)
                max_close_price = "{:.2f}".format(max_val)
                min_close_price = "{:.2f}".format(min_val)

                new_col = i*2

                # header
                header_label = ctk.CTkLabel(popup_window,
                                            text="{} Closing Summary ({})".format(ticker, time_range),
                                            text_color="#764c9f",
                                            font=title_style)
                header_label.grid(row=0, column=new_col, columnspan=2, padx=10, pady=(10,5), sticky="w")

                # summary stats
                stats = [("Mean Price:", mean_close_price),
                         ("Max Price:", max_close_price),
                         ("Min Price:", min_close_price),]

                # organize summary stats side-by-side
                for j, (type, val) in enumerate(stats, start=1):
                    type_label = ctk.CTkLabel(popup_window,
                                              text=type,
                                              text_color="#323339",
                                              font=headers_style)
                    type_label.grid(row=j+1, column=new_col, padx=10, pady=3, sticky="w")
                    val_label = ctk.CTkLabel(popup_window,
                                             text='$'+val,
                                             text_color="#323339",
                                             font=values_style)
                    val_label.grid(row=j+1, column=new_col+1, padx=10, pady=3, sticky="w")

                # plot closing price
                ax.plot(prices, label="{} Close".format(ticker), color=line_colors[i%len(line_colors)])

                # compute moving averages (MA) based on selected time range
                if time_range == '1 Day':
                    ma = prices.rolling(20).mean()
                    ma_label = ticker+" 20-period MA"
                    x_label = 'Time'
                elif time_range == '5 Days':
                    ma = prices.rolling(10).mean()
                    ma_label = ticker+" 10-period MA"
                elif time_range == '1 Month':
                    ma = prices.rolling(20).mean()
                    ma_label = ticker+" 20-period MA"
                else:
                    ma = prices.rolling(12).mean()
                    ma_label = ticker+" 12-period MA"

                # plot the moving average
                ax.plot(ma, label=ma_label, color=ma_colors[i%len(ma_colors)], linestyle='--')
            
                # annotate max and min closing prices
                offset = (max_val - min_val) * 0.10
                ax.scatter(max_time, max_val, color='red')
                ax.annotate('Max',
                            xy=(max_time, max_val), # point that arrow points to
                            xytext=(max_time, max_val+offset), # point for tail of arrow
                            arrowprops=dict(facecolor='red', color='red', arrowstyle='->')) # arrow's appearance

                ax.scatter(min_time, min_val, color='blue')
                ax.annotate('Min',
                            xy=(min_time, min_val), # point that arrow points to
                            xytext=(min_time, min_val-offset), # point for tail of arrow
                            arrowprops=dict(facecolor='blue', color='blue', arrowstyle='->')) # arrow's appearance
             
            except Exception as e:
                print("Error computing stats: ", e)
                continue
            
        # dynamically adjust y-axis to reflect data in different ranges
        y_min, y_max = min(all_prices), max(all_prices)
        y_padding = (y_max-y_min)*0.1
        ax.set_ylim(y_min-y_padding, y_max+y_padding)

        # set title, axes labels, legend, and grid
        ax.set_title('Stock Price Comparison ({})'.format(time_range))
        ax.set_xlabel(x_label)
        ax.set_ylabel('Price ($)')
        ax.legend(fontsize='small')
        ax.grid(True, alpha=0.5, linestyle='--')

        # format datetime df to be more readable when plotted :")
        if time_range == '1 Day':
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))
        elif time_range == '5 Days':
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
            ax.xaxis.set_major_locator(mdates.DayLocator(interval=1))
        elif time_range == '1 Month':
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
            ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
        elif time_range == '1 Year':
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
            ax.xaxis.set_major_locator(mdates.MonthLocator(interval=2))

        plt.setp(ax.get_xticklabels())
        plt.tight_layout()

        # show plot in tkinter window
        canvas = FigureCanvasTkAgg(stock_fig, master=popup_window)
        canvas.draw()
        canvas.get_tk_widget().grid(row=5, column=0, columnspan=6, padx=10, pady=10)

        # add a button to close the window
        self.close_button = ctk.CTkButton(popup_window,
                                          text="Close Window",
                                          command=popup_window.destroy,
                                          fg_color="#debbe7",
                                          text_color="#fdfaff")
        self.close_button.grid(column=0, row=8, padx=20, pady=10, sticky="w")


    # download as csv or json into current directory based on chosen data format
    def download(self):
        try:
            if self.data.empty:
                CTkMessagebox(title="Error Message", message="Data cannot be downloaded. Ensure data has been "
                                                             "generated and is valid.", icon="warning")
                return
        except AttributeError:
            CTkMessagebox(title="Error Message", message="Data cannot be downloaded. Ensure data has been generated "
                                                         "and is valid.", icon="warning")
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
                CTkMessagebox(title="Error Message", message="Request could not be processed due to: {}".format(e),
                              icon="warning")
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
                    CTkMessagebox(title="Success", message="Data for {} data has been exported".format(t), icon="check")
                except Exception as e:
                    CTkMessagebox(title="Error Message", message=f"Could not save data for {t}: {e}", icon="warning")

# create a root Tk object
root = ctk.CTk()

# create an AddReturn object with the Tk root object as an argument
Homepage(root)

# call the mainloop method on the Tk root object
root.mainloop()
