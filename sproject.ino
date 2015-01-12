/*
# <Project name>


## Note for myself
Serial Port: /dev/tty.usbmodem1411


## Equipments

* [Arduino Uno](http://arduino.cc/en/Main/arduinoBoardUno)
* [SD Card](http://www.arduitronics.com/product/210/microsd-card-adapter-v1-1-catalex)
* [MPU-6050](http://playground.arduino.cc/Main/MPU-6050)
* [GY-GPS6MV2 (U-blox NEO 6M GPS)](https://developer.mbed.org/users/edodm85/notebook/gps-u-blox-neo-6m/)


## Wiring

MPU-6050
    INT   -  pin 2 
    SDA   -  pin A4
    SCL   -  pin A5
    VCC   -  5V
    GND   -  GND

GY-GPS6MV2 (U-blox NEO 6M GPS)
    TX (to RX on Arduino) - pin 7
    RX (to TX on Arduino) - pin 6
    VCC   -  5V
    GND   -  GND

SD Card
    MISO  -  pin 12
    MOSI  -  pin 11
    CLK   -  pin 13
    CS    -  pin 4
    VCC   -  5V
    GND   -  GND
*/

// MPU-6050
#include "I2Cdev.h"
#include "MPU6050.h"
// SD card
#include <SD.h>
// GPS
#include <SoftwareSerial.h>
#include <TinyGPS.h>


/*****************************************************************************/
// MPU-6050 Config
/*****************************************************************************/

// Arduino Wire library is required if I2Cdev I2CDEV_ARDUINO_WIRE implementation is used in I2Cdev.h
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
    #include "Wire.h"
#endif

MPU6050 accelgyro;

int16_t ax, ay, az;
int16_t gx, gy, gz;

// uncomment "OUTPUT_READABLE_ACCELGYRO" if you want to see a tab-separated
// list of the accel X/Y/Z and then gyro X/Y/Z values in decimal. Easy to read,
// not so easy to parse, and slow(er) over UART.
#define OUTPUT_READABLE_ACCELGYRO

// uncomment "OUTPUT_BINARY_ACCELGYRO" to send all 6 axes of data as 16-bit
// binary, one right after the other. This is very fast (as fast as possible
// without compression or data loss), and easy to parse, but impossible to read
// for a human.
// #define OUTPUT_BINARY_ACCELGYRO

// End MPU-6050 Config


/*****************************************************************************/
// SD Card Config
/*****************************************************************************/

// On the Ethernet Shield, CS is pin 4. Note that even if it's not
// used as the CS pin, the hardware CS pin (10 on most Arduino boards,
// 53 on the Mega) must be left as an output or the SD library
// functions will not work.
const int chipSelect = 4;

// End SD Card Config


/*****************************************************************************/
// GPS Config
/*****************************************************************************/

TinyGPS gps;
SoftwareSerial ss(4, 3); // TX, RX on GPS to (RX, TX) on Arduino
static void smartdelay(unsigned long ms);
static void print_float(float val, float invalid, int len, int prec);
static void print_int(unsigned long val, unsigned long invalid, int len);
static void print_date(TinyGPS &gps);
static void print_str(const char *str, int len);

// End GPS Config


#define LED_PIN 13
bool blinkState = false;

