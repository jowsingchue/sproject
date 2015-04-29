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

ax = list()
ay = list()
az = list()
gx = list()
gy = list()
gz = list()

print 'Collection data.....'
for i in range(10000):

    #########################
    #   read data

    #   ax, ay, az, gx, gy, gz
    rawData = [
        read_word_2c(0x3b),
        read_word_2c(0x3d),
        read_word_2c(0x3f),
        read_word_2c(0x43),
        read_word_2c(0x45),
        read_word_2c(0x47)
    ]

    ax.append( rawData[0] )
    ay.append( rawData[1] )
    az.append( rawData[2] )
    gx.append( rawData[3] )
    gy.append( rawData[4] )
    gz.append( rawData[5] )

    print i, ': ',
    print rawData[0],
    print rawData[1],
    print rawData[2],
    print rawData[3],
    print rawData[4],
    print rawData[5]

print
print
print '##### RESULT #####'
print int( sum( ax ) / float( len( ax ) ) ),
print int( sum( ay ) / float( len( ay ) ) ),
print int( sum( az ) / float( len( az ) ) ) - 16384,
print int( sum( gx ) / float( len( gx ) ) ),
print int( sum( gy ) / float( len( gy ) ) ),
print int( sum( gz ) / float( len( gz ) ) )

