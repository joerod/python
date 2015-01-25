__author__ = 'joerod'
import serial,time,smtplib,tweepy,email.utils
from time import strftime
from email.mime.text import MIMEText

ser = serial.Serial('/dev/tty.usbmodem5d11', 9600)
while True:
    print ser.readline()
    with open('/Volumes/JoeRod/joerod/Desktop/temp.txt', 'w') as f:
      f.write(ser.readline())

    subject = 'The temperature is currently %s' %(ser.readline())
    #sends email
    text =  'Temperature was taken at %s' % (strftime("%m/%d/%Y %H:%M"))
    msg = MIMEText(text)
    msg['To'] = email.utils.formataddr(('Joe Rodriguez', 'joerod@gmail.com'))
    msg['From'] = email.utils.formataddr(('JoeRod Temperature', 'acropolis21284e@gmail.com'))
    msg['Subject'] = subject


    # Credentials (if needed)
    username = 'acropolis21284e@gmail.com'
    password = ''

   # The actual mail send
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(username,password)
    server.sendmail('acropolis21284e@gmail.com', ['joerod@gmail.com'], msg.as_string())
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
