__author__ = 'joerod'
#This will rename all files in the folder path to their date in format m/d/y h:m:s
#todo: use curent files extenstion rather then .jpg for all images

import os.path, time

path = '/Users/joerod/Desktop/picture frame'

print "Renaming files in %s" %path

for i in os.listdir(path):
    old =  path + "/" + i
    new = time.strftime('%m-%d-%Y %H:%M:%S', time.gmtime(os.path.getmtime(old)))
    new = path + "/" + new + ".jpg"
    print "Working on %s" %i
    os.rename(old, new)
