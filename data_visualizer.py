from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import pandas as pd

class DataVisualizer(ABC):
    def __init__(self, data):
        self.data = data

    @abstractmethod
    def visualize(self):
        pass

class GDPVisualizer(DataVisualizer):
    def visualize(self):
        plt.figure(figsize=(10, 5))
        plt.plot(self.data['Year'], self.data['GDP'], label='GDP')
        plt.plot(self.data['Year'], self.data['GNP'], label='GNP')
        plt.title('GDP and GNP over years')
        plt.xlabel('Year')
        plt.ylabel('Value')
        plt.legend()
        plt.show()

# Пример использования (для проверки):
if __name__ == "__main__":
    from data_loader import GDPDataLoader
    from data_analyzer import GDPDataAnalyzer
    
    loader = GDPDataLoader()
    data = loader.load_data()
    analyzer = GDPDataAnalyzer(data)
    analyzed_data = analyzer.analyze()
    visualizer = GDPVisualizer(analyzed_data)
    visualizer.visualize()
