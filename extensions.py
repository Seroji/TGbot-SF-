import json
import requests
from config import currencies


class APIException(Exception):
    pass


class Converting:
    @staticmethod
    def checking(values):
        if len(values) != 3:
            raise APIException("Введено недопустимое количество слов!")

        base, quote, amount = values

        if quote == base:
            raise APIException(f"Невозможно перевести две одинаковые валюты: {base}!")

        try:
            a = currencies[base]
        except KeyError:
            raise APIException(f"Невозможно обработать валюту: {base}!")

        try:
            b = currencies[quote]
        except KeyError:
            raise APIException(f"Невозможно обработать валюту: {quote}!")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать количество: {amount}!")

    @staticmethod
    def get_price(base, quote, amount):
        data = requests.get(f"https://v6.exchangerate-api.com/v6/9a04811013f55681e16b5ae6/pair/{currencies[base]}/"
                            f"{currencies[quote]}/{amount}")
        count = json.loads(data.content)['conversion_rate']
        total_count = json.loads(data.content)['conversion_result']
        text = f"Вы переводите {currencies[base]} в {currencies[quote]} в количестве {amount}." \
               f"\nСтоимость одного {currencies[base]}: {count} {currencies[quote]}." \
               f"\nОбщая сумма: {total_count} {currencies[quote]}"
        return text
