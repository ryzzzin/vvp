from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
from interfaces import ForecastModel

class GDPForecastModel(ForecastModel):
    def forecast(self, years: int) -> pd.DataFrame:
        # Вычисление скользящего среднего
        self.data['GDP Rolling Mean'] = self.data['GDP'].rolling(window=3).mean()

        # Экстраполяция на заданное количество лет
        last_known_year = self.data['Year'].iloc[-1]
        forecast_years = [last_known_year + i for i in range(1, years + 1)]
        rolling_mean = self.data['GDP Rolling Mean'].dropna().values

        forecast_values = []
        for i in range(years):
            if len(rolling_mean) > 3:
                new_value = np.mean(rolling_mean[-3:])
            else:
                new_value = np.mean(rolling_mean)
            forecast_values.append(new_value)
            rolling_mean = np.append(rolling_mean, new_value)

        forecast_df = pd.DataFrame({'Year': forecast_years, 'GDP Forecast': forecast_values})
        return forecast_df