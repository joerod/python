__author__ = 'joerod'

import datetime
import time
import os

path = '/tmp/files'
pattern = '%Y-%d-%m'

#finds delta time between today and 7 years from now
now_plus = ((datetime.datetime.now()) + datetime.timedelta(7*365)).strftime(pattern)
#converts date to epoch time
epoch = int(time.mktime(time.strptime(now_plus,pattern)))
#gives full path of files in folder

#loops through files and sets A time
for file in ([os.path.join(path,fn)for fn in next(os.walk(path))[2]]):
    print ("Working on %s" %file)
    os.utime(file,(time.time(),epoch))
