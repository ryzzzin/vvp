from abc import ABC, abstractmethod
import pandas as pd
from interfaces import ForecastModel

class GDPForecastModel(ForecastModel):
    def forecast(self, years):
        last_value = self.data['GDP'].iloc[-1]
        forecast_years = range(self.data['Year'].iloc[-1] + 1, self.data['Year'].iloc[-1] + 1 + years)
        forecast_values = [last_value] * years
        forecast_df = pd.DataFrame({'Year': forecast_years, 'GDP Forecast': forecast_values})
        return forecast_df