void setup()
{
    // join I2C bus (I2Cdev library doesn't do this automatically)
    #if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
        Wire.begin();
    #elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
        Fastwire::setup(400, true);
    #endif

    // initialize serial communication
    // (38400 chosen because it works as well at 8MHz as it does at 16MHz, but
    // it's really up to you depending on your project)
    Serial.begin(115200);

    // initialize device
    Serial.println("Initializing I2C devices...");
    accelgyro.initialize();

    // verify connection
    Serial.println("Testing device connections...");
    Serial.println(accelgyro.testConnection() ? "MPU6050 connection successful" : "MPU6050 connection failed");

    // use the code below to change accel/gyro offset values
    /* 
    Serial.println("Updating internal sensor offsets...");
    // -76	-2359	1688	0	0	0
    Serial.print(accelgyro.getXAccelOffset()); Serial.print("\t"); // -76
    Serial.print(accelgyro.getYAccelOffset()); Serial.print("\t"); // -2359
    Serial.print(accelgyro.getZAccelOffset()); Serial.print("\t"); // 1688
    Serial.print(accelgyro.getXGyroOffset()); Serial.print("\t"); // 0
    Serial.print(accelgyro.getYGyroOffset()); Serial.print("\t"); // 0
    Serial.print(accelgyro.getZGyroOffset()); Serial.print("\t"); // 0
    Serial.print("\n");
    accelgyro.setXGyroOffset(220);
    accelgyro.setYGyroOffset(76);
    accelgyro.setZGyroOffset(-85);
    Serial.print(accelgyro.getXAccelOffset()); Serial.print("\t"); // -76
    Serial.print(accelgyro.getYAccelOffset()); Serial.print("\t"); // -2359
    Serial.print(accelgyro.getZAccelOffset()); Serial.print("\t"); // 1688
    Serial.print(accelgyro.getXGyroOffset()); Serial.print("\t"); // 0
    Serial.print(accelgyro.getYGyroOffset()); Serial.print("\t"); // 0
    Serial.print(accelgyro.getZGyroOffset()); Serial.print("\t"); // 0
    Serial.print("\n");
    */

    // configure Arduino LED for
    pinMode(LED_PIN, OUTPUT);
    
    Serial.print("Initializing SD card...");
    // make sure that the default chip select pin is set to
    // output, even if you don't use it:
    pinMode(10, OUTPUT); //=================
    
    // see if the card is present and can be initialized:
    if (!SD.begin(chipSelect))
    {
        Serial.println("Card failed, or not present");
    }
    else
    {
        Serial.println("card initialized.");
    }
    
    Serial.println(); 
    Serial.println("The output will be in the format of:");
    Serial.println("----------------------------------------------------");
    Serial.println("{ax},{ay},{az},{gx},{gy},{gz},{latitude},{longitude}");
    Serial.println("----------------------------------------------------");
}

void loop()
{   
    // read imu
    accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);
    print_imu_to_serial();
    print_gps_to_serial();
    write_to_sd_card();
    delay(1000);

}


/**
*  Print IMU values to Serial
*/
static void print_imu_to_serial()
{
    // MPU-6050
    #ifdef OUTPUT_READABLE_ACCELGYRO
        // display tab-separated accel/gyro x/y/z values
        Serial.print("a/g:\t");
        Serial.print(ax); Serial.print("\t");
        Serial.print(ay); Serial.print("\t");
        Serial.print(az); Serial.print("\t");
        Serial.print(gx); Serial.print("\t");
        Serial.print(gy); Serial.print("\t");
        Serial.println(gz);
    #endif

    #ifdef OUTPUT_BINARY_ACCELGYRO
        Serial.write((uint8_t)(ax >> 8)); Serial.write((uint8_t)(ax & 0xFF));
        Serial.write((uint8_t)(ay >> 8)); Serial.write((uint8_t)(ay & 0xFF));
        Serial.write((uint8_t)(az >> 8)); Serial.write((uint8_t)(az & 0xFF));
        Serial.write((uint8_t)(gx >> 8)); Serial.write((uint8_t)(gx & 0xFF));
        Serial.write((uint8_t)(gy >> 8)); Serial.write((uint8_t)(gy & 0xFF));
        Serial.write((uint8_t)(gz >> 8)); Serial.write((uint8_t)(gz & 0xFF));
    #endif
}

