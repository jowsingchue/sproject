#include "I2Cdev.h"
#include "MPU6050.h"
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
#include "Wire.h"
#endif
MPU6050 accelgyro;
int16_t ax, ay, az;
int16_t gx, gy, gz;
#define OUTPUT_READABLE_ACCELGYRO
// uncomment "OUTPUT_BINARY_ACCELGYRO" to send all 6 axes of data as 16-bit
// binary, one right after the other. This is very fast (as fast as possible
// without compression or data loss), and easy to parse, but impossible to read
// for a human.
//#define OUTPUT_BINARY_ACCELGYRO

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

    Serial.begin(38400);
    Serial.println();
    Serial.println();

    // initialize device
    Serial.println("Initializing I2C devices...");
    accelgyro.initialize();

    // verify connection
    Serial.println("Testing device connections...");
    Serial.println(accelgyro.testConnection() ? "MPU6050 connection successful" : "MPU6050 connection failed");

    // use the code below to change accel/gyro offset values
    /*
        Serial.println("Updating internal sensor offsets...");
        // -76  -2359   1688    0   0   0
        Serial.print(accelgyro.getXAccelOffset()); Serial.print("\t"); // -76
        Serial.print(accelgyro.getYAccelOffset()); Serial.print("\t"); // -2359
        Serial.print(accelgyro.getZAccelOffset()); Serial.print("\t"); // 1688
        Serial.print(accelgyro.getXGyroOffset()); Serial.print("\t"); // 0
        Serial.print(accelgyro.getYGyroOffset()); Serial.print("\t"); // 0
        Serial.print(accelgyro.getZGyroOffset()); Serial.print("\t"); // 0
        Serial.print("\n");
        accelgyro.setXAccelOffset(0);
        accelgyro.setYAccelOffset(0);
        accelgyro.setZAccelOffset(0);
        accelgyro.setXGyroOffset(0);
        accelgyro.setYGyroOffset(0);
        accelgyro.setZGyroOffset(0);
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
}

void loop()
{
    // read raw accel/gyro measurements from device
    accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

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

    // blink LED to indicate activity
    blinkState = !blinkState;
    digitalWrite(LED_PIN, blinkState);

    delay(1000);
}
