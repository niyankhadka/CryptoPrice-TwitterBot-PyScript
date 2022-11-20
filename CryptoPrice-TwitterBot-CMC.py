# -------------------------------------
# Program Starts from here
# ------------------------------------- 
import os
import tweepy
import configparser
import pandas as pd
from requests import Request, Session
import json
import pprint
import time
from numerize import numerize



# -------------------------------------------------------
# Extracting info
# -------------------------------------------------------



def getInfo( key ) :

    # read configs
    config = configparser.ConfigParser()
    config.read('config.ini')

    url = config['cmc']['api_url'] # Coinmarketcap API url

    parameters = { 'slug': key, 'convert': 'USD' } # API parameters to pass in for retrieving specific cryptocurrency data

    api_key = config['cmc']['api_key']

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key
    } # Replace 'YOUR_API_KEY' with the API key you have recieved

    session = Session()
    session.headers.update(headers)

    response = session.get(url, params=parameters)

    if response:

        info = response.json()
    
    else:

        init_loop = True

        while init_loop:

            time.sleep(1)
            print( "Requesting response......" )
            response = session.get(url, params=parameters)

            if response :

                info = response.json()
                init_loop = False

            else:
                init_loop = True

    return info



# -------------------------------------------------------
# Generating Status
# -------------------------------------------------------



def getStatus( name, symbol, price, m_cap, change_1h, emoji_1h , change_24h, emoji_24h, volume_24h ):

    status = f"{name} #{symbol} Statistics 📊 \n\n Current price is : {price} USD with marketcap of : {m_cap} USD. \n In last 1H, price change in percentage is {change_1h}% {emoji_1h}. \n In 24H time frame, {change_24h}% {emoji_24h}  was change with volume of : {volume_24h} USD. \n\n #{symbol}Price"

    return status



# -------------------------------------------------------
# Twitter Api
# -------------------------------------------------------



def createAPI():

    # read configs
    config = configparser.ConfigParser()
    config.read('config.ini')

    api_key = config['twitter']['api_key']
    api_key_secret = config['twitter']['api_key_secret']

    access_token = config['twitter']['access_token']
    access_token_secret = config['twitter']['access_token_secret']

    # authentication
    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    return api


def tweet(api, message):

    try:
        api.update_status(message)
        print(f'status updated')
    except tweepy.errors.Forbidden:
        print('Can`t tweet message!')



# -------------------------------------------------------
# Run Program
# -------------------------------------------------------


def main():

    query = {
        "bitcoin" : '1',
        "ethereum" : '1027',
        "bnb" : '1839',
        "solana" : '5426',
        "cardano" : '2010',
        "polygon" : '3890',
        "polkadot" : '6636',
        "dogecoin" : '74',
        "xrp" : '52',
        "tron" : '1958'
    }

    api = createAPI()

    for key, value in query.items():

        info = getInfo( key )
        data = info['data'][value]

        name = data['name']
        symbol = data['symbol']
        price = round( data['quote']['USD']['price'], 5 )
        m_cap = numerize.numerize( data['quote']['USD']['market_cap'], 2 )
        change_1h = round( data['quote']['USD']['percent_change_1h'], 2 )
        change_24h = round( data['quote']['USD']['percent_change_24h'], 2 )
        volume_24h = numerize.numerize( data['quote']['USD']['volume_24h'], 2 )

        emoji_1h = "🔴⬇️" if change_1h < 0 else "🟢⬆️"
        emoji_24h = "🔴⬇️" if change_24h < 0 else "🟢⬆️"

        status = getStatus( name, symbol, price, m_cap, change_1h, emoji_1h , change_24h, emoji_24h, volume_24h )

        tweet(api, status)

        time.sleep(1)


if __name__ == '__main__':
    main()



    


	                        




