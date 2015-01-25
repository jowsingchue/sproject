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
byte Month, Day, Hour, Minute, Second;

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


void setup()
{
    Serial.begin(115200);
    while (!Serial) ; // Needed for Leonardo only
    SerialGPS.begin(9600);
    
    Serial.println();
    Serial.println();
    Serial.println("--- Start ---");
    Serial.print("Initializing SD card...");
    // make sure that the default chip select pin is set to
    // output, even if you don't use it:
    pinMode(10, OUTPUT);

    // see if the card is present and can be initialized:
    if (!SD.begin(chipSelect))
    {
        Serial.println("Card failed, or not present");
        // don't do anything more:
        return;
    }
    Serial.println("card initialized.");

    Serial.println("Waiting for GPS time ... ");
    do
    {
        if (gps.encode(SerialGPS.read()))   // process gps messages
        {
            // when TinyGPS reports new data...

            // read datetime
            gps.crack_datetime(&Year, &Month, &Day, &Hour, &Minute, &Second, NULL, &age);

            if (age < 500)
            {
                // set the Time to the latest GPS reading
                setTime(Hour, Minute, Second, Day, Month, Year);
                adjustTime(offset * SECS_PER_HOUR);
            }
        }
    } while (timeStatus() == timeNotSet);

    sprintf(dirName, "%04d%02d%02d",
            Year, Month, Day
           );
    if(SD.exists(dirName))
    {
        Serial.print("dir_name: ");
        Serial.print(dirName);
        Serial.println(" already exists.");
    } else {
        SD.mkdir(dirName);
        Serial.print("dir_name: ");
        Serial.print(dirName);
        Serial.println(" created.");
    }

    sprintf(fileName, "%02d%02d%02d.log",
            Hour, Minute, Second
           );
    Serial.print("File name is: ");
    Serial.println(fileName);

    strcpy(fileLocation, dirName);
    strcat(fileLocation, "/");
    strcat(fileLocation, fileName);

    Serial.print("Data will be write to: ");
    Serial.println(fileLocation);

    Serial.println("--- Done Initialization ---");
}

void loop()
{
    while (SerialGPS.available())
    {
        if (gps.encode(SerialGPS.read()))   // process gps messages
        {
            // when TinyGPS reports new data...
            // read datetime
            gps.crack_datetime(&Year, &Month, &Day, &Hour, &Minute, &Second, NULL, &age);
            // read position
            gps.f_get_position(&flat, &flon, &age);
            // read imu
            accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

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
        if (now() != prevDisplay)   //update the display only if the time has changed
        {
            prevDisplay = now();

            // datetime
            char date_time[100];
            sprintf(date_time, "%02d-%02d-%02d,%02d:%02d:%02d,",
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
            strcat(flon_string, ","); // add a colon for CSV format

            // IMU
            char imu_string[100];
            sprintf(imu_string, "%d,%d,%d,%d,%d,%d",
                    ax, ay, az,
                    gx, gy, gz
                   );

            String dataString = "";
            dataString += date_time;
            dataString += flat_string;
            dataString += flon_string;
            dataString += imu_string;

            File dataFile = SD.open(fileLocation, FILE_WRITE);
            // if the file is available, write to it:
            if (dataFile)
            {
                dataFile.println(dataString);
                dataFile.close();
                // print to the serial port too:
                Serial.print("Data written: ");
                Serial.println(dataString);
            }
            // if the file isn't open, pop up an error:
            else
            {
                Serial.print("error opening ");
                Serial.println(fileLocation);
            }
        }
    }
}