#This script gets data from the serial device (Adruino) then updates a file/sends and email/posts tweet of the current temp
#Where the website known as joerod.com lives.  Updates every hour

__author__ = 'joerod'
import serial,time,smtplib,tweepy
from time import strftime


ser = serial.Serial('/dev/tty.usbmodem5d11', 9600)
while True:
    print ser.readline()
    with open('/Volumes/JoeRod/joerod/Desktop/temp.txt', 'w') as f:
      f.write(ser.readline())

    #sends email
    fromaddr = 'acropolis21284e@gmail.com'
    toaddrs  = 'joerod@gmail.com'
    subject = 'The temperature is currently %s' %(ser.readline())
    text =  'Temperature was taken at %s' % (strftime("%m/%d/%Y %H:%M"))
    msg = 'From: Temperature@gmail.com\nSubject: %s\n\n%s' % (subject,text)


    # Credentials (if needed)
    username = 'acropolis21284e@gmail.com'
    password = 'Password1'

     # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail(fromaddr, toaddrs, msg)
    server.quit()


    #sends tweet with temperature
    #enter the corresponding information from your Twitter application:
    CONSUMER_KEY = ''#keep the quotes, replace this with your consumer key
    CONSUMER_SECRET = ''#keep the quotes, replace this with your consumer secret key
    ACCESS_KEY = ''#keep the quotes, replace this with your access token
    ACCESS_SECRET = ''#keep the quotes, replace this with your access token secret
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    api.update_status(subject)

    #Waits an hour before resending info
    time.sleep(3600)
