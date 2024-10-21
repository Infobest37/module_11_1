"""Код для получения данных по криптовалюте и прогнозированию """
import requests # для отправки HTTP-запросов и получения данных с API.
import pandas as pd # для работы с табличными данными, их обработки и анализа.
import numpy as np # для математических операций, таких как логарифмы и разности
import matplotlib.pyplot as plt # для построения графиков.


# Класс для получения и обработки данных
class Crypto_Price:
    def __init__(self, name_krypt): # функция принимающая имя криптовалюты, данные которые на данный момент пустые
        self.name_krypt = name_krypt
        self.data = None

    # Функция для получения данных с публичного API
    def fetch_data(self):
        url = f"https://api.coingecko.com/api/v3/coins/{self.name_krypt}/market_chart?vs_currency=usd&days=30"
        response = requests.get(url) # отправляем GET-запрос на сервер для получения данных
        if response.status_code == 200: # Если запрос успешен, данные извлекаются в формате JSON и преобразуются
            # в pandas.DataFrame, который напоминает таблицу в Excel.
            prices = response.json()['prices']
            self.data = pd.DataFrame(prices, columns=['timestamp', 'price']) # pandas.DataFrame используется для
            # хранения данных с двумя колонками: timestamp (время) и price (цена)
            self.data['timestamp'] = pd.to_datetime(self.data['timestamp'], unit='ms') # pd.to_datetime преобразует
            # метки времени (в миллисекундах) в нормальный формат даты и времени.
            print(f"Данные успешно загружены для {self.name_krypt}")
        else:
            print("Ошибка при загрузке данных")

    # Функция для анализа тренда и простого прогнозирования
    def analyze_trend(self):
        if self.data is not None: # Если данные отсутствуют тогда
            self.data['log_price'] = np.log(self.data['price']) # рассчитываем натуральный логарифм цены благодаря
            # библиотеке numpy.
            self.data['return'] = self.data['log_price'].diff() # вычисляем разницу между логарифмами цен и доходностью
            # между данными которая дает нам функция diff() из библиотеки numpy
            print(self.data.describe()) # выводит общие статистические данные по таблице(средние стандартное отклонение)
            print("Анализ тренда выполнен")
        else:
            print("Нет данных для анализа")

    # Функция для построения графиков
    def plot_data(self):
        if self.data is not None:
            plt.figure(figsize=(10, 6)) # создаем основу где будет наноситься наш график
            plt.plot(self.data['timestamp'], self.data['price'], label='Price') # строит глафик согласно которому
            # происходит измененении цены по времени
            plt.title(f'Цены {self.name_krypt} за последние 30 дней') # добовляет заголовок к графику
            plt.xlabel('Дата') # обзывает ось Х
            plt.ylabel('Цена в USD') # обзывает ось У
            plt.legend() # показывает нам что обозначает каждая линия на графике
            plt.show() # самое основное выводит график
        else:
            print("Нет данных для построения графика")


# Самый главный блок который запускает наш класс
if __name__ == "__main__": # это проверка которая позволяет использовать код только если этот файл запускается на
    # прямую, а не импортируется как модуль в другой файл.
    crypto_symbol = 'bitcoin'  # Можно заменить на 'ethereum', 'dogecoin' и т.д.
    predictor = Crypto_Price(crypto_symbol)

    predictor.fetch_data()  # Получаем данные с API
    predictor.analyze_trend()  # Анализируем тренд
    predictor.plot_data()  # Строим график
