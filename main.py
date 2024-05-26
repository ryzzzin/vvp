import pandas as pd
import matplotlib.pyplot as plt

def main():
    # Тестовые данные
    data = {
        "Year": range(2008, 2023),
        "GDP": [1.5, 1.6, 1.7, 1.85, 2.0, 2.1, 2.2, 2.3, 2.5, 2.7, 2.9, 3.0, 3.1, 3.2, 3.4],
        "GNP": [1.4, 1.5, 1.55, 1.7, 1.8, 1.9, 2.0, 2.2, 2.4, 2.6, 2.7, 2.9, 3.0, 3.1, 3.2]
    }
    df = pd.DataFrame(data)
    
    # Анализ данных
    df['GDP Growth'] = df['GDP'].pct_change() * 100
    df['GNP Growth'] = df['GNP'].pct_change() * 100
    
    # Визуализация данных
    plt.figure(figsize=(10, 5))
    plt.plot(df['Year'], df['GDP'], label='GDP')
    plt.plot(df['Year'], df['GNP'], label='GNP')
    plt.title('GDP and GNP over years')
    plt.xlabel('Year')
    plt.ylabel('Value')
    plt.legend()
    plt.show()
    
    # Прогнозирование
    last_gdp = df['GDP'].iloc[-1]
    forecast_years = range(df['Year'].iloc[-1] + 1, df['Year'].iloc[-1] + 6)
    forecast_values = [last_gdp] * 5
    forecast_df = pd.DataFrame({'Year': forecast_years, 'GDP Forecast': forecast_values})
    
    # Визуализация прогноза
    plt.figure(figsize=(10, 5))
    plt.plot(df['Year'], df['GDP'], label='Actual GDP')
    plt.plot(forecast_df['Year'], forecast_df['GDP Forecast'], label='Forecast GDP', linestyle='--')
    plt.title('GDP Forecast')
    plt.xlabel('Year')
    plt.ylabel('Value')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
