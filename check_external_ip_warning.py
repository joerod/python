#!/usr/bin/env python

import urllib
import re
import time,smtplib,email.utils
from email.mime.text import MIMEText

#Grabs external ip from site
def get_external_ip():
    site = urllib.urlopen("http://checkip.dyndns.org/").read()
    grab = re.findall('([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', site)
    address = grab[0]
    return address

if __name__ == '__main__':

#checks file for saved IP address to compare with IP from site
  ip_check_file = open('/Users/joerod/Desktop/ip.txt', 'r')

read_ip = file.read(ip_check_file)

#If ip has changed sends email
if get_external_ip() != read_ip:
    subject = 'IP has changed for joerod.com %s' %(get_external_ip())
    #sends email
    text =  'New IP: %s' % (get_external_ip())
    msg = MIMEText(text)
    msg['To'] = email.utils.formataddr(('Joe Rodriguez', 'joerod@gmail.com'))
    msg['From'] = email.utils.formataddr(('JoeRod.com IP Change', 'acropolis21284e@gmail.com'))
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
else:
    print 'All is good!'
    
#check timestamp on file if IP has change and timestamp greater then 2 hours change file to current IP    
