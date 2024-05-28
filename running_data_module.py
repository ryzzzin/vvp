import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np

# Шаг 1: Загрузка данных
file_path = 'run_data.csv'  # Замените на путь к вашему файлу
data = pd.read_csv(file_path)

# Преобразование столбца с датами в формат datetime
data['Дата'] = pd.to_datetime(data['Дата'], format='%Y-%m-%d')

# Шаг 2: Вывод данных в табличном формате
print(data)

# Шаг 3: Построение графиков зависимости по двум параметрам от дня
fig, axes = plt.subplots(3, 1, figsize=(12, 7.5))

# График 1: Длительность бега по дням
axes[0].plot(data['Дата'], data['Длительность бега (минуты)'], marker='o', linestyle='-')
axes[0].set_title('Длительность бега по дням')
axes[0].set_xlabel('Дата')
axes[0].set_ylabel('Длительность (минуты)')

# График 2: Пройденное расстояние по дням
axes[1].plot(data['Дата'], data['Пройденное расстояние (км)'], marker='o', linestyle='-')
axes[1].set_title('Пройденное расстояние по дням')
axes[1].set_xlabel('Дата')
axes[1].set_ylabel('Расстояние (км)')

# График 3: Прогнозирование методом скользящей средней
N = 7  # Количество дней для прогнозирования
data['Скользящая средняя (км)'] = data['Пройденное расстояние (км)'].rolling(window=3).mean()

# Экстраполяция на N дней
last_known_date = data['Дата'].iloc[-1]
forecast_dates = [last_known_date + pd.Timedelta(days=i) for i in range(1, N+1)]
rolling_mean = data['Скользящая средняя (км)'].dropna().values

forecast_values = []
for i in range(N):
    if len(rolling_mean) > 3:
        new_value = np.mean(rolling_mean[-3:])
    else:
        new_value = np.mean(rolling_mean)
    forecast_values.append(new_value)
    rolling_mean = np.append(rolling_mean, new_value)

forecast_df = pd.DataFrame({'Дата': forecast_dates, 'Прогноз (км)': forecast_values})

axes[2].plot(data['Дата'], data['Пройденное расстояние (км)'], marker='o', linestyle='-', label='Фактические данные')
axes[2].plot(data['Дата'], data['Скользящая средняя (км)'], marker='o', linestyle='-', label='Скользящая средняя')
axes[2].plot(forecast_df['Дата'], forecast_df['Прогноз (км)'], marker='o', linestyle='-', color='r', label='Прогноз')
axes[2].set_title('Прогноз пройденного расстояния методом скользящей средней')
axes[2].set_xlabel('Дата')
axes[2].set_ylabel('Расстояние (км)')
axes[2].legend()

plt.tight_layout()
plt.subplots_adjust(hspace=0.35)  # Увеличить расстояние между подграфиками
plt.show()
