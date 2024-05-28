from abc import ABC, abstractmethod
import matplotlib.pyplot as plt
import pandas as pd
from interfaces import DataVisualizer

class GDPVisualizer(DataVisualizer):
    def visualize(self):
        plt.figure(figsize=(10, 5))
        plt.plot(self.data['Year'], self.data['GDP'], label='GDP')
        if 'GNP' in self.data.columns:
            plt.plot(self.data['Year'], self.data['GNP'], label='GNP')
        plt.title('GDP and GNP over years')
        plt.xlabel('Year')
        plt.ylabel('Value')
        plt.legend()
        plt.show()