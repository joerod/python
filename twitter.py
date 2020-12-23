import tweepy

auth = tweepy.OAuthHandler("W6WgZsMjzzADqhNbsanm06fuL", "ZZbvZH7CsuawRB8GSmQ5BN1MhFBbIOKBd9aTbI0AlPbxxOlcLQ")
auth.set_access_token("14146231-fRVDfh7Ig596P28pe76sVPoL6ic3SvNr1VvLiThzF", "kdOhJwfu898KJmioihTAClFxuPPxALpa7Gbe7sbgzkhbd")

api = tweepy.API(auth)

for status in tweepy.Cursor(api.home_timeline).items(200):
    # Process the status here
    process_status(status)    


    api.update_profile_background_image(/home/joerod/Desktop/800px-Lower_Manhattan_skyline_-_June_2017.jpg)