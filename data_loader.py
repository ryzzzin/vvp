import pandas as pd
from abc import ABC
from interfaces import DataLoader

class GDPDataLoader(DataLoader):
    def load_data(self, file_path):
        return pd.read_csv(file_path)
