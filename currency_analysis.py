# currency_analysis.py

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from abc import ABC, abstractmethod

class CurrencyDataLoader:
    def load_data(self, file_path: str) -> pd.DataFrame:
        return pd.read_csv(file_path)

class CurrencyDataAnalyzer:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def analyze(self) -> pd.DataFrame:
        self.data['Date'] = pd.to_datetime(self.data['Date'], format='%Y-%m-%d')
        self.data['Day'] = self.data['Date'].dt.day
        return self.data

    def calculate_changes(self):
        self.data['Change Currency 1'] = self.data['Currency 1'].diff()
        self.data['Change Currency 2'] = self.data['Currency 2'].diff()

        max_increase_currency_1 = self.data['Change Currency 1'].max()
        max_increase_day_currency_1 = self.data.loc[self.data['Change Currency 1'].idxmax(), 'Date']
        
        max_decrease_currency_1 = self.data['Change Currency 1'].min()
        max_decrease_day_currency_1 = self.data.loc[self.data['Change Currency 1'].idxmin(), 'Date']

        max_increase_currency_2 = self.data['Change Currency 2'].max()
        max_increase_day_currency_2 = self.data.loc[self.data['Change Currency 2'].idxmax(), 'Date']

        max_decrease_currency_2 = self.data['Change Currency 2'].min()
        max_decrease_day_currency_2 = self.data.loc[self.data['Change Currency 2'].idxmin(), 'Date']

        return {
            'max_increase_currency_1': (max_increase_day_currency_1, max_increase_currency_1),
            'max_decrease_currency_1': (max_decrease_day_currency_1, max_decrease_currency_1),
            'max_increase_currency_2': (max_increase_day_currency_2, max_increase_currency_2),
            'max_decrease_currency_2': (max_decrease_day_currency_2, max_decrease_currency_2)
        }

class CurrencyVisualizer:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def visualize(self):
        plt.figure(figsize=(10, 5))
        plt.plot(self.data['Date'], self.data['Currency 1'], label='Currency 1')
        plt.plot(self.data['Date'], self.data['Currency 2'], label='Currency 2')
        plt.title('Exchange Rates Over Days')
        plt.xlabel('Date')
        plt.ylabel('Exchange Rate')
        plt.legend()
        plt.grid(True)
        plt.show()

class CurrencyForecastModel:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def forecast(self, days: int) -> pd.DataFrame:
        self.data['Rolling Mean Currency 1'] = self.data['Currency 1'].rolling(window=3).mean()
        self.data['Rolling Mean Currency 2'] = self.data['Currency 2'].rolling(window=3).mean()

        last_date = self.data['Date'].iloc[-1]
        forecast_dates = [last_date + pd.Timedelta(days=i) for i in range(1, days + 1)]

        rolling_mean_currency_1 = self.data['Rolling Mean Currency 1'].dropna().values
        rolling_mean_currency_2 = self.data['Rolling Mean Currency 2'].dropna().values

        forecast_currency_1 = []
        forecast_currency_2 = []

        for i in range(days):
            if len(rolling_mean_currency_1) > 3:
                new_value_1 = np.mean(rolling_mean_currency_1[-3:])
            else:
                new_value_1 = np.mean(rolling_mean_currency_1)
            forecast_currency_1.append(new_value_1)
            rolling_mean_currency_1 = np.append(rolling_mean_currency_1, new_value_1)

            if len(rolling_mean_currency_2) > 3:
                new_value_2 = np.mean(rolling_mean_currency_2[-3:])
            else:
                new_value_2 = np.mean(rolling_mean_currency_2)
            forecast_currency_2.append(new_value_2)
            rolling_mean_currency_2 = np.append(rolling_mean_currency_2, new_value_2)

        forecast_data = pd.DataFrame({
            'Date': forecast_dates,
            'Forecast Currency 1': forecast_currency_1,
            'Forecast Currency 2': forecast_currency_2
        })

        return forecast_data

    def visualize_forecast(self, forecast: pd.DataFrame):
        plt.figure(figsize=(10, 5))
        plt.plot(self.data['Date'], self.data['Currency 1'], label='Actual Currency 1')
        plt.plot(self.data['Date'], self.data['Currency 2'], label='Actual Currency 2')
        plt.plot(forecast['Date'], forecast['Forecast Currency 1'], label='Forecast Currency 1', linestyle='--')
        plt.plot(forecast['Date'], forecast['Forecast Currency 2'], label='Forecast Currency 2', linestyle='--')
        plt.title('Currency Forecast')
        plt.xlabel('Date')
        plt.ylabel('Exchange Rate')
        plt.legend()
        plt.grid(True)
        plt.show()
