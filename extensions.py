import json
import requests
from config import exchanges


class APIException(Exception):
    pass


class Converter_Values:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            quote_key = exchanges[quote.lower()]
        except KeyError:
            raise APIException(f"Валюта {quote} не найдена!")

        if base_key == quote_key:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}!')


        url = f"https://api.apilayer.com/currency_data/convert?to={quote_key}&from={base_key}&amount={amount}"

        payload = {}
        headers = {
            "apikey": "GxIi3mQdFDGwzfnSGBxooCkoAnDuUgxX"
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        status_code = response.status_code
        result = response.text

        result_dict = json.loads(result)

        new_price = result_dict['result'] * amount
        new_price = round(new_price, 3)
        message = f"Цена {amount} {base} в {quote} : {new_price} {quote_key}"
        return message
