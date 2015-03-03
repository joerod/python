author__ = 'joerod'

import subprocess,os

path = '/tmp/files'
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
        print ('There is a file open')
        print (output)
