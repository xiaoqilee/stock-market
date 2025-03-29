# Stock Price Analyzer

## Authors
* Xiao Qi Lee
* Lila Nguyen

## Project Description
Our stock price analyzer will allow users to retrieve data on a stock of interest. For access to market data, we will be using Yahoo Finance’s API. Users will be able to view the data within a specified time range (1 Day, 5 Days, 1 Month, 1 Year) and see statistics on the stock’s average price, highs and lows, and overall trends. A visual representation of the stock trends will be shown using a line graph. Furthermore, users will be able to compare their stock of interest to another stock that they are interested in.

## Project Outline
### **Interface Plan**
* GUI using Python’s Tkinter library
* Windows:
  * Home screen to enter the stock ticker and select a time range
  * Pop-up window of summary statistics and stock trend visualization
* Widgets: 
  * Labels on home screen, i.e.,
    * “Stock Ticker:”
    * “Graph:”
    * “Summary Statistics:”
  * Search bar for stock ticker input from user
  * Drop-down menu to select time range (1 Day, 5 Days, 1 Month, 1 Year)
  * Button to fetch data and generate:
    * Stock trend visualization
    * Summary statistics
  * Pop-up message for when data retrieval fails
  
### **Data Collection and Storage Plan (written by Qi)**
* Use the yfinance library (utilizes web scraping) to retrieve user’s selection of stock price data 
* Store the fetched data based on their given time range in a Pandas DataFrame for easy manipulation
* If data retrieval fails, an error message and pop-up will be shown
* Users can download the dataframe as different files depending on their needs. For instance, they can export it as a JSON or CSV for readability and storage

### **Data Analysis and Visualization Plan (written by Lila)**
* Perform basic preprocessing and validation (i.e. handling missing values)
* Compute basic statistics (mean, max, min closing price) using Pandas and NumPy
* Create the line plots of stock trends using Matplotlib
* Possibly include a moving average trendline to smooth out fluctuations in price using Pandas
* Display data in a readable format using Tkinter
