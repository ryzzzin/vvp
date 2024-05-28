from tkinter import filedialog, messagebox, ttk
import tkinter as tk

from matplotlib import pyplot as plt
from data_fabric import DataFactory


# Пример интерфейса
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Analysis Tool")
        
        self.label = tk.Label(root, text="Choose Data Type:")
        self.label.pack(pady=10)
        
        self.data_type = tk.StringVar()
        self.data_type.set("salary")
        
        self.radio_salary = tk.Radiobutton(root, text="Salary", variable=self.data_type, value="salary")
        self.radio_salary.pack(pady=5)
        
        self.radio_gdp = tk.Radiobutton(root, text="GDP", variable=self.data_type, value="gdp")
        self.radio_gdp.pack(pady=5)
        
        self.button = tk.Button(root, text="Load Data", command=self.load_data)
        self.button.pack(pady=20)

        self.tree = None
        
    def load_data(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            main(self.data_type.get(), file_path, self.display_data)
    
    def display_data(self, data):
        if self.tree:
            self.tree.destroy()
        
        self.tree = ttk.Treeview(self.root)
        self.tree.pack(pady=20)
        
        self.tree["columns"] = list(data.columns)
        self.tree["show"] = "headings"
        
        for column in data.columns:
            self.tree.heading(column, text=column)
            self.tree.column(column, anchor="center")
        
        for _, row in data.iterrows():
            self.tree.insert("", "end", values=list(row))

def main(data_type: str, file_path: str, display_callback):
    factory = DataFactory(data_type)
    
    # Загрузка данных
    loader = factory.get_loader()
    data = loader.load_data(file_path)

    display_callback(data)
    
    # Анализ данных
    analyzer = factory.get_analyzer(data)
    analyzed_data = analyzer.analyze()
    
    if data_type == 'salary':
        # Вычисление максимального и минимального процента роста/падения для зарплат
        max_growth_men, min_growth_men, max_growth_women, min_growth_women = analyzer.calculate_growth()
        messagebox.showinfo("Growth Info", f"Максимальный процент роста у мужчин: {max_growth_men}\n"
                                           f"Минимальный процент падения у мужчин: {min_growth_men}\n"
                                           f"Максимальный процент роста у женщин: {max_growth_women}\n"
                                           f"Минимальный процент падения у женщин: {min_growth_women}")
    
    # Визуализация данных
    visualizer = factory.get_visualizer(analyzed_data)
    visualizer.visualize()
    
    # Прогнозирование
    forecast_model = factory.get_forecast_model(analyzed_data)
    forecast = forecast_model.forecast(5)  # Прогноз на 5 лет
    
    # Визуализация прогноза
    if data_type == 'salary':
        plt.figure(figsize=(10, 5))
        plt.plot(analyzed_data['Year'], analyzed_data['Median Salary Men'], label='Actual Salary Men')
        plt.plot(analyzed_data['Year'], analyzed_data['Median Salary Women'], label='Actual Salary Women')
        plt.plot(forecast['Year'], forecast['Salary Forecast Men'], label='Forecast Salary Men', linestyle='--')
        plt.plot(forecast['Year'], forecast['Salary Forecast Women'], label='Forecast Salary Women', linestyle='--')
        plt.title('Median Salary Forecast')
        plt.xlabel('Year')
        plt.ylabel('Salary')
        plt.legend()
        plt.show()
    elif data_type == 'gdp':
        plt.figure(figsize=(10, 5))
        plt.plot(analyzed_data['Year'], analyzed_data['GDP'], label='Actual GDP')
        plt.plot(forecast['Year'], forecast['GDP Forecast'], label='Forecast GDP', linestyle='--')
        plt.title('GDP Forecast')
        plt.xlabel('Year')
        plt.ylabel('GDP')
        plt.legend()
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()