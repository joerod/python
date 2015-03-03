__author__ = 'joerod'

import subprocess

openfiles = subprocess.Popen(['lsof'],
                             stdout=subprocess.PIPE)
grep = subprocess.Popen(['grep', 'read.txt'],
                        stdin=openfiles.stdout,
                        stdout=subprocess.PIPE
                        )
openfiles.stdout.close()
output =  grep.communicate()[0]

if output != '':
    print 'There is a file open'
    print output
