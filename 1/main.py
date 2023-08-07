import random
import json


class City:
    def __init__(self, path_json='population.json'):
        self.path_json = path_json
            

    def __get_data(self, path_json):
        with open(json_file.path_json, "r") as read_file:
            return json.load(read_file)


    def __get_total_population(self, data):
        self.total = 0
        for i in range(0, len(data)):
            self.total += data[i]['population']
        return self.total


    def __get_chance_line (self, data, total):
        self.chance_line = [0]
        for i in range(0, len(data) - 1):
            self.chance_line.append(round(self.chance_line[i] + data[i]['population'] / (total / 100), 1))
        self.chance_line.append(100)
        return self.chance_line


    def __get_city_name(self, chance_line, chance, data):
        for i in range(1, len(chance_line)):
            if chance != 0:
                if chance > chance_line[i-1] and chance <= chance_line[i]:
                    return data[i-1]['name']                    
            else:
                return data[0]['name']


    def random_city(self, chance):
        # Округляем шанс до десятичных знаков и преобразуем значение в интервал от 0.0 до 100.0
        chance = (round(chance, 3))*1000/10
        # Выводим случайное число
        print(chance)
        # Получаем данные из json файла
        data = json_file.__get_data(json_file.path_json)
        # Выводим полученные данные из json файла
        print(data)
        # Считаем общую популяцию всех городов
        total = json_file.__get_total_population(data)
        # Выводим общую популяцию
        print(total)
        # Получаем интервалы вероятностей
        chance_line = json_file.__get_chance_line(data, total)
        # Получаем название города и выводим его название
        print(json_file.__get_city_name(chance_line, chance, data))


# Создаем объект класса
json_file = City('population.json')
# Вызываем метод, который выводит название города, исходя из вероятности
json_file.random_city(random.random())
