from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
from data_analyzer import DataAnalyzer
from data_loader import DataLoader
from data_visualizer import DataVisualizer
from forecast_model import ForecastModel


class SalaryDataLoader(DataLoader):
    def load_data(self, file_path: str) -> pd.DataFrame:
        return pd.read_csv(file_path)

class SalaryDataAnalyzer(DataAnalyzer):
    def analyze(self) -> pd.DataFrame:
        return self.data

    def calculate_growth(self):
        self.data['Growth Men'] = self.data['Median Salary Men'].pct_change() * 100
        self.data['Growth Women'] = self.data['Median Salary Women'].pct_change() * 100
        max_growth_men = self.data['Growth Men'].max()
        min_growth_men = self.data['Growth Men'].min()
        max_growth_women = self.data['Growth Women'].max()
        min_growth_women = self.data['Growth Women'].min()
        return max_growth_men, min_growth_men, max_growth_women, min_growth_women

class SalaryVisualizer(DataVisualizer):
    def visualize(self):
        plt.figure(figsize=(10, 5))
        plt.plot(self.data['Year'], self.data['Median Salary Men'], marker='o', label='Median Salary Men')
        plt.plot(self.data['Year'], self.data['Median Salary Women'], marker='o', label='Median Salary Women')
        plt.title('Median Salary Over Years')
        plt.xlabel('Year')
        plt.ylabel('Median Salary')
        plt.legend()
        plt.grid(True)
        plt.show()

class SalaryForecastModel(ForecastModel):
    def forecast(self, years: int) -> pd.DataFrame:
        # Вычисление скользящего среднего
        self.data['Median Salary Men Rolling Mean'] = self.data['Median Salary Men'].rolling(window=3).mean()
        self.data['Median Salary Women Rolling Mean'] = self.data['Median Salary Women'].rolling(window=3).mean()

        # Экстраполяция на заданное количество лет
        last_year = self.data['Year'].iloc[-1]
        forecast_years = [last_year + i for i in range(1, years + 1)]
        rolling_mean_men = self.data['Median Salary Men Rolling Mean'].dropna().values
        rolling_mean_women = self.data['Median Salary Women Rolling Mean'].dropna().values

        forecast_salaries_men = []
        forecast_salaries_women = []

        for i in range(years):
            if len(rolling_mean_men) > 3:
                new_value_men = np.mean(rolling_mean_men[-3:])
            else:
                new_value_men = np.mean(rolling_mean_men)
            forecast_salaries_men.append(new_value_men)
            rolling_mean_men = np.append(rolling_mean_men, new_value_men)

            if len(rolling_mean_women) > 3:
                new_value_women = np.mean(rolling_mean_women[-3:])
            else:
                new_value_women = np.mean(rolling_mean_women)
            forecast_salaries_women.append(new_value_women)
            rolling_mean_women = np.append(rolling_mean_women, new_value_women)

        forecast_data = pd.DataFrame({
            'Year': forecast_years,
            'Salary Forecast Men': forecast_salaries_men,
            'Salary Forecast Women': forecast_salaries_women
        })

        return forecast_data
