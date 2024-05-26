from data_loader import GDPDataLoader
from data_analyzer import GDPDataAnalyzer
from data_visualizer import GDPVisualizer
from forecast_model import GDPForecastModel
import matplotlib.pyplot as plt

def main():
    # Загрузка данных
    loader = GDPDataLoader()
    data = loader.load_data()
    
    # Анализ данных
    analyzer = GDPDataAnalyzer(data)
    analyzed_data = analyzer.analyze()
    
    # Визуализация данных
    visualizer = GDPVisualizer(analyzed_data)
    visualizer.visualize()
    
    # Прогнозирование
    forecast_model = GDPForecastModel(analyzed_data)
    forecast = forecast_model.forecast(5)
    
    # Визуализация прогноза
    plt.figure(figsize=(10, 5))
    plt.plot(analyzed_data['Year'], analyzed_data['GDP'], label='Actual GDP')
    plt.plot(forecast['Year'], forecast['GDP Forecast'], label='Forecast GDP', linestyle='--')
    plt.title('GDP Forecast')
    plt.xlabel('Year')
    plt.ylabel('Value')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()
