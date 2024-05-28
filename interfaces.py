from abc import ABC, abstractmethod
import pandas as pd

class DataLoader(ABC):
    @abstractmethod
    def load_data(self, file_path: str) -> pd.DataFrame:
        pass

class DataAnalyzer(ABC):
    def __init__(self, data: pd.DataFrame):
        self.data = data

    @abstractmethod
    def analyze(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def calculate_growth(self):
        pass

class DataVisualizer(ABC):
    def __init__(self, data: pd.DataFrame):
        self.data = data

    @abstractmethod
    def visualize(self):
        pass

class ForecastModel(ABC):
    def __init__(self, data: pd.DataFrame):
        self.data = data

    @abstractmethod
    def forecast(self, years: int) -> pd.DataFrame:
        pass
