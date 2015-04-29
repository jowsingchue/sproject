from multiprocessing import Process, Queue
import requests
import json
import time
import random
import datetime
import smbus

###############################################
#
#	Constant
#
device_id = 1234

#	amr server
#url = 'http://183.90.171.55:8080/log'
#	local
url = 'http://192.168.43.155:8080/log'

imu_offset = [ 56, -142, -294, -246, 192, 144 ]


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
#	Process
#

def post_data( payload, results ):
	while True:
		time.sleep(0.1)
		if not payload.empty():

			data_payload = payload.get()
			try:
				# url = 'http://localhost:8080/log'

				headers = {'content-type': 'application/json'}
				r = requests.post(url, data=json.dumps(data_payload), headers=headers)
				print(r.status_code)
			except:
				print("Failed to send data")





if __name__ == '__main__':

	results = Queue()

	payload = Queue()
	post_process = Process( target=post_data, args=( payload, results ) )


	##########################################
	#
	#	Initialize
	#
	bus = smbus.SMBus(1) # for Revision 2 boards

	# Power management registers
	power_mgmt_1 = 0x6b
	power_mgmt_2 = 0x6c

	# This is the address value read via the i2cdetect command
	address = 0x68

	# Now wake the 6050 up as it starts in sleep mode
	bus.write_byte_data(address, power_mgmt_1, 0)

	#	First read,
	print 'Read first data.'
	#	acceleration
	raw_ax = read_word_2c(0x3b) - imu_offset[0]
	raw_ay = read_word_2c(0x3d) - imu_offset[1]
	raw_az = read_word_2c(0x3f) - imu_offset[2]
	#   gyro
	raw_gx = read_word_2c(0x43) - imu_offset[3]
	raw_gy = read_word_2c(0x45) - imu_offset[4]
	raw_gz = read_word_2c(0x47) - imu_offset[5]

	lastReadTime = time.time()

	imu_list = list()

	post_process.start()

	data_list = [ device_id, False, False, False ]

	lastPostTime = time.time()

	while True:

		if time.time() - lastPostTime >= 2:

			#	pack and send data
			data_list.append( imu_list )
			print 'Sending data...'
			print data_list[:4], '[', data_list[4][0], ', ... ]'
			payload.put( data_list )

			#	Reset
			imu_list = list()
			lastPostTime = time.time()
			
			#	add new dummy gps data
			data_list = [ device_id, False, False, False ]


		#########################
		#   read imu data

		#   acceleration
		raw_ax = read_word_2c(0x3b) - imu_offset[0]
		raw_ay = read_word_2c(0x3d) - imu_offset[1]
		raw_az = read_word_2c(0x3f) - imu_offset[2]

		#   gyro
		raw_gx = read_word_2c(0x43) - imu_offset[3]
		raw_gy = read_word_2c(0x45) - imu_offset[4]
		raw_gz = read_word_2c(0x47) - imu_offset[5]

		#   time period
		now = time.time()
		dt = now - lastReadTime
		lastReadTime = now

		imu_list.append( [
			raw_ax,
			raw_ay,
			raw_az,
			raw_gx,
			raw_gy,
			raw_gz,
			dt
		] )


