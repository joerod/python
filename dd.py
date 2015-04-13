__author__ = 'joerod'

import datetime,time,os,subprocess,zipfile,shutil

pattern = '%Y-%d-%m'
source = '/tmp/files'
destination = '/tmp/files/move'

#finds delta time between today and 7 years from now
now_plus = ((datetime.datetime.now()) + datetime.timedelta(7*365)).strftime(pattern)
#converts date to epoch time
epoch = int(time.mktime(time.strptime(now_plus,pattern)))

#gives full path of files in folder
#loops through files and sets A time
for file in ([os.path.join(source,fn)for fn in next(os.walk(source))[2]]):

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
        print ("Working on %s" %file)
        #sets A time, changes file name to date, zips file, and sends to DD
        #zip
        zipname = file + '_' +datetime.datetime.now().strftime('%m-%d-%Y') +'.zip'
        zip = zipfile.ZipFile(zipname, 'w')
        zip.write(file)
        zip.close()
        #sets A time
        os.utime(zipname,(time.time(),epoch))
        #sends to folder
        shutil.move(zipname, destination )
