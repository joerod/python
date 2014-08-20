import os
path = "/Users/joerod/Desktop/"
list = os.listdir(path)
os.chdir(path)
for i in list:
   os.rename(i, i.title())
