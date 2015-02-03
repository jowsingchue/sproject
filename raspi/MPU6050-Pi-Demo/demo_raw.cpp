#include <stdio.h>
#include <stdint.h>
#include <unistd.h>
#include "I2Cdev.h"
#include "MPU6050.h"

// class default I2C address is 0x68
// specific I2C addresses may be passed as a parameter here
// AD0 low = 0x68 (default for InvenSense evaluation board)
// AD0 high = 0x69
MPU6050 accelgyro;

int16_t ax, ay, az;
int16_t gx, gy, gz;

int count=0;

void setup() {
    // initialize device
    printf("Initializing I2C devices...\n");
    accelgyro.initialize();

    accelgyro.setFullScaleGyroRange(MPU6050_GYRO_FS_250);
    accelgyro.setFullScaleAccelRange(MPU6050_ACCEL_FS_2);

    // accelgyro.setXAccelOffset(-4783);
    accelgyro.setXAccelOffset(-4701);
    accelgyro.setYAccelOffset(-1143);
    accelgyro.setZAccelOffset(1172);
    accelgyro.setXGyroOffset(-23);
    accelgyro.setYGyroOffset(9);
    accelgyro.setZGyroOffset(-114);

    // verify connection
    printf("Testing device connections...\n");
    printf(accelgyro.testConnection() ? "MPU6050 connection successful\n" : "MPU6050 connection failed\n");
}

void loop() {

    printf("%d: ", ++count);

    // read raw accel/gyro measurements from device
    accelgyro.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

    // these methods (and a few others) are also available
    //accelgyro.getAcceleration(&ax, &ay, &az);
    //accelgyro.getRotation(&gx, &gy, &gz);

    // display accel/gyro x/y/z values
    printf("a/g: %6hd %6hd %6hd   %6hd %6hd %6hd\n",ax,ay,az,gx,gy,gz);
}

int main()
{
    setup();
    for (;;)
        loop();
}

