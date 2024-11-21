import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import mplfinance as mpf

# Load the dataset
df = pd.read_csv('infy_stock.csv')

# Convert the 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Set 'Date' as the index
df.set_index('Date', inplace=True)

# Display the first 10 rows of the dataset
print("First 10 rows of the dataset:")
print(df.head(10))

# Check for missing values and handle them
print("\nMissing values in each column:")
print(df.isnull().sum())
df.fillna(method='ffill', inplace=True)

# Plot the closing price over time
plt.figure(figsize=(10, 6))
plt.plot(df['Close'], label='Closing Price')
plt.title('Closing Price Over Time')
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.legend()
plt.show()

# Plot a candlestick chart using mplfinance
mpf.plot(df, type='candle', style='charles', volume=True, title='Candlestick Chart')

# Calculate the daily return percentage
df['Daily Return (%)'] = ((df['Close'] - df['Open']) / df['Open']) * 100

# Statistical Analysis
average_return = df['Daily Return (%)'].mean()
median_return = df['Daily Return (%)'].median()
std_dev_close = df['Close'].std()

print(f"\nAverage Daily Return: {average_return:.2f}%")
print(f"Median Daily Return: {median_return:.2f}%")
print(f"Standard Deviation of Closing Prices: {std_dev_close:.2f}")

# Calculate the 50-day and 200-day moving averages
df['50-Day MA'] = df['Close'].rolling(window=50).mean()
df['200-Day MA'] = df['Close'].rolling(window=200).mean()

# Plot the moving averages
plt.figure(figsize=(10, 6))
plt.plot(df['Close'], label='Closing Price', alpha=0.5)
plt.plot(df['50-Day MA'], label='50-Day Moving Average', color='green')
plt.plot(df['200-Day MA'], label='200-Day Moving Average', color='red')
plt.title('50-Day and 200-Day Moving Averages')
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend()
plt.show()

# Volatility analysis using rolling standard deviation (30-day window)
df['30-Day Volatility'] = df['Close'].rolling(window=30).std()

plt.figure(figsize=(10, 6))
plt.plot(df['30-Day Volatility'], label='30-Day Volatility', color='orange')
plt.title('Stock Price Volatility (30-Day Rolling Std)')
plt.xlabel('Date')
plt.ylabel('Volatility')
plt.legend()
plt.show()

# Identify bullish and bearish trends based on moving averages
df['Trend'] = np.where(df['50-Day MA'] > df['200-Day MA'], 'Bullish', 'Bearish')

# Filter bullish and bearish periods
bullish = df[df['Trend'] == 'Bullish']
bearish = df[df['Trend'] == 'Bearish']

# Plot bullish and bearish trends with fill_between
plt.figure(figsize=(14, 7))

# Bullish periods
plt.fill_between(bullish.index, df.loc[bullish.index, 'Close'], color='green', alpha=0.3, label='Bullish')

# Bearish periods
plt.fill_between(bearish.index, df.loc[bearish.index, 'Close'], color='red', alpha=0.3, label='Bearish')

# Adding labels and titles
plt.title("Bullish and Bearish Trends in Stock Price")
plt.xlabel("Date")
plt.ylabel("Stock Price")
plt.legend()

# Show the plot
plt.show()
