#this script searches a directory for jpgs then extracts the geolocation. 

import OS
from pexif import JpegFile

workingdir = '/Users/joerod/Pictures'

for file in os.listdir(workingdir):
    if file.endswith(".JPG"):
        try:
            print(pexif.JpegFile.fromFile(workingdir + "/" + file).get_geo())
        except IOError:
            type, value, traceback = sys.exc_info()
            print >> sys.stderr, "Error opening file:", value
        except JpegFile.NoSection:
            type, value, traceback = sys.exc_info()
            print >> sys.stderr, "Error get GPS info:", value
       except JpegFile.InvalidFile:
           type, value, traceback = sys.exc_info()
           print >> sys.stderr, "Error opening file:", value
    
