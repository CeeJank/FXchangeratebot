import os
import requests
from dotenv import load_dotenv

load_dotenv()

ratetoken = os.environ.get("EXCHANGERATE_API")

def pairCur(cur1, cur2):
    url = f'https://v6.exchangerate-api.com/v6/{ratetoken}/pair/{cur1}/{cur2}'
    response = requests.get(url)
    data = response.json()
    exchangeRate = [*data["conversion_rates"].values()]
    return exchangeRate

def getRates():
    url = f'https://v6.exchangerate-api.com/v6/{ratetoken}/latest/USD'
    response = requests.get(url)
    currency_sheet = response.json()
    return currency_sheet



# generate most commonly used currencies
def commonCurrencies():
    currency = ["USD", "EUR", "JPY", "GBP", "AUD"]
    return currency

def moreCurrencies():
    dict = getRates()
    more = [*dict["conversion_rates"].keys()]
    return more




