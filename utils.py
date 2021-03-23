import requests
import json
from settings import keys,inv_keys,API_KEY

class ConvertException(Exception):
    pass

class CurrencyConvertion:
    @staticmethod
    def convert(base:str, quote:list, amount:str):
        #Количество
        try:
            amount=amount.lower()
            #Если количество не указали
            if amount in keys.values() or amount in keys.keys():
                quote.append(amount)
                amount="1"
            amount = float(amount)
        except ValueError:
            #Пробовал костыли не получилось думаю так сойдет )
            raise ConvertException(f"Не удалось обработать количество : {amount}\nвозможно надо поставить точку\nили ошибка обработки последней валюты")
        #Список конвертации
        try:
            #Обрабатываем спикок конвертируемых валют
            quote_tiker=[]
            for i in quote:
                if i.lower() in keys.values():
                    quote_tiker.append(i.lower())
                elif i.lower() in keys.keys():
                    quote_tiker.append(keys[i.lower()])
            if quote_tiker==[]:
                quote=",".join(quote)
                raise ConvertException(f"Не удалось обработать валюту(ы): {quote}")
            else:
                quote_tiker = list(set(quote_tiker))
                ask_tiker="&base=".join(quote_tiker)
        except KeyError:
            raise ConvertException(f"Не удалось обработать валюту: {quote}")
        # Базовое значение
        try:
            if base.lower() in keys.values():
                base_tiker=base.lower()
            else:
                base_tiker=keys[base.lower()]
        except KeyError:
            raise ConvertException(f"Не удалось обработать Базовую валюту валюту: {base}")
        #Да я тут поменял понятия base и quote, но это мой бот и я предпочел что так удобнее для ряда запросов
        r = requests.get(f"https://www1.oanda.com/rates/api/v2/rates/spot.json?api_key={API_KEY}&base={ask_tiker}&quote={base_tiker}")
        total_base=json.loads(r.content)["quotes"]
        #Применил костыль, возможно надо было просто использовать другой формат строк (, не задумывался об этом и не пробовал (
        tiker_q = "base_currency"
        tiker_b="quote_currency"
        amount_a="ask"
        text = ""
        for i in total_base:
            text += f"{amount} {inv_keys[i[tiker_q].lower()]} в {inv_keys[i[tiker_b].lower()]} ~ {amount*float(i[amount_a]):.02f}\n"
        return text