#Simple Script I wrote to fetch the OS versions on a list of hostnames.  The script uses ssh to log into the unix boxes and wmi
# to get info on a Windows box. 

import wmi
import paramiko

hostname = ['linuxbox','windowsbox','linuxbox2']

for computer in hostname:
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(computer, username='linuxaccout', password='foo')
        stdin, stdout, stderr = client.exec_command('cat /etc/redhat-release')
        OS = stdout.readlines()
        print computer, "-", ''.join([item.rstrip('\n') for item in OS])


    except:
           c = wmi.WMI(computer)
           for win in c.Win32_OperatingSystem():
             print computer, '-', win.Caption
