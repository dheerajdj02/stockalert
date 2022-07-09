import os

import requests
import telepot as telepot
from datetime import datetime


TOKEN = '5534927645:AAEldiK0AQY-GZtBN3VD2tQbt5ve6WWT2AU'
chat_id = '-1001537732861'
now = datetime.now()
weekday = now.weekday()


class NseIndia:

    def __init__(self):
        self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,like Gecko)'
                                      'Chrome/80.0.3987.149 Safari/537.36', 'accept-language': 'en,gu;q=0.9,hi;q=0.8',
                        'accept-encoding': 'gzip, deflate, br'}
        self.session = requests.Session()
        self.session.get("https://www.nseindia.com/", headers=self.headers)

    def pre_market_data(self):
        keys = ["NIFTY", "BANKNIFTY"]
        for key in keys:
            print(key)
            url = f"https://www.nseindia.com/api/market-data-pre-open?key={key}"
            response = self.session.get(url, headers=self.headers)
            data_value = response.json()["niftyPreopenStatus"]
            print(data_value)
            bot = telepot.Bot(TOKEN)
            message = f"Hey, All!\n\n{key} Market Status ({now.strftime('%d - %B')}):\n\nStatus: {data_value['status']}\n" \
                      f"Last Price: {data_value['lastPrice']}\nChange: {data_value['change']}\npChange: {data_value['pChange']}\n\nThank you!😀"
            bot.sendMessage(chat_id, message)

    def holidays(self):
        holiday_list = []
        holiday = ["clearing", "trading"]
        key = "trading"
        data = self.session.get(f'https://www.nseindia.com/api/holiday-master?type={holiday[holiday.index(key)]}',
                                headers=self.headers).json()
        holidays = data["CBM"]
        for holiday in holidays:
            holiday_list.append(holiday["tradingDate"])
            if datetime.date(datetime.now()) == holiday["tradingDate"]:
                bot = telepot.Bot(TOKEN)
                holiday_message = f"Hey, All! Market is Closed\n\nEnjoy the holiday.\n\nThank you!😀"
                bot.sendMessage(chat_id, holiday_message)
        return holiday_list


nse = NseIndia()



def alert():
    if weekday != 5 and weekday != 6:
        nse.holidays()
    elif weekday == 5 or weekday == 6:
        bot = telepot.Bot(TOKEN)
        holiday_message = f"Hey,All! Market is Closed\n\nEnjoy the holiday.\n\nThank you!😀"
        bot.sendMessage(chat_id, holiday_message)
    else:
        nse.pre_market_data()


alert()
