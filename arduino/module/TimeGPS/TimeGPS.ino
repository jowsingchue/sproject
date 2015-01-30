
#include <Time.h>
#include <TinyGPS.h>
#include <SoftwareSerial.h>

SoftwareSerial SerialGPS = SoftwareSerial(7, 6);
TinyGPS gps;

// Offset hours from gps time (UTC)
const int offset = 7;  // Bangkok Thailand

time_t prevDisplay = 0; // when the digital clock was displayed

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
            digitalClockDisplay();
        }
    }
}

void digitalClockDisplay()
{
    // digital clock display of the time
    Serial.print(hour());
    printDigits(minute());
    printDigits(second());
    Serial.print(" ");
    Serial.print(day());
    Serial.print(" ");
    Serial.print(month());
    Serial.print(" ");
    Serial.print(year());
    Serial.println();
}

void printDigits(int digits)
{
    // utility function for digital clock display: prints preceding colon and leading 0
    Serial.print(":");
    if (digits < 10)
        Serial.print('0');
    Serial.print(digits);
}

