#!/usr/bin/python

import smbus
import math
import time

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

# complementary filter params
K = 0.98
K1 = 1 - K

def read_byte(adr):
    return bus.read_byte_data(address, adr)

def read_word(adr):
    high = bus.read_byte_data(address, adr)
    low = bus.read_byte_data(address, adr+1)
    val = (high << 8) + low
    return val

def read_word_2c(adr):
    val = read_word(adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val

def comp_filter(prev_roll, prev_pitch, current_roll, current_pitch, gyro_scaled_x, gyro_scaled_y, dt):
    new_pitch = K * (prev_pitch + gyro_scaled_x * dt) + (K1 * current_roll)
    new_roll = K * (prev_roll + gyro_scaled_y * dt) + (K1 * current_pitch)
    return (new_pitch, new_roll)

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)


##########################################
#
#   Initialization
#
# offset = [ 700, -200, 1164, -30, -20, -18]
i = 0
lastTime = time.time()

accel_xout = read_word_2c(0x3b)
accel_yout = read_word_2c(0x3d)
accel_zout = read_word_2c(0x3f)

accel_xout_scaled = accel_xout / 16384.0
accel_yout_scaled = accel_yout / 16384.0
accel_zout_scaled = accel_zout / 16384.0

prev_roll = get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
prev_pitch = get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)


while True:

    i += 1

    #########################
    #   read data
    accel_xout = read_word_2c(0x3b)
    accel_yout = read_word_2c(0x3d)
    accel_zout = read_word_2c(0x3f)

    gyro_xout = read_word_2c(0x43)
    gyro_yout = read_word_2c(0x45)
    gyro_zout = read_word_2c(0x47)

    now = time.time()
    dt = now - lastTime
    lastTime = now

    #########################
    #   calculation
    accel_xout_scaled = accel_xout / 16384.0
    accel_yout_scaled = accel_yout / 16384.0
    accel_zout_scaled = accel_zout / 16384.0

    # gyro_xout_scaled = gyro_xout / 131
    # gyro_yout_scaled = gyro_yout / 131
    # gyro_zout_scaled = gyro_zout / 131

    current_roll = get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
    current_pitch = get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)

    # (roll, pitch) = comp_filter(prev_roll, prev_pitch, current_roll, current_pitch, gyro_xout_scaled, gyro_yout_scaled, dt)


    print( '{0:8d} {1:8d} {2:8d} {3:8d} {4:8d} {5:8d} {6:8d} {7:10.4f} {8:10.4f} {9}'.format(
          i,
          accel_xout - 400,
          accel_yout + 162,
          accel_zout + 360,
          gyro_xout + 31,
          gyro_yout - 20,
          gyro_zout - 18,
          current_roll,
          current_pitch,
          dt
    ))