from optparse import OptionParser
from multiprocessing import Process, Queue
from random import randint
from pprint import pprint
import time
import random
import json
import datetime

import requests
#import smbus


###############################################
#
#	Constant
#
device_id = 1234

#	amr server
#url = 'http://183.90.171.55:8080/log'
#	local
url = 'http://localhost:8080/log'
#url = 'http://192.168.43.155:8080/log'

#imu_offset = [ 56, -142, -294, -246, 192, 144 ]


#################################################
#
#	Function
#
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


###############################################
#
#	Class
#

class ImuRaw():
	'''
	Read raw data
	'''

	def __init__( self, withOffset=False ):

#		if withOffset:
#			#	acceleration
#			self.ax = read_word_2c(0x3b) - imu_offset[0]
#			self.ay = read_word_2c(0x3d) - imu_offset[1]
#			self.az = read_word_2c(0x3f) - imu_offset[2]
#			#   gyro
#			self.gx = read_word_2c(0x43) - imu_offset[3]
#			self.gy = read_word_2c(0x45) - imu_offset[4]
#			self.gz = read_word_2c(0x47) - imu_offset[5]
#
#		else:
#			#	acceleration
#			self.ax = read_word_2c(0x3b)
#			self.ay = read_word_2c(0x3d)
#			self.az = read_word_2c(0x3f)
#			#   gyro
#			self.gx = read_word_2c(0x43)
#			self.gy = read_word_2c(0x45)
#			self.gz = read_word_2c(0x47)

		self.ax = randint( 0, 16384 )
		self.ay = randint( 0, 16384 )
		self.az = randint( 0, 16384 )
		self.gx = randint( 0, 16384 )
		self.gy = randint( 0, 16384 )
		self.gz = randint( 0, 16384 )


###############################################
#
#	Process
#

def do_post( payload, results ):
	while True:
		time.sleep(0.1)
		if not payload.empty():

			data_payload = payload.get()
			print
			pprint( data_payload )
			try:
				headers = {'content-type': 'application/json'}
				r = requests.post(url, data=json.dumps(data_payload), headers=headers)
				print(r.status_code)
			except:
				print("Failed to send data")


###############################################
#
#	Main
#

def main():

	#	option
	parser = OptionParser()
	
	results = Queue()
	payload = Queue()
	post_process = Process( target=do_post, args=( payload, results ) )


	##########################################
	#
	#	Initialize
	#

#	bus = smbus.SMBus(1) # for Revision 2 boards
#
#	# Power management registers
#	power_mgmt_1 = 0x6b
#	power_mgmt_2 = 0x6c
#
#	# This is the address value read via the i2cdetect command
#	address = 0x68
#
#	# Now wake the 6050 up as it starts in sleep mode
#	bus.write_byte_data(address, power_mgmt_1, 0)

	#data_list = [ device_id, False, False, False ]
	data_list = [ device_id, '2015-03-30T16:09:29', 13.8486997,100.5491168 ]
	imu = ImuRaw()
	lastReadTime = time.time()
	lastPostTime = time.time()

	post_process.start()

	imu_list = list()
	while True:

		if time.time() - lastPostTime >= 2:

			#	pack and send data
			data_list.append( imu_list )
			print '------------------------'
			print 'Sending data...'
			print data_list[:4], '[', data_list[4][0], ', ... ]'
			payload.put( data_list )

			#	Reset
			imu_list = list()
			lastPostTime = time.time()
			
			#	add new dummy gps data
			#data_list = [ device_id, False, False, False ]
			data_list = [ device_id, '2015-03-30T16:09:29', 13.8486997,100.5491168 ]


		#########################
		#   read imu data

		imu = ImuRaw()

		#   time period
		now = time.time()
		dt = now - lastReadTime
		lastReadTime = now

		imu_list.append( [
			imu.ax,
			imu.ay,
			imu.az,
			imu.gx,
			imu.gy,
			imu.gz,
			dt
		] )

		time.sleep( 1 )


if __name__ == '__main__':
	main()
