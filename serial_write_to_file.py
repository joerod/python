# This script connects to my Arduino via the UBS serial port then grabs the data being sent to serial and writes it to a file 
# On my computer.  

__author__ = 'joerod'
import serial

ser = serial.Serial('/dev/tty.usbmodem5d11', 9600)
while True:
    print ser.readline()
    with open('/Volumes/JoeRod/joerod/Desktop/temp.txt', 'w') as f:
      f.write(ser.readline())
