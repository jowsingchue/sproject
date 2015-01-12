<Project name> eg. rail-vehicle-sensor
===================


## Note for myself
Serial Port: /dev/tty.usbmodem1411


## Equipments

* [Arduino Uno](http://arduino.cc/en/Main/arduinoBoardUno)
* [SD Card](http://www.arduitronics.com/product/210/microsd-card-adapter-v1-1-catalex)
* [MPU-6050](http://playground.arduino.cc/Main/MPU-6050)
* [GY-GPS6MV2 (U-blox NEO 6M GPS)](https://developer.mbed.org/users/edodm85/notebook/gps-u-blox-neo-6m/)


## Wiring

MPU-6050
    INT   -  pin 2 
    SDA   -  pin A4
    SCL   -  pin A5
    VCC   -  5V
    GND   -  GND

GY-GPS6MV2 (U-blox NEO 6M GPS)
    TX (to RX on Arduino) - pin 7
    RX (to TX on Arduino) - pin 6
    VCC   -  5V
    GND   -  GND

SD Card
    MISO  -  pin 12
    MOSI  -  pin 11
    CLK   -  pin 13
    CS    -  pin 4
    VCC   -  5V
    GND   -  GND