/**
*
*/
static void print_gps_to_serial()
{
    float flat, flon;
    unsigned long age, date, time, chars = 0;
    unsigned short sentences = 0, failed = 0;
    static const double LONDON_LAT = 51.508131, LONDON_LON = -0.128002;
    
    print_int(gps.satellites(), TinyGPS::GPS_INVALID_SATELLITES, 5);
    print_int(gps.hdop(), TinyGPS::GPS_INVALID_HDOP, 5);
    gps.f_get_position(&flat, &flon, &age);
    print_float(flat, TinyGPS::GPS_INVALID_F_ANGLE, 10, 6);
    print_float(flon, TinyGPS::GPS_INVALID_F_ANGLE, 11, 6);
    print_int(age, TinyGPS::GPS_INVALID_AGE, 5);
    print_date(gps);
    print_float(gps.f_altitude(), TinyGPS::GPS_INVALID_F_ALTITUDE, 7, 2);
    print_float(gps.f_course(), TinyGPS::GPS_INVALID_F_ANGLE, 7, 2);
    print_float(gps.f_speed_kmph(), TinyGPS::GPS_INVALID_F_SPEED, 6, 2);
    print_str(gps.f_course() == TinyGPS::GPS_INVALID_F_ANGLE ? "*** " : TinyGPS::cardinal(gps.f_course()), 6);
    print_int(flat == TinyGPS::GPS_INVALID_F_ANGLE ? 0xFFFFFFFF : (unsigned long)TinyGPS::distance_between(flat, flon, LONDON_LAT, LONDON_LON) / 1000, 0xFFFFFFFF, 9);
    print_float(flat == TinyGPS::GPS_INVALID_F_ANGLE ? TinyGPS::GPS_INVALID_F_ANGLE : TinyGPS::course_to(flat, flon, LONDON_LAT, LONDON_LON), TinyGPS::GPS_INVALID_F_ANGLE, 7, 2);
    print_str(flat == TinyGPS::GPS_INVALID_F_ANGLE ? "*** " : TinyGPS::cardinal(TinyGPS::course_to(flat, flon, LONDON_LAT, LONDON_LON)), 6);

    gps.stats(&chars, &sentences, &failed);
    print_int(chars, 0xFFFFFFFF, 6);
    print_int(sentences, 0xFFFFFFFF, 10);
    print_int(failed, 0xFFFFFFFF, 9);
    Serial.println();

}

/**
* Write string data into SD card
*/
static void write_to_sd_card()
{
    String dataString = "";
    dataString += String(ax) + ", ";
    dataString += String(ay) + ", ";
    dataString += String(az) + ", ";
    dataString += String(gx) + ", ";
    dataString += String(gy) + ", ";
    dataString += String(gz);
    
    File dataFile = SD.open("data.log", FILE_WRITE);
    
    if (dataFile) {
        dataFile.println(dataString);
        dataFile.close();
    }
    else
    {
        Serial.println("error opening data.log");
    }  
}



/* ================================================================== */
static void smartdelay(unsigned long ms)
{
    unsigned long start = millis();
    do 
    {
        while (ss.available())
        gps.encode(ss.read());
    } while (millis() - start < ms);
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
        for (int i=flen; i<len; ++i)
            Serial.print(' ');
    }
    smartdelay(0);
}

static void print_int(unsigned long val, unsigned long invalid, int len)
{
    char sz[32];
    if (val == invalid)
        strcpy(sz, "*******");
    else
        sprintf(sz, "%ld", val);

    sz[len] = 0;
    for (int i=strlen(sz); i<len; ++i)
        sz[i] = ' ';
    if (len > 0) 
        sz[len-1] = ' ';
    Serial.print(sz);
    smartdelay(0);
}

static void print_date(TinyGPS &gps)
{
    int year;
    byte month, day, hour, minute, second, hundredths;
    unsigned long age;
    gps.crack_datetime(&year, &month, &day, &hour, &minute, &second, &hundredths, &age);
    if (age == TinyGPS::GPS_INVALID_AGE)
        Serial.print("********** ******** ");
    else
    {
        char sz[32];
        sprintf(sz, "%02d/%02d/%02d %02d:%02d:%02d ",
        month, day, year, hour, minute, second);
        Serial.print(sz);
    }
    print_int(age, TinyGPS::GPS_INVALID_AGE, 5);
    smartdelay(0);
}

static void print_str(const char *str, int len)
{
    int slen = strlen(str);
    for (int i=0; i<len; ++i)
        Serial.print(i<slen ? str[i] : ' ');
    smartdelay(0);
}
