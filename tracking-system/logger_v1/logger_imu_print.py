#!/usr/bin/python

import smbus
import math
from math import sin
from math import cos
import time

# Power management registers
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c


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

def accel_low_pass_filter(ax, ay, az, raw_ax, raw_ay, raw_az):
    new_ax = ax + alpha * ( raw_ax - ax )
    new_ay = ay + alpha * ( raw_ay - ay )
    new_az = az + alpha * ( raw_az - az )
    return ( int(new_ax), int(new_ay), int(new_az) )

def comp_filter(roll, pitch,
                gyro_scaled_x,
                gyro_scaled_y,
                ax_filtered_scaled,
                ay_filtered_scaled,
                dt ):
    new_roll = K * (roll + gyro_scaled_x * dt) + (K1 * ax_filtered_scaled)
    new_pitch = K * (pitch + gyro_scaled_y * dt) + (K1 * ay_filtered_scaled)
    return (new_roll, new_pitch)

def dist(a,b):
    return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -radians

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return radians

bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)


##########################################
#
#   Constant
#

# low pass filter const
alpha = 0.1

# complementary filter const
K = 0.999
K1 = 1 - K

# gyroscope
READ_FS_SEL = read_word_2c(0x1b)
GYRO_FACTOR = 131.0/(READ_FS_SEL + 1)

# sensor offset: ax, ay, az, gx, gy, gz
offset = [750, -28, -258, -256, 252, 139]


##########################################
#
#   Initialization, these are required for filter
#



ax_filtered = read_word_2c(0x3b)
ay_filtered = read_word_2c(0x3d)
az_filtered = read_word_2c(0x3f)

lastTime = time.time()

ax_filtered_scaled = ax_filtered / 16384.0
ay_filtered_scaled = ay_filtered / 16384.0
az_filtered_scaled = az_filtered / 16384.0

roll = get_x_rotation(ax_filtered_scaled, ay_filtered_scaled, az_filtered_scaled)
pitch = get_y_rotation(ax_filtered_scaled, ay_filtered_scaled, az_filtered_scaled)


while True:

    #########################
    #   read data

    #   acceleration
    raw_ax = read_word_2c(0x3b) - offset[0]
    raw_ay = read_word_2c(0x3d) - offset[1]
    raw_az = read_word_2c(0x3f) - offset[2]

    #   gyro
    raw_gx = read_word_2c(0x43) - offset[3]
    raw_gy = read_word_2c(0x45) - offset[4]
    raw_gz = read_word_2c(0x47) - offset[5]

    #   time period
    now = time.time()
    dt = now - lastTime
    lastTime = now





    #########################
    #   low pass filter on accel
    ( ax_filtered, ay_filtered, az_filtered ) = accel_low_pass_filter( ax_filtered,
                                                              ay_filtered,
                                                              az_filtered,
                                                              raw_ax,
                                                              raw_ay,
                                                              raw_az )

    #########################
    #   calculation
    raw_ax_scaled = raw_ax / 16384.0
    raw_ay_scaled = raw_ay / 16384.0
    raw_az_scaled = raw_az / 16384.0

    ax_filtered_scaled = ax_filtered / 16384.0
    ay_filtered_scaled = ay_filtered / 16384.0
    az_filtered_scaled = az_filtered / 16384.0

    raw_gx_scaled = raw_gx / GYRO_FACTOR
    raw_gy_scaled = raw_gy / GYRO_FACTOR
    raw_gz_scaled = raw_gz / GYRO_FACTOR

    roll = get_x_rotation(ax_filtered_scaled, ay_filtered_scaled, az_filtered_scaled)
    pitch = get_y_rotation(ax_filtered_scaled, ay_filtered_scaled, az_filtered_scaled)

    (roll, pitch) = comp_filter(roll, pitch, raw_gx_scaled, raw_gy_scaled, ax_filtered_scaled, ay_filtered_scaled, dt)

    #   get gravity component
    #   source: http://reallybigcompany.com/papers/roll_pitch/roll_pitch.htm
    # gravity_scaled = [ -sin( roll ), cos( roll ) * sin( pitch ), cos( roll ) * cos( pitch ) ]
    # gravity = [ x * 16384.0 for x in gravity_scaled ]

    # linear_ax = raw_ax - gravity[0]
    # linear_ay = raw_ay - gravity[1]
    # linear_az = raw_az - gravity[2]

    # linear_ax_scaled = raw_ax_scaled - gravity_scaled[0]
    # linear_ay_scaled = raw_ay_scaled - gravity_scaled[1]
    # linear_az_scaled = raw_az_scaled - gravity_scaled[2]

    linear_ax = raw_ax - ax_filtered
    linear_ay = raw_ay - ay_filtered
    linear_az = raw_az - az_filtered


    print( '{:8d} {:8d} {:8d} {:8d} {:8d} {:8d} {:10.0f} {:10.0f} {:10.4f}'.format(
        int( linear_ax ),
        int( linear_ay ),
        int( linear_az ),
        raw_gx,
        raw_gy,
        raw_gz,
        math.degrees(roll),
        math.degrees(pitch),
        dt
    ))

    time.sleep(0.1)
