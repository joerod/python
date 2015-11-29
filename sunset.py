# -*- coding: utf-8 -*-
"""
This script gets the sunset time for EST time zone
Created on Mon Nov 16 22:34:51 2015
@author: joerod
"""

import json
import urllib2
from dateutil.parser import parse
from datetime import datetime,timedelta

#get sunset from API
data = urllib2.urlopen("http://api.sunrise-sunset.org/json?lat=40.722760&lng=-73.873324&formatted=0")
sunset = json.load(data)
sunset = (sunset['results']['sunset'])
#format time
sunset = parse(sunset)

#Convert form UTC to EST
mytime = datetime.strptime(str(sunset).replace('+00:00',''),"%Y-%m-%d %H:%M:%S")
mytime += timedelta(hours=-5)
print mytime
