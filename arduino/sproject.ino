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
    Serial.println();
    Serial.println();

    accelgyro.initialize();
    accelgyro.setXAccelOffset(-4783);
    accelgyro.setYAccelOffset(-1120);
    accelgyro.setZAccelOffset(1164);
    accelgyro.setXGyroOffset(58);
    accelgyro.setYGyroOffset(-40);
    accelgyro.setZGyroOffset(-39);

    SerialGPS.begin(9600);
    Serial.println("Waiting for GPS time ... ");
    while (1)
    {
        while (SerialGPS.available())
        {
            if (gps.encode(SerialGPS.read()))   // process gps messages
            {
                // when TinyGPS reports new data...

                // read datetime
                gps.crack_datetime(&Year, &Month, &Day, &Hour, &Minute, &Second, &Hundredths, &age);
                // read position
                gps.f_get_position(&flat, &flon, &age);

                if (age < 500)
                {
                    // set the Time to the latest GPS reading
                    setTime(Hour, Minute, Second, Day, Month, Year);
                    adjustTime(offset * SECS_PER_HOUR);
                }
            }
        }
        if (timeStatus() != timeNotSet)
        {
            // datetime
            // %Y-%m-%dT%H:%M:%S.%f
            char date_time[100];
            sprintf(date_time, "%02d-%02d-%02dT%02d:%02d:%02d,",
                    year(), month(), day(),
                    hour(), minute(), second()
                   );

            // position latitude
            char flat_string[100];
            dtostrf(flat, 3, 6, flat_string);
            strcat(flat_string, ","); // add a colon for CSV format

            // position longitude
            char flon_string[100];
            dtostrf(flon, 3, 6, flon_string);

            String position = "++";
            position += date_time;
            position += flat_string;
            position += flon_string;
            Serial.println(position);
            break;
        }
    }
}


void loop()
{
    currentTime = millis();
    if (currentTime - startTime >= 1000)
    {
        while (SerialGPS.available())
        {
            if (gps.encode(SerialGPS.read()))    // process gps messages
            {
                // when TinyGPS reports new data...
                // read datetime
                gps.crack_datetime(&Year, &Month, &Day, &Hour, &Minute, &Second, &Hundredths, &age);
                // read position
                gps.f_get_position(&flat, &flon, &age);

                // reset time
                startTime = millis();

                if (age < 500)
                {
                    // set the Time to the latest GPS reading
                    setTime(Hour, Minute, Second, Day, Month, Year);
                    adjustTime(offset * SECS_PER_HOUR);
                }

                // datetime
                // %Y-%m-%dT%H:%M:%S.%f
                char date_time[100];
                sprintf(date_time, "%02d-%02d-%02dT%02d:%02d:%02d,",
                        year(), month(), day(),
                        hour(), minute(), second()
                       );

                // position latitude
                char flat_string[100];
                dtostrf(flat, 3, 6, flat_string);
                strcat(flat_string, ","); // add a colon for CSV format

                // position longitude
                char flon_string[100];
                dtostrf(flon, 3, 6, flon_string);

                String position = "++";
                position += date_time;
                position += flat_string;
                position += flon_string;
                Serial.println(position);

            }
        }
    }

    // read imu
    accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);


    // IMU
    char imu_string[100];
    sprintf(imu_string, "%d,%d,%d,%d,%d,%d",
            ax, ay, az,
            gx, gy, gz
           );

    Serial.println(imu_string);

    // Serial.println("--- end loop ---");

}
