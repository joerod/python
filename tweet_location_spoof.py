import requests
import urllib.parse
import tweepy
import pickle
import os
import argparse

def get_coordinates(address,api_key):
    add_encode = urllib.parse.quote(address)
    try:
        results = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={add_encode}&key={api_key}')
        return (results.json())['results'][0]['geometry']['location']
    except:
        print(errors)
        quit()

def tweet_spoof_location(tweet,lat,long,access_token=None,access_token_secret=None,consumer_key=None,consumer_secret=None,**kwargs):
    if (kwargs):
        kwargs=kwargs['kwargs']
        consumer_key        = kwargs['consumer_key']
        consumer_secret     = kwargs['consumer_secret']
        access_token        = kwargs['access_token']
        access_token_secret = kwargs['access_token_secret']
    elif(not access_token or not access_token_secret or not consumer_key or not consumer_secret): 
        print("Authentication is missing a paramter")
        quit()
    auth = tweepy.OAuth1UserHandler(
        consumer_key, consumer_secret, access_token, access_token_secret
    )
    try:
        api = tweepy.API(auth)
    except: 
        print(error)
        quit()    
    api.update_status(tweet,lat=lat,long=long)

def main():
    parser = argparse.ArgumentParser(
        description="Spoofs a tweet location",
        epilog='python python tweet_location_spoof.py --tweet ''hello from the terminal'' -location ''seatle, washington'' --twitter_pickel ''/home/joerod/twitter.p'' --gmaps_pickel ''/home/joerod/gmaps.p'''
    )
    parser.add_argument("--tweet", required=True, help="")
    parser.add_argument("--location", required=True, help="")
    parser.add_argument("--twitter_pickel",  help="")
    parser.add_argument("--twitter_access_token",  help="")
    parser.add_argument("--twitter_access_token_secret",  help="")
    parser.add_argument("--twitter_consumer_key",  help="")
    parser.add_argument("--twitter_consumer_secret",  help="")
    parser.add_argument("--gmaps_key",  help="")
    parser.add_argument("--gmaps_pickel",  help="")
    args = parser.parse_args()

    if(args.twitter_pickel):
        if os.path.exists(args.twitter_pickel):
            with open(args.twitter_pickel, 'rb') as token:
                twitter  = pickle.load(token)
        else:
            print(f"{args.twitter_pickel}: Does not exist") 
            quit()
    if(args.gmaps_pickel):
        if os.path.exists(args.gmaps_pickel):
            with open(args.gmaps_pickel, 'rb') as token:
                gmaps_key  = (pickle.load(token))['api']
        else:
            print(f"{args.gmaps_pickel}: Does not exist") 
            quit()
            
    coord = get_coordinates(args.location,gmaps_key)
    if(args.twitter_pickel):
        tweet_spoof_location(args.tweet,coord['lat'],coord['lng'],kwargs=twitter)
    else:
        tweet_spoof_location(args.tweet,coord['lat'],coord['lng'],args.twitter_access_token,args.twitter_access_token_secret,args.twitter_consumer_key,args.twitter_consumer_secret) 

if __name__ == "__main__":
    main()
