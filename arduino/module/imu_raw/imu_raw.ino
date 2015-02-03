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

int count = 0;

void setup()
{
    // join I2C bus (I2Cdev library doesn't do this automatically)
#if I2CDEV_IMPLEMENTATION == I2CDEV_ARDUINO_WIRE
    Wire.begin();
#elif I2CDEV_IMPLEMENTATION == I2CDEV_BUILTIN_FASTWIRE
    Fastwire::setup(400, true);
#endif

    Serial.begin(115200);
    accelgyro.initialize();
    Serial.println(accelgyro.testConnection() ? "-- MPU6050 connection successful" : "-- MPU6050 connection failed");

    accelgyro.setXAccelOffset(-4783);
    accelgyro.setYAccelOffset(-1120);
    accelgyro.setZAccelOffset(1164);
    accelgyro.setXGyroOffset(58);
    accelgyro.setYGyroOffset(-40);
    accelgyro.setZGyroOffset(-39);

    // configure Arduino LED for
    pinMode(LED_PIN, OUTPUT);
}

void loop()
{
    // read raw accel/gyro measurements from device
    accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

    char dataString[100];
    sprintf(dataString,
            "%d,%d,%d,%d,%d,%d",
            ax, ay, az,
            gx, gy, gz
           );
    Serial.println(dataString);

    // blink LED to indicate activity
    // blinkState = !blinkState;
    // digitalWrite(LED_PIN, blinkState);

    // delay(200);

}
