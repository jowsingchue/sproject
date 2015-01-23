// IMU ------------------------------------------------------------------------

#include <I2Cdev.h>
#include <MPU6050.h>
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
#include <Wire.h>
#endif
MPU6050 accelgyro;
int16_t ax, ay, az;
int16_t gx, gy, gz;
#define LED_PIN 13
bool blinkState = false;



// GPS ------------------------------------------------------------------------

#include <SoftwareSerial.h>
#include <TinyGPS.h>
TinyGPS gps;
SoftwareSerial ss(7, 6);
float flat, flon;
unsigned long age;
static void smartdelay(unsigned long ms);
static void print_float(float val, float invalid, int len, int prec);



// SD card --------------------------------------------------------------------

#include <SD.h>
const int chipSelect = 4;
File root;
static void printDirectory(File dir, int numTabs);



/******************************************************************************
*  Setup
******************************************************************************/
void setup()
{
    
    Serial.begin(38400);
    Serial.println();
    Serial.println();

    while (!Serial)
    {
        ; // wait for serial port to connect. Needed for Leonardo only
    }
    


// IMU ------------------------------------------------------------------------

    // join I2C bus (I2Cdev library doesn't do this automatically)
    #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
    Wire.begin();
    #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
    Fastwire::setup(400, true);
    #endif

    // initialize device
    Serial.println("Initializing I2C devices...");
    accelgyro.initialize();

    // verify connection
    Serial.println("Testing device connections...");
    Serial.println(accelgyro.testConnection() ? "MPU6050 connection successful" : "MPU6050 connection failed");
    pinMode(LED_PIN, OUTPUT);

// GPS ------------------------------------------------------------------------
    
    Serial.println("Latitude, Longitude");
    ss.begin(9600);



// SD card --------------------------------------------------------------------

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



/******************************************************************************
*  Loop
******************************************************************************/

void loop()
{

// IMU ------------------------------------------------------------------------

    // read raw accel/gyro measurements from device
    accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);



// GPS ------------------------------------------------------------------------

    gps.f_get_position(&flat, &flon, &age);

    // print_float(flat, TinyGPS::GPS_INVALID_F_ANGLE, 10, 6);
    // print_float(flon, TinyGPS::GPS_INVALID_F_ANGLE, 11, 6);
    // Serial.println();


// SD card --------------------------------------------------------------------
    
    // make a string for assembling the data to log:
    String dataString = "";
    dataString += String(flat) + ",";
    dataString += String(flon) + ",";
    dataString += String(ax) + ",";
    dataString += String(ay) + ",";
    dataString += String(az) + ",";
    dataString += String(gx) + ",";
    dataString += String(gy) + ",";
    dataString += String(gz) + ",";

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

    

    // blink LED to indicate activity
    blinkState = !blinkState;
    digitalWrite(LED_PIN, blinkState);
    smartdelay(1000);
}

/******************************************************************************
*  Function
******************************************************************************/

// GPS ------------------------------------------------------------------------

static void smartdelay(unsigned long ms)
{
    unsigned long start = millis();
    do
    {
        while (ss.available())
            gps.encode(ss.read());
    }
    while (millis() - start < ms);
}

static void print_float(float val, float invalid, int len, int prec)
{
    if (val == invalid)
    {
        while (len-- > 1)
            Serial.print('*');
        Serial.print(' ');
    }
    else
    {
        Serial.print(val, prec);
        int vi = abs((int)val);
        int flen = prec + (val < 0.0 ? 2 : 1); // . and -
        flen += vi >= 1000 ? 4 : vi >= 100 ? 3 : vi >= 10 ? 2 : 1;
        for (int i = flen; i < len; ++i)
            Serial.print(' ');
    }
    smartdelay(0);
}


// SD card --------------------------------------------------------------------

static void printDirectory(File dir, int numTabs)
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
