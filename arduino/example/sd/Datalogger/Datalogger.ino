/*
  SD card datalogger

 This example shows how to log data from three analog sensors
 to an SD card using the SD library.

 The circuit:
 * analog sensors on analog ins 0, 1, and 2
 * SD card attached to SPI bus as follows:
 ** MOSI - pin 11
 ** MISO - pin 12
 ** CLK - pin 13
 ** CS - pin 4

 created  24 Nov 2010
 modified 9 Apr 2012
 by Tom Igoe

 This example code is in the public domain.

 */

#include <SD.h>

// On the Ethernet Shield, CS is pin 4. Note that even if it's not
// used as the CS pin, the hardware CS pin (10 on most Arduino boards,
// 53 on the Mega) must be left as an output or the SD library
// functions will not work.
const int chipSelect = 4;


void setup()
{
    // Open serial communications and wait for port to open:
    Serial.begin(115200);
    while (!Serial)
    {
        ; // wait for serial port to connect. Needed for Leonardo only
    }


    Serial.print("Initializing SD card...");
    // make sure that the default chip select pin is set to
    // output, even if you don't use it:
      pinMode(10, OUTPUT);
      digitalWrite(10, HIGH); // davekw7x: If it's low, the Wiznet chip corrupts the SPI bus

    // see if the card is present and can be initialized:
    if (!SD.begin(chipSelect))
    {
        Serial.println("Card failed, or not present");
        // don't do anything more:
        return;
    }
    Serial.println("card initialized.");

    if (SD.exists("test.log"))
    {
        SD.remove("test.log");
        Serial.println("test.log removed");
    } else {
        Serial.println("test.log not found");
    }

    // -----
}

void loop()
{
    // make a string for assembling the data to log:
    String dataString = "";

    // read three sensors and append to the string:
    // for (int analogPin = 0; analogPin < 3; analogPin++) {
    //   int sensor = analogRead(analogPin);
    //   dataString += String(sensor);
    //   if (analogPin < 2) {
    //     dataString += ",";
    //   }
    // }
    for (int i = 0; i < 3; i++)
    {
        dataString += String(i);
        if (i < 2)
        {
            dataString += ",";
        }
    }

    // open the file. note that only one file can be open at a time,
    // so you have to close this one before opening another.
    File dataFile = SD.open("test.log", FILE_WRITE);

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
        Serial.println("error opening test.log");
    }

    delay(400);
}









