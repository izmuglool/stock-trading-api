import pip
import requests
import datetime as dt
import os
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla"
PRICE_API_KEY = "5HNPUSPXQTE2CU6Y"
TWILIO_ACCOUNT_SID = "AC1fda313a752838ef067ca650b0d07778"
TWILIO_AUTH_TOKEN = "42e34b761612436038c319f058680000"
MY_NUMBER = "+923555724968"
TWILLIO_NUMBER = "+12056496992"
NEWS_API_KEY = "34a1ac2d5fb7461ab4bddcd439cc81e3"
PRICE_API_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_API_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_PARAMETERS = {
    "apiKey": NEWS_API_KEY,
    "q": COMPANY_NAME,
    "pageSize": 3,
    "sortBy": "publishedAt",
    "language": "en"
}
PRICE_PARAMETERS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize": "compact",
    "apikey": PRICE_API_KEY
}

yesterday = dt.date.today() - dt.timedelta(days=1)
day_before_yesterday = yesterday - dt.timedelta(days=1)

def check_days():
    global yesterday, day_before_yesterday
    if yesterday.weekday() == 7:
        yesterday = dt.date.today() - dt.timedelta(days=3)
        day_before_yesterday = yesterday - dt.timedelta(days=1)
    elif yesterday.weekday() == 6:
        yesterday = dt.date.today() - dt.timedelta(days=2)
        day_before_yesterday = yesterday - dt.timedelta(days=1)
    elif yesterday.weekday() == 1:
        day_before_yesterday = yesterday - dt.timedelta(days=3)
    

check_days()
    
## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

price_request = requests.get(url=PRICE_API_ENDPOINT, params=PRICE_PARAMETERS)
price_data = price_request.json()

try:
    yesterday_price = price_data["Time Series (Daily)"][str(yesterday)]["1. open"]
    day_before_yesterday_price = price_data["Time Series (Daily)"][str(day_before_yesterday)]["1. open"]
except KeyError:
    yesterday = dt.date.today() - dt.timedelta(days=2)
    day_before_yesterday = yesterday - dt.timedelta(days=1)
else:
    check_days()

price_difference = (float(yesterday_price) / float(day_before_yesterday_price)) * 100 - 100
if day_before_yesterday_price > yesterday_price:
    price_difference *= -1

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

news_request = requests.get(url=NEWS_API_ENDPOINT, params=NEWS_PARAMETERS)
news_data = news_request.json()

Article_1 = f"Headline: {news_data['articles'][0]['title']}\nDescription: {news_data['articles'][0]['description']}"
Article_2 = f"Headline: {news_data['articles'][1]['title']}\nDescription: {news_data['articles'][1]['description']}"
Article_3 = f"Headline: {news_data['articles'][2]['title']}\nDescription: {news_data['articles'][2]['description']}"
## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 

MESSAGE = f"TSLA: {price_difference}% change\n\n{Article_1}\n\n{Article_2}\n\n{Article_3}"

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

message = client.messages \
    .create(
         body=MESSAGE,
         from_=TWILLIO_NUMBER,
         to=MY_NUMBER
     )

#Optional: Format the SMS message like this:


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure

# account_sid = os.environ[TWILIO_ACCOUNT_SID]
# auth_token = os.environ[TWILIO_AUTH_TOKEN]

print(message.status)
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

