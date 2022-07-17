#-------------------------------------------------------------------------------
# Name:        bluefruit_rename
# Purpose:     Allows renaming a batch of Adafruit Bluefruit LE UART Modules
#
# Author:      Andrew A. Katz
#
# Created:     14/07/2022
# Copyright:   (c) Andrew A. Katz 2022
# Copyright:   (c) University of Pennsylvania
# Licence:     MIT
#-------------------------------------------------------------------------------
import serial
from time import sleep
import sys

serial_port = 'COM5' # Set the serial port to the FTDI Cable here. COM5 worked on my PC but it will vary system to system.
name_prefix = 'BLEFriend' # Set the prefix of the Bluefruit name here (Comes before the number)
start = 1 # Starting number for the batch of bluefruits
end = -1 # Number of the last bluefruit. If smaller than start, the script will continue until CRTL+C

def main():
    num = start
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.port = serial_port
    ser.rtscts = True
    ser.xonxoff = False
    ser.open()
    ser.timeout=1
    try:
        while ((end < 0) or (num <= end)):
            a = input(f"Press Enter to program Module {num} (or enter a number manually to program that specific module number)>")
            if(a != ''):
                num = int(a)
            print(ser.read_all())
            ser.write(f'AT+GAPDEVNAME\r\n'.encode())
            ser.flush()

            print(f'{ser.readline()}\n{ser.readline()}\n{ser.readline()}')
            ser.write(f'AT+GAPDEVNAME={name_prefix} {num}\r\n'.encode())
            ser.flush()
            print(f'{ser.readline()}\n{ser.readline()}\n')
            sleep(1)
            num += 1
    except KeyboardInterrupt:
        ser.flush()
        ser.close()
        sys.exit()


if __name__ == '__main__':
    main()
