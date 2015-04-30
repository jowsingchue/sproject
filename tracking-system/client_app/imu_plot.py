#	standard modules
import argparse
import json
from pprint import pprint
from math import atan, sqrt, fabs

#	external modules
import requests
from matplotlib import pyplot as plt

#	GLOBAL
url = 'http://183.90.171.55:8080/log'
READ_FS_SEL = 0

G = 1
ALPHA = 0.1
CompCoef = 0.999
FSAccel = 16384.0
FSGyro = 131.0/(READ_FS_SEL + 1)

# sensor offset: ax, ay, az, gx, gy, gz
#OFFSET = [750, -28, -258, -256, 252, 139]
OFFSET = [ 0, 0, 0, 0, 0, 0 ]


def main():

	parser = argparse.ArgumentParser(description='Process and plot IMU data.')
	parser.add_argument('numrecord', metavar='NUM', type=int,
					   help='number of record')
	parser.add_argument('displaymode', metavar='MODE', type=int,
						help='display mode')
	args = parser.parse_args()
	num = args.numrecord
	displayMode = args.displaymode

	#	get data from server
	headers = {'content-type': 'application/json'}
	response = requests.get( url, data=json.dumps(num), headers=headers )
	contentDictList = json.loads( response.content )

	#	sort list by id
	sortedByIdDictList = sorted( contentDictList, key = lambda k: int( k[ 'id' ] ) )

	########################
	#	Initialization
	x_value = 0
	x = list()
	y1 = list()
	y2 = list()
	y3 = list()

	#	use first dict as starter value
	raw_ax = int( sortedByIdDictList[0][ 'ax' ] ) - OFFSET[0]
	raw_ay = int( sortedByIdDictList[0][ 'ay' ] ) - OFFSET[1]
	raw_az = int( sortedByIdDictList[0][ 'az' ] ) - OFFSET[2]
	raw_gx = int( sortedByIdDictList[0][ 'gx' ] ) - OFFSET[3]
	raw_gy = int( sortedByIdDictList[0][ 'gy' ] ) - OFFSET[4]
	raw_gz = int( sortedByIdDictList[0][ 'gz' ] ) - OFFSET[5]

	ax_scaled = raw_ax / FSAccel
	ay_scaled = raw_ay / FSAccel
	az_scaled = raw_az / FSAccel

	roll_comp_filtered = atan( ay_scaled / sqrt( ax_scaled**2 + az_scaled**2 ) ) # [131*degree/second]
	pitch_comp_filtered = atan( ax_scaled / sqrt( ay_scaled**2 + az_scaled**2 ) ) # [131*degree/second]

	velocity = 0
	distance = 0

	for dataDict in sortedByIdDictList[1:]:

		#	extract data
		raw_ax = int( dataDict[ 'ax' ] ) - OFFSET[0]
		raw_ay = int( dataDict[ 'ay' ] ) - OFFSET[1]
		raw_az = int( dataDict[ 'az' ] ) - OFFSET[2]
		raw_gx = int( dataDict[ 'gx' ] ) - OFFSET[3]
		raw_gy = int( dataDict[ 'gy' ] ) - OFFSET[4]
		raw_gz = int( dataDict[ 'gz' ] ) - OFFSET[5]
		delta_t = float( dataDict[ 'dt' ] )

#		 if fabs( raw_gx ) > 200:
#			 continue
#		 if fabs( raw_ax ) > 150:
#			 continue

		ax_scaled = raw_ax / FSAccel
		ay_scaled = raw_ay / FSAccel
		az_scaled = raw_az / FSAccel

		gx_scaled = raw_gx / FSGyro
		gy_scaled = raw_gy / FSGyro

		#	calculation
		#	roll
		roll = gx_scaled * delta_t # [131*degree/second]
		roll_accel = atan( ay_scaled / sqrt( ax_scaled**2 + az_scaled**2 ) ) # [131*degree/second]
		roll_comp_filtered = CompCoef * ( roll_comp_filtered + roll ) + ( 1 - CompCoef ) * roll_accel # [131*degree/second]

		#	pitch
		pitch = gy_scaled * delta_t # [131*degree/second]
		pitch_accel = atan( ax_scaled / sqrt( ay_scaled**2 + az_scaled**2 ) ) # [131*degree/second]
		pitch_comp_filtered = CompCoef * ( pitch_comp_filtered + pitch ) + ( 1 - CompCoef ) * pitch_accel # [131*degree/second]

		print pitch, pitch_accel, pitch_comp_filtered

		#	linear acceleration
		linear_ax = ax_scaled + pitch_comp_filtered * G # [9.81*meter/second**2]
		linear_ay = ay_scaled - roll_comp_filtered * G # [9.81*meter/second**2]
		linear_az = az_scaled - G # [9.81*meter/second**2]

		#	distance
		velocity = linear_ax * delta_t + velocity
		distance = velocity * delta_t + distance

		#	store in x-y list
		if displayMode == 1:
			y1.append( linear_ax )
			y2.append( linear_ay )
			y3.append( linear_az )

		if displayMode == 2:
			y1.append( raw_ax )
			y2.append( raw_ay )
			y3.append( raw_az )

		if displayMode == 3:
			y1.append( raw_gx )
			y2.append( raw_gy )
			y3.append( raw_gz )

		x_value += delta_t
		x.append( x_value )

	#	plot
	fig = plt.figure( 'Linear Acceleration (g) vs. Time (s)' )

	ax1 = fig.add_subplot( 311 )
	ax1.plot( x, y1 )

	ax2 = fig.add_subplot( 312 )
	ax2.plot( x, y2 )

	ax3 = fig.add_subplot( 313 )
	ax3.plot( x, y3 )

	#	label
	ax1.set_ylabel( 'x' )
	ax2.set_ylabel( 'Linear Acceleration (g)\ny' )
	ax3.set_ylabel( 'z' )
	ax3.set_xlabel( 'Time (s)' )

	plt.show()

	return

if __name__ == '__main__':
	main()
