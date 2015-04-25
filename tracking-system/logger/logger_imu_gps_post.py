from multiprocessing import Process, Queue
import requests
import json
import time
import random
import datetime
import gps
import smbus

###############################################
#
#	Constant
#
device_id = 1234

#	amr server
url = 'http://183.90.171.55:8080/log'
#	local
# url = 'http://192.168.1.114:8080/log'

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
def gps_logger( gps_data, results ):

	session = gps.gps("localhost", "2947")
	session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

	time.sleep(1)

	while True:

		report = session.next()
		# Wait for a 'TPV' report and get the information

		if report['class'] == 'TPV':

			if hasattr(report, 'time'):
				timestamp = report.time
			if hasattr(report, 'lat'):
				latitude = report.lat
			if hasattr(report, 'lon'):
				longitude = report.lon

			#	hack timestamp,
			#	from '2015-03-30T16:09:29.000Z' to '2015-03-30T16:09:29'
			gps_data.put( [ device_id, timestamp[0:19], latitude, longitude ] )


def post_data( payload, results ):
	while True:
		time.sleep(0.1)
		if not payload.empty():

			data_payload = payload.get()
			print data_payload

			try:
				# url = 'http://localhost:8080/log'

				headers = {'content-type': 'application/json'}
				r = requests.post(url, data=json.dumps(data_payload), headers=headers)
				print(r.status_code)
			except:
				print("Failed to send data")





if __name__ == '__main__':

	results = Queue()

	gps_data = Queue()
	gps_process = Process( target=gps_logger, args=( gps_data, results ) )

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

	session = gps.gps("localhost", "2947")
	session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)

	while True:
		report = session.next()
		# Wait for a 'TPV' report and get the information
		if report['class'] == 'TPV':
			if hasattr(report, 'time'):
				timestamp = report.time
			if hasattr(report, 'lat'):
				latitude = report.lat
			if hasattr(report, 'lon'):
				longitude = report.lon
			#	hack timestamp,
			#	from '2015-03-30T16:09:29.000Z' to '2015-03-30T16:09:29'
			gps_data.put( [ device_id, timestamp[0:19], latitude, longitude ] )

			break

	#	First read,
	#	acceleration
	raw_ax = read_word_2c(0x3b) - imu_offset[0]
	raw_ay = read_word_2c(0x3d) - imu_offset[1]
	raw_az = read_word_2c(0x3f) - imu_offset[2]
	#   gyro
	raw_gx = read_word_2c(0x43) - imu_offset[3]
	raw_gy = read_word_2c(0x45) - imu_offset[4]
	raw_gz = read_word_2c(0x47) - imu_offset[5]

	lastTime = time.time()

	imu_list = list()

	gps_process.start()
	post_process.start()

	data_list = gps_data.get()

	while True:

		if not gps_data.empty():

			#	pack and send data
			data_list.append( imu_list )
			payload.put( data_list )

			#	Reset
			imu_list = list()
			data_list = gps_data.get()


		#########################
		#   read data

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
		dt = now - lastTime
		lastTime = now

		imu_list.append( [
			raw_ax,
			raw_ay,
			raw_az,
			raw_gx,
			raw_gy,
			raw_gz,
			dt
		] )


