from abc import ABC, abstractmethod
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from datetime import datetime, timedelta
import numpy as np

class DataLoader(ABC):
    @abstractmethod
    def load_data(self, file_path: str) -> pd.DataFrame:
        pass

class CSVDataLoader(DataLoader):
    def load_data(self, file_path: str) -> pd.DataFrame:
        return pd.read_csv(file_path)

class DataAnalyzer(ABC):
    def __init__(self, data: pd.DataFrame):
        self.data = data

    @abstractmethod
    def analyze(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def calculate_growth(self):
        pass

class RunDataAnalyzer(DataAnalyzer):
    def analyze(self) -> pd.DataFrame:
        self.data['Дата'] = pd.to_datetime(self.data['Дата'], format='%Y-%m-%d').dt.date
        self.data['День недели'] = pd.to_datetime(self.data['Дата']).dt.dayofweek
        return self.data

    def calculate_growth(self):
        weekend_data = self.data[self.data['День недели'] >= 5]
        total_distance_weekends = weekend_data['Пройденное расстояние (км)'].sum()
        print(f'Сумма пройденных км за все выходные дни: {total_distance_weekends} км')
        return total_distance_weekends

class DataVisualizer(ABC):
    def __init__(self, data: pd.DataFrame):
        self.data = data

    @abstractmethod
    def visualize(self):
        pass

class RunDataVisualizer(DataVisualizer):
    def visualize(self):
        fig1 = plt.figure(figsize=(14.5, 7.5))
        fig1.canvas.manager.set_window_title('Run Data Visualization - Graphs')

        # Создание первой группы графиков
        gs1 = GridSpec(2, 1)
        ax1 = fig1.add_subplot(gs1[0, 0])
        ax2 = fig1.add_subplot(gs1[1, 0])

        # График 1: Длительность бега по дням
        ax1.plot(self.data['Дата'], self.data['Длительность бега (минуты)'], marker='o', linestyle='-')
        ax1.set_title('Длительность бега по дням')
        ax1.set_xlabel('Дата')
        ax1.set_ylabel('Длительность (минуты)')

        # График 2: Пройденное расстояние по дням
        ax2.plot(self.data['Дата'], self.data['Пройденное расстояние (км)'], marker='o', linestyle='-')
        ax2.set_title('Пройденное расстояние по дням')
        ax2.set_xlabel('Дата')
        ax2.set_ylabel('Расстояние (км)')

        plt.tight_layout()
        plt.subplots_adjust(hspace=0.4)
        plt.show()

        # Создание окна для таблицы
        fig2 = plt.figure(figsize=(14.5, 7.5))
        fig2.canvas.manager.set_window_title('Run Data Visualization - Table')

        ax_table = fig2.add_subplot(111)
        ax_table.axis('tight')
        ax_table.axis('off')
        table_data = self.data[['Дата', 'Длительность бега (минуты)', 'Пройденное расстояние (км)', 'Максимальная скорость (км/ч)', 'Минимальная скорость (км/ч)', 'Средняя скорость (км/ч)', 'Средний пульс (уд/мин)']]
        table = ax_table.table(cellText=table_data.values, colLabels=table_data.columns, cellLoc='center', loc='center')
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        table.scale(1.2, 1.2)

        plt.tight_layout()
        plt.show()

        # Создание окна для третьего графика
        fig3 = plt.figure(figsize=(14.5, 7.5))
        fig3.canvas.manager.set_window_title('Run Data Visualization - Forecast')

        ax3 = fig3.add_subplot(111)
        N = 7  # Количество дней для прогнозирования
        self.data['Скользящая средняя (км)'] = self.data['Пройденное расстояние (км)'].rolling(window=3).mean()

        # Экстраполяция на N дней
        last_known_date = self.data['Дата'].iloc[-1]
        forecast_dates = [last_known_date + timedelta(days=i) for i in range(1, N+1)]
        rolling_mean = self.data['Скользящая средняя (км)'].dropna().values

        forecast_values = []
        for i in range(N):
            if len(rolling_mean) > 3:
                new_value = np.mean(rolling_mean[-3:])
            else:
                new_value = np.mean(rolling_mean)
            forecast_values.append(new_value)
            rolling_mean = np.append(rolling_mean, new_value)

        forecast_df = pd.DataFrame({'Дата': forecast_dates, 'Прогноз (км)': forecast_values})

        ax3.plot(self.data['Дата'], self.data['Пройденное расстояние (км)'], marker='o', linestyle='-', label='Фактические данные')
        ax3.plot(self.data['Дата'], self.data['Скользящая средняя (км)'], marker='o', linestyle='-', label='Скользящая средняя')
        ax3.plot(forecast_df['Дата'], forecast_df['Прогноз (км)'], marker='o', linestyle='-', color='r', label='Прогноз')
        ax3.set_title('Прогноз пройденного расстояния методом скользящей средней')
        ax3.set_xlabel('Дата')
        ax3.set_ylabel('Расстояние (км)')
        ax3.legend()

        plt.tight_layout()
        plt.show()

class ForecastModel(ABC):
    def __init__(self, data: pd.DataFrame):
        self.data = data

    @abstractmethod
    def forecast(self, days: int) -> pd.DataFrame:
        pass

class SimpleMovingAverageForecast(ForecastModel):
    def forecast(self, days: int) -> pd.DataFrame:
        self.data['Скользящая средняя (км)'] = self.data['Пройденное расстояние (км)'].rolling(window=3).mean()

        # Экстраполяция на заданное количество дней
        last_known_date = self.data['Дата'].iloc[-1]
        forecast_dates = [last_known_date + timedelta(days=i) for i in range(1, days+1)]
        rolling_mean = self.data['Скользящая средняя (км)'].dropna().values

        forecast_values = []
        for i in range(days):
            if len(rolling_mean) > 3:
                new_value = np.mean(rolling_mean[-3:])
            else:
                new_value = np.mean(rolling_mean)
            forecast_values.append(new_value)
            rolling_mean = np.append(rolling_mean, new_value)

        forecast_df = pd.DataFrame({'Дата': forecast_dates, 'Прогноз (км)': forecast_values})
        return forecast_df

# Пример использования:
file_path = 'run_data.csv'

# Загрузка данных
loader = CSVDataLoader()
data = loader.load_data(file_path)

# Анализ данных
analyzer = RunDataAnalyzer(data)
analyzed_data = analyzer.analyze()
analyzer.calculate_growth()

# Визуализация данных
visualizer = RunDataVisualizer(analyzed_data)
visualizer.visualize()

# Прогнозирование данных
forecast_model = SimpleMovingAverageForecast(analyzed_data)
forecast = forecast_model.forecast(7)
print(forecast)
