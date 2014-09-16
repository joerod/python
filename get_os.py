#Simple Script I wrote to fetch the OS versions on a list of hostnames.  The script uses ssh to log into the unix boxes and wmi
# to get info on a Windows box. 

import wmi
import paramiko

with open('C:\\Users\\jorodriguez\\Desktop\\hosts.txt', 'r') as hostname:

 for computer in hostname:
    try:
        #gets OS version on Linux boxes
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(computer.strip(), username='joroadmin', password='foo')
        stdin, stdout, stderr = client.exec_command('cat /etc/redhat-release')
        OS = stdout.readlines()
        print computer.strip(), "-", ''.join([item.rstrip('\n') for item in OS])


    except:
           #gets OS version on Windows boxes
           c = wmi.WMI(computer.strip())
           for win in c.Win32_OperatingSystem():
             print computer.strip(), '-', win.Caption
