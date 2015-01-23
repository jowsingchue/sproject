#include <SD.h>
const int chipSelect = 4;

File root;

void printDirectory(File dir, int numTabs);

void setup()
{
    // Open serial communications and wait for port to open:
    Serial.begin(38400);
    Serial.println();
    Serial.println();

    while (!Serial)
    {
        ; // wait for serial port to connect. Needed for Leonardo only
    }

    Serial.print("Initializing SD card... ");
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

    // use code below to list files in SD
    Serial.println("Files in /data");
    root = SD.open("/data");
    printDirectory(root, 1);

    if (SD.exists("data/test.log"))
    {
        SD.remove("data/test.log");
        Serial.println("test.log has been removed");
    }
    else
    {
        Serial.println("test.log not found");
    }
    Serial.println("--- Done initialization ---");
}

void loop()
{
    // make a string for assembling the data to log:
    String dataString = "";

    for (int i = 0; i < 3; i++)
    {
        dataString += String(i);
        if (i < 2)
        {
            dataString += ",";
        }
    }

    File dataFile = SD.open("data/test.log", FILE_WRITE);

    if (dataFile)
    {
        dataFile.println(dataString);
        dataFile.close();
        // print to Serial
        Serial.print("Data written: ");
        Serial.println(dataString);
    }
    else
    {
        Serial.println("error opening test.log");
    }

    delay(1000);
}

void printDirectory(File dir, int numTabs)
{
    while (true)
    {

        File entry =  dir.openNextFile();
        if (! entry)
        {
            // no more files
            break;
        }
        for (uint8_t i = 0; i < numTabs; i++)
        {
            Serial.print('\t');
        }
        Serial.print(entry.name());
        if (entry.isDirectory())
        {
            Serial.println("/");
            printDirectory(entry, numTabs + 1);
        }
        else
        {
            // files have sizes, directories do not
            Serial.print("\t\t");
            Serial.println(entry.size(), DEC);
        }
        entry.close();
    }
}
