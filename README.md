# co2Sensor
howto install use the co2 sensor

hardware
board:
mskezurich with circuitpython

software
circuitpython

raspberry pico is with usb connected

with 
pyserial-miniterm 

shows all connected device 
choose the ttyACME 

it begins to run

program

import time
import board
import adafruit_scd4x
import busio

#i2c = board.I2C()
i2c = busio.I2C(scl=board.GP13, sda=board.GP12)
scd4x = adafruit_scd4x.SCD4X(i2c)
print("Serial number:", [hex(i) for i in scd4x.serial_number])

scd4x.start_periodic_measurement()
print("Waiting for first measurement....")

while True:
    if scd4x.data_ready:
        print("CO2: %d ppm" % scd4x.CO2)
        print("Temperature: %0.1f *C" % scd4x.temperature)
        print("Humidity: %0.1f %%" % scd4x.relative_humidity)
        print()
    time.sleep(1)


explanation todo

use

result
Press any key to enter the REPL. Use CTRL-D to reload.
soft reboot

Auto-reload is on. Simply save files over USB to run them or enter REPL to disable.
code.py output:
␛]0;🐍Wi-Fi: off | code.py | 8.1.0␛\Serial number: ['0x1f', '0x4e', '0x57', '0x7', '0x3b', '0x26']
Waiting for first measurement....
␛]0;🐍Wi-Fi: off | Done | 8.1.0␛\
Code stopped by auto-reload. Reloading soon.
soft reboot

Auto-reload is on. Simply save files over USB to run them or enter REPL to disable.
code.py output:
␛]0;🐍Wi-Fi: off | code.py | 8.1.0␛\Serial number: ['0x1f', '0x4e', '0x57', '0x7', '0x3b', '0x26']
Waiting for first measurement....
CO2: 690 ppm
Temperature: 26.0 *C
Humidity: 30.1 %

CO2: 684 ppm
Temperature: 25.6 *C
Humidity: 30.8 %

CO2: 698 ppm
Temperature: 25.4 *C
Humidity: 31.2 %

CO2: 723 ppm
Temperature: 25.1 *C
Humidity: 32.0 %

CO2: 750 ppm
Temperature: 24.9 *C
Humidity: 32.6 %

CO2: 756 ppm
Temperature: 24.7 *C
Humidity: 32.9 %

...



                            
