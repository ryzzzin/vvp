from abc import ABC, abstractmethod
import pandas as pd

class DataAnalyzer(ABC):
    def __init__(self, data):
        self.data = data

    @abstractmethod
    def analyze(self):
        pass

class GDPDataAnalyzer(DataAnalyzer):
    def analyze(self):
        self.data['GDP Test'] = self.data['GDP'].pct_change() * 100
        self.data['GNP Growth'] = self.data['GNP'].pct_change() * 100
        return self.data

# Пример использования (для проверки):
if __name__ == "__main__":
    from data_loader import GDPDataLoader
    
    loader = GDPDataLoader()
    data = loader.load_data()
    analyzer = GDPDataAnalyzer(data)
    analyzed_data = analyzer.analyze()
    print(analyzed_data)
