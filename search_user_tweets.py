"""
A Twitter dev account is needed for this 
https://developer.twitter.com/en/apply-for-access

Usage: 
id = "joerodr"
search_tweets(api,id,items,search_term) 

Parameters:	
api – Authentication to the twitter API
id – twitter handle to search
search_term – String to search for in tweet
Return type:	
string of tweets
"""

import tweepy

auth = tweepy.OAuthHandler('', '')
auth.set_access_token('', '')
api = tweepy.API(auth)

def user_status_count(api,id):
    # fetching the user 
    user = api.get_user(id) 
    # fetching the statuses_count attribute 
    return user.statuses_count  

def search_tweets(api,id,items,search_term):
    for tweet in tweepy.Cursor(api.user_timeline, id=id).items(items):
        if search_term in tweet.text:
            print(tweet.text)      


id = "joerodr"
search_tweets(api,id,user_status_count(api,id),"Awesome")    
