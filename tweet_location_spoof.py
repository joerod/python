import requests
import urllib.parse
import tweepy

def get_coordinates(address,api=''):
    add_encode = urllib.parse.quote(address)
    results = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={add_encode}&key={api}')
    return (results.json())['results'][0]['geometry']['location']

def tweet_spoof_location(tweet,lat,long):
    access_token = ""
    access_token_secret = ""
    consumer_key=""
    consumer_secret=""
    auth = tweepy.OAuth1UserHandler(
        consumer_key, consumer_secret, access_token, access_token_secret
    )
    api = tweepy.API(auth)
    api.update_status(tweet,lat=lat,long=long)

address = 'united center, chicago'   
tweet = 'this is a retest of the tweetbot tweet spoofer'
coord = get_coordinates(address)
tweet_spoof_location(tweet,coord['lat'],coord['lng'])
