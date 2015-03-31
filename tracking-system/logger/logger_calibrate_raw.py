#!/usr/bin/python

import smbus

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



bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
address = 0x68       # This is the address value read via the i2cdetect command

# Now wake the 6050 up as it starts in sleep mode
bus.write_byte_data(address, power_mgmt_1, 0)



#   ax, ay, az, gx, gy, gz
rawData = [
    read_word_2c(0x3b),
    read_word_2c(0x3d),
    read_word_2c(0x3f),
    read_word_2c(0x43),
    read_word_2c(0x45),
    read_word_2c(0x47)
]

minValue = list()
maxValue = list()

for x in rawData:
    minValue.append( x )
    maxValue.append( x )

print '-------- Before --------'
print minValue
print maxValue

for i in range(2000):

    #########################
    #   read data
    rawData = [
        read_word_2c(0x3b),
        read_word_2c(0x3d),
        read_word_2c(0x3f),
        read_word_2c(0x43),
        read_word_2c(0x45),
        read_word_2c(0x47)
    ]

    for index, value in enumerate( rawData ):
        if minValue[ index ] > value:
            minValue[ index ] = value
        if maxValue[ index ] < value:
            maxValue[ index ] = value

print '-------- After --------'
print minValue
print maxValue

aveValue = list()
for index in range( 0, len( minValue ) ):
    aveValue.append( int( ( minValue[ index ] + maxValue[ index ] ) / 2.0 ) )
aveValue[2] -= 16384

print '--------- Result -----------'
print aveValue