__author__ = 'joerod'
"""I created this script to prepare files to be sent to EMC data domain
"""

import datetime,time,os,subprocess,zipfile

path = '/tmp/files'
pattern = '%Y-%d-%m'

#finds delta time between today and 7 years from now
now_plus = ((datetime.datetime.now()) + datetime.timedelta(7*365)).strftime(pattern)
#converts date to epoch time
epoch = int(time.mktime(time.strptime(now_plus,pattern)))

#gives full path of files in folder
#loops through files and sets A time
for file in ([os.path.join(path,fn)for fn in next(os.walk(path))[2]]):

    openfiles = subprocess.Popen(['/usr/sbin/lsof'],
                             stdout=subprocess.PIPE)
    grep = subprocess.Popen(['grep', file],
                        stdin=openfiles.stdout,
                        stdout=subprocess.PIPE
                        )
    openfiles.stdout.close()
    output =  (grep.communicate()[0]).decode('utf-8')

    if (output != ''):
        print ('%s is open, please close before I can proceed' %file)
        print (output)

    else:
        print ("Doing stuff to %s" %file)
        #sets A time, changes file name to date, zips file, and sends to DD
        os.chdir(path)
        zipname = file + datetime.datetime.now().strftime('%m-%d-%Y') +'.zip'
        zip = zipfile.ZipFile(zipname, 'w')
        zip.write(file)
        zip.close()
        os.utime(zipname,(time.time(),epoch))

