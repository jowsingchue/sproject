/*
 * TimeGPS.pde
 * example code illustrating time synced from a GPS
 *
 */

#include <Time.h>
#include <TinyGPS.h>       // http://arduiniana.org/libraries/TinyGPS/
#include <SoftwareSerial.h>
// TinyGPS and SoftwareSerial libraries are the work of Mikal Hart

SoftwareSerial SerialGPS = SoftwareSerial(7, 6);  // receive on pin 4
TinyGPS gps;

// To use a hardware serial port, which is far more efficient than
// SoftwareSerial, uncomment this line and remove SoftwareSerial
//#define SerialGPS Serial1

// Offset hours from gps time (UTC)
// const int offset = 1;   // Central European Time
//const int offset = -5;  // Eastern Standard Time (USA)
//const int offset = -4;  // Eastern Daylight Time (USA)
//const int offset = -8;  // Pacific Standard Time (USA)
//const int offset = -7;  // Pacific Daylight Time (USA)
const int offset = 7;  // Bangkok Thailand

// Ideally, it should be possible to learn the time zone
// based on the GPS position data.  However, that would
// require a complex library, probably incorporating some
// sort of database using Eric Muller's time zone shape
// maps, at http://efele.net/maps/tz/

time_t prevMillis = 0; // when the digital clock was displayed

// Global Variables
float flat, flon;

void setup()
{
    Serial.begin(115200);
    while (!Serial) ; // Needed for Leonardo only
    SerialGPS.begin(9600);
    Serial.println("Waiting for GPS time ... ");
}

void loop()
{
    while (SerialGPS.available())
    {
        if (gps.encode(SerialGPS.read()))   // process gps messages
        {
            // when TinyGPS reports new data...
            unsigned long age;
            int Year;
            byte Month, Day, Hour, Minute, Second;

            // read datetime
            gps.crack_datetime(&Year, &Month, &Day, &Hour, &Minute, &Second, NULL, &age);
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
        // now() != prevDisplay
        // millis() - prevMillis >= 200
        if (millis() - prevMillis >= 200)   //update the display only if the time has changed
        {
            prevMillis = millis();
            // datetime
            char date_time[100];
            sprintf(date_time, "%02d/%02d/%02d,%02d:%02d:%02d:%03d ",
                    year(), month(), day(),
                    hour(), minute(), second(), prevMillis%1000
                   );
            // latitude
            char flat_string[100];
            dtostrf(flat, 3, 6, flat_string);
            // longitude
            char flon_string[100];
            dtostrf(flon, 3, 6, flon_string);

            Serial.println(date_time);
            Serial.println(flat_string);
            Serial.println(flon_string);

            Serial.println("--- end loop ---");
        }
    }


}
