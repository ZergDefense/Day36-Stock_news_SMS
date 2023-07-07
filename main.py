import os
import datetime
from twilio.rest import Client
import requests

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

NEWS_API_KEY = os.environ['NEWS_API_KEY']

account_sid = os.environ['TWILIO_SID']
auth_token = os.environ['TWILIO_TOKEN']

## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

# TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]

STOCK_API_KEY = os.environ['STOCK_API_KEY']

parameters = {
    "function": "TIME_SERIES_INTRADAY",
    "symbol": STOCK_NAME,
    "interval": "60min",
    "apikey": STOCK_API_KEY
}

response = requests.get(STOCK_ENDPOINT, params=parameters)
response.raise_for_status()
data = response.json()
yesterday_closing_price = 0

yesterday_closing_date_time = (str(datetime.datetime.today() - datetime.timedelta(days=1)).split(" "))[0] + " 16:00:00"

for time_series in data["Time Series (60min)"].items():
    if time_series[0] == yesterday_closing_date_time:
        print(time_series)
        yesterday_closing_price = float(time_series[1]["4. close"])

print(yesterday_closing_price)

# TODO 2. - Get the day before yesterday's closing stock price

day_before_yesterday_closing_price = 0
day_before_yesterday_closing_date_time = (str(datetime.datetime.today() - datetime.timedelta(days=2)).split(" "))[
                                             0] + " 16:00:00"
for time_series in data["Time Series (60min)"].items():
    if time_series[0] == day_before_yesterday_closing_date_time:
        day_before_yesterday_closing_price = float(time_series[1]["4. close"])

print(day_before_yesterday_closing_price)

# TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference = round(abs(yesterday_closing_price - day_before_yesterday_closing_price), 2)
print(difference)

# TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
percentage_difference = round(difference / yesterday_closing_price * 100, 2)
print(percentage_difference)

# TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").

## STEP 2: https://newsapi.org/
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

# TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.

yesterday_closing_date = (str(datetime.datetime.today() - datetime.timedelta(days=1)).split(" "))[0]

news_parameters = {
    "qInTitle": "tesla",
    "apiKey": NEWS_API_KEY
}

articles = []


def get_news():
    news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"]
    return news_data


if percentage_difference > 1:
    articles = get_news()

    # TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation

    three_articles = articles[:3]
    print(three_articles)

    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    # to send a separate message with each article's title and description to your phone number.

    client = Client(account_sid, auth_token)
    for index in range(3):
        message = client.messages \
            .create(
            body=f"{three_articles[index]['title']}:\n\n{three_articles[index]['description']}",
            from_=os.environ['FROM_PHONE_NUMBER'],
            to=os.environ['TO_PHONE_NUMBER']
        )
        print(message.status)

# TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.

# TODO 9. - Send each article as a separate message via Twilio.


# Optional TODO: Format the message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
