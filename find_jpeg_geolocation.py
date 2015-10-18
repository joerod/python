"""
Created on Mon Oct 12 10:55:36 2015

@author: joerod
"""

import pexif, os, json, urllib2
#from pprint import pprint

workingdir = "/Users/joerod/Pictures"
key = ''

for file in os.listdir(workingdir):
    if file.endswith(".JPG"):
        lat_log = (pexif.JpegFile.fromFile(workingdir + "/" + file)).get_geo()
        lat_log = str(lat_log).replace('(','').replace(')','')
        url = "https://maps.googleapis.com/maps/api/geocode/json?latlng={0}&key={1}".format(lat_log,key).replace(" ","")
        data = json.load(urllib2.urlopen(url))
        #print urlobj
        print data['results'][0]['formatted_address']
    
  
