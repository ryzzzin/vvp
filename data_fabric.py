import pandas as pd
from data_analyzer import DataAnalyzer, GDPDataAnalyzer
from data_loader import DataLoader, GDPDataLoader
from data_visualizer import DataVisualizer, GDPVisualizer
from forecast_model import ForecastModel, GDPForecastModel
from salary_classes import SalaryDataAnalyzer, SalaryDataLoader, SalaryForecastModel, SalaryVisualizer
from running_data_module import RunDataAnalyzer, CSVDataLoader, RunDataVisualizer, SimpleMovingAverageForecast


class DataFactory:
    def __init__(self, data_type: str):
        self.data_type = data_type

    def get_loader(self) -> DataLoader:
        if self.data_type == 'run':
            return CSVDataLoader()
        elif self.data_type == 'salary':
            return SalaryDataLoader()
        elif self.data_type == 'gdp':
            return GDPDataLoader()
        else:
            raise ValueError(f"Unknown data type: {self.data_type}")

    def get_analyzer(self, data: pd.DataFrame) -> DataAnalyzer:
        if self.data_type == 'run':
            return RunDataAnalyzer(data)
        elif self.data_type == 'salary':
            return SalaryDataAnalyzer(data)
        elif self.data_type == 'gdp':
            return GDPDataAnalyzer(data)
        else:
            raise ValueError(f"Unknown data type: {self.data_type}")

    def get_visualizer(self, data: pd.DataFrame) -> DataVisualizer:
        if self.data_type == 'run':
            return RunDataVisualizer(data)
        elif self.data_type == 'salary':
            return SalaryVisualizer(data)
        elif self.data_type == 'gdp':
            return GDPVisualizer(data)
        else:
            raise ValueError(f"Unknown data type: {self.data_type}")

    def get_forecast_model(self, data: pd.DataFrame) -> ForecastModel:
        if self.data_type == 'run':
            return SimpleMovingAverageForecast(data)
        elif self.data_type == 'salary':
            return SalaryForecastModel(data)
        elif self.data_type == 'gdp':
            return GDPForecastModel(data)
        else:
            raise ValueError(f"Unknown data type: {self.data_type}")