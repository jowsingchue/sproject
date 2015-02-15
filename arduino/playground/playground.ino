// GPS ---------------
#include <Time.h>
#include <TinyGPS.h>
#include <SoftwareSerial.h>
SoftwareSerial SerialGPS = SoftwareSerial(7, 6);  // receive on pin 7
// Offset hours from gps time (UTC)
const int offset = 7;  // Bangkok Thailand
// variables
time_t prevDisplay = 0; // when the digital clock was displayed
TinyGPS gps;
float flat, flon;
unsigned long age;
int Year;
byte Month, Day, Hour, Minute, Second, Hundredths;

// IMU -----------------
#include <I2Cdev.h>
#include <MPU6050.h>
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
#include <Wire.h>
#endif
// variables
MPU6050 accelgyro;
int16_t ax, ay, az;
int16_t gx, gy, gz;

// SD -------------------
#include <SD.h>
const int chipSelect = 4;
// variables
char dirName[12];
char fileName[12];
char fileLocation[30];
long startTime = 0;
long currentTime = 1000;


void setup()
{
    Serial.begin(115200);
    while (!Serial) ; // Needed for Leonardo only


}

void loop()
{
    Serial.println(millis());
    delay(1000);
}
