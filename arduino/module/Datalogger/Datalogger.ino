#include <SD.h>
const int chipSelect = 4;
char dirName[12];
char fileName[12];
char fileLocation[30];

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

    // see if the card is present and can be initialized:
    if (!SD.begin(chipSelect))
    {
        Serial.println("Card failed, or not present");
        // don't do anything more:
        return;
    }
    Serial.println("card initialized.");

    sprintf(dirName, "%04d%02d%02d",
            2014, 02, 27
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
            15, 04, 48
           );
    Serial.print("File name is: ");
    Serial.println(fileName);

    strcpy(fileLocation, dirName);
    strcat(fileLocation, "/");
    strcat(fileLocation, fileName);

    Serial.print("Data will be write to: ");
    Serial.println(fileLocation);
}

void loop()
{

    String dataString = "2015-01-25,16:42:36,13.847307,100.569810,-9420,-8200,-10848,-237,191,138";

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

    delay(400);
}









