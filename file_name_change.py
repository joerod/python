import os
list = os.listdir("/Users/joerod/Desktop/")
for i in list:
   os.rename('/Users/joerod/Desktop/' + i, '/Users/joerod/Desktop/' + i.title())
