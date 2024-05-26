import pandas as pd
from abc import ABC, abstractmethod

# Абстрактный класс для загрузки данных
class DataLoader(ABC):
    @abstractmethod
    def load_data(self):
        pass

class GDPDataLoader(DataLoader):
    def load_data(self):
        # Загрузка данных о ВВП и ВНП
        data = {
            "Year": range(2008, 2023),
            "GDP": [1.5, 1.6, 1.7, 1.85, 2.0, 2.1, 2.2, 2.3, 2.5, 2.7, 2.9, 3.0, 3.1, 3.2, 3.4],
            "GNP": [1.4, 1.5, 1.55, 1.7, 1.8, 1.9, 2.0, 2.2, 2.4, 2.6, 2.7, 2.9, 3.0, 3.1, 3.2]
        }
        return pd.DataFrame(data)
