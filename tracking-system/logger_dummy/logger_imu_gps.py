from multiprocessing import Process, Queue
import requests
import json
import time
import random
import datetime



def gps_logger( gps_data, results ):

	print 'gps_logger started.'

	while True:

		device_id = 1234
		timestamp = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
		latitude = round(random.uniform(1.5, 1.9), 5)
		longitude = round(random.uniform(1.5, 1.9), 5)

		gps_data.put( [ device_id, timestamp, latitude, longitude ] )

		time.sleep(2)



def post_data( payload, results ):
	while True:
		time.sleep(0.1)
		if not payload.empty():

			data_payload = payload.get()
			print data_payload

			try:
				url = 'http://localhost:8080/log'
				headers = {'content-type': 'application/json'}
				r = requests.post(url, data=json.dumps(data_payload), headers=headers)
				print(r.status_code)
			except:
				print("Failed to send data")


if __name__ == '__main__':

	results = Queue()

	gps_data = Queue()
	gps_process = Process( target=gps_logger, args=( gps_data, results ) )
	print '== start gps_process=='
	gps_process.start()

	payload = Queue()
	post_process = Process( target=post_data, args=( payload, results ) )
	post_process.start()

	# print '== joining processe 1 =='
	# gps_process.join()
	# print '== joining processe 2 =='
	# post_process.join()

	print '== create imu list =='
	imu_list = list()

	while True:

		if not gps_data.empty():
			# print imu_list
			# print '==========================',gps_data.get()

			#	pack and send data
			data_list = gps_data.get()
			data_list.append( imu_list )

			# print data_list
			payload.put( data_list )

			# payload.put( data_list )

			#	Reset
			imu_list = list()

		#	ax, ay, az, gx, gy, gz
		raw_imu = [
			random.randint(-16000, 16000),
			random.randint(-16000, 16000),
			random.randint(-16000, 16000),
			random.randint(-16000, 16000),
			random.randint(-16000, 16000),
			random.randint(-16000, 16000),

			random.uniform(0, 1) ]

		imu_list.append( raw_imu )
		time.sleep(0.1)

