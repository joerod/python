__author__ = 'joerod'

#!/usr/bin/env python

import urllib,re,smtplib,email.utils,os.path,datetime
from email.mime.text import MIMEText

#Grabs external ip from site
file_path = '/Users/joerod/Desktop/ip.txt'
d = datetime.datetime.now()

def get_external_ip():
    site = urllib.urlopen("http://checkip.dyndns.org/").read()
    grab = re.findall('([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)', site)
    address = grab[0]
    return address
if __name__ == '__main__':
    #checks file for saved IP address to compare with IP from site
    #If ip has changed sends email
    if get_external_ip().strip() != file.read(open(file_path, 'r')).strip():
        print "We gotta problem!"
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
        print "All is good! %s" %d.strftime("%m-%d-%Y %H:%M:%S")

    #if current time is +1 hours from last write time of file and if IP does not match file, write to file

filetime = os.path.getmtime(file_path)

if filetime > (filetime - 3600) and get_external_ip().strip() != file.read(open(file_path, 'r')).strip():
    print "Updating %s with new IP" %file_path
    fn = (open(file_path, 'w'))
    fn.write(get_external_ip())
    fn.close()
