// GPS ---------------
#include <Time.h>
#include <TinyGPS.h>
#include <SoftwareSerial.h>

SoftwareSerial SerialGPS = SoftwareSerial(7, 6);  // receive on pin 7

// Offset hours from gps time (UTC)
const int offset = 7;  // Bangkok Thailand
time_t prevDisplay = 0; // when the digital clock was displayed

// Global Variables -------------
TinyGPS gps;
unsigned long age;
int Year;
byte Month, Day, Hour, Minute, Second;


void setup()
{
    Serial.begin(115200);
    while (!Serial) ; // Needed for Leonardo only
    SerialGPS.begin(9600);
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

    Serial.println("Done Initialization");
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

        }
    }
}