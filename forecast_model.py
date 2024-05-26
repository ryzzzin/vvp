from abc import ABC, abstractmethod
import pandas as pd

class ForecastModel(ABC):
    def __init__(self, data):
        self.data = data

    @abstractmethod
    def forecast(self, years):
        pass

class GDPForecastModel(ForecastModel):
    def forecast(self, years):
        last_value = self.data['GDP'].iloc[-1]
        forecast_years = range(self.data['Year'].iloc[-1] + 1, self.data['Year'].iloc[-1] + 1 + years)
        forecast_values = [last_value] * years
        forecast_df = pd.DataFrame({'Year': forecast_years, 'GDP Forecast': forecast_values})
        return forecast_df

# Пример использования (для проверки):
if __name__ == "__main__":
    from data_loader import GDPDataLoader
    from data_analyzer import GDPDataAnalyzer
    
    loader = GDPDataLoader()
    data = loader.load_data()
    analyzer = GDPDataAnalyzer(data)
    analyzed_data = analyzer.analyze()
    
    forecast_model = GDPForecastModel(analyzed_data)
    forecast = forecast_model.forecast(5)
    print(forecast)
