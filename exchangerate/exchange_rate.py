import os
import requests
from dotenv import load_dotenv

load_dotenv()

ratetoken = os.environ.get("EXCHANGERATE_API")

def getRates():
    url = f'https://v6.exchangerate-api.com/v6/{ratetoken}/latest/USD'
    response = requests.get(url)
    data = response.json()
    print(data)


