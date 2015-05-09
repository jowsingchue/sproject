#	standard modules
import argparse
import json
from pprint import pprint
from math import atan, sqrt, fabs, pi

#	external modules
import requests
from matplotlib import pyplot as plt
from scipy.fftpack import fft
import numpy

#	GLOBAL

#   amr server
url = 'http://183.90.171.55:8080/log'

#url = 'http://localhost:8080/log'

# sensor offset: ax, ay, az, gx, gy, gz
#OFFSET = [750, -28, -258, -256, 252, 139]
OFFSET = [ -600, 0, 0, -244, 169, 144 ]

READ_FS_SEL = 0

G = 1
ALPHA = 0.1
CompCoef = 0.999
FSAccel = 16384.0
FSGyro = 131.0/(READ_FS_SEL + 1)



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

	gx_scaled = raw_gx / FSGyro
	gy_scaled = raw_gy / FSGyro

	roll_comp_filtered = atan( ay_scaled / sqrt( ax_scaled**2 + az_scaled**2 ) ) # [131*degree/second]
	pitch_comp_filtered = atan( ax_scaled / sqrt( ay_scaled**2 + az_scaled**2 ) ) # [131*degree/second]

	velocity = 0
	distance = 0

	gx_degree = raw_gx / 131.0
	gy_degree = raw_gy / 131.0
	gz_degree = raw_gz / 131.0

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

#		gx_scaled = raw_gx / FSGyro
#		gy_scaled = raw_gy / FSGyro
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

		print pitch_comp_filtered, roll_comp_filtered

		# ------------------------------------------------------------------
		gx_dps = raw_gx / 131.0 - 0.0597 # sensitivity drift
		gy_dps = raw_gy / 131.0 - 0.032 # sensitivity drift
		gz_dps = raw_gz / 131.0

		gx_degree = gx_degree + gx_dps * delta_t #+ 0.2   # zero drift
		gy_degree = gy_degree + gy_dps * delta_t #+ 0.16   # zero drift
		gz_degree = gz_degree + gz_dps * delta_t

		gx_rad = gx_degree * pi / 180.0
		gy_rad = gy_degree * pi / 180.0
		gz_rad = gz_degree * pi / 180.0
		# ------------------------------------------------------------------

		#	linear acceleration
		linear_ax = ax_scaled + gy_rad * G # [9.81*meter/second**2]
		linear_ay = ay_scaled - gx_rad * G # [9.81*meter/second**2]
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

		if displayMode == 4:
			y1.append( pitch_comp_filtered )
			y2.append( roll_comp_filtered )
			y3.append( raw_gz )

		if displayMode == 5:
			y1.append( gx_degree )
			y2.append( gy_degree )
			y3.append( gz_degree )

		if displayMode == 6:
			y1.append( gx_degree )
			y2.append( gy_degree )
			y3.append( gz_degree )

		x_value += delta_t
		x.append( x_value )

	#	fft
	Y = fft( y1 )

	#	plot
	fig = plt.figure( 'Linear Acceleration (g) vs. Time (s)' )

	ax1 = fig.add_subplot( 311 )
	ax1.plot( x, y1 )

	ax2 = fig.add_subplot( 312 )
	ax2.plot( x, y2 )

	ax3 = fig.add_subplot( 313 )
	ax3.plot( x, y3 )
#	ax3.plot( x, Y )

	#	label
	ax1.set_ylabel( 'x' )
	ax2.set_ylabel( 'Linear Acceleration (g)\ny' )
	ax3.set_ylabel( 'z' )
	ax3.set_xlabel( 'Time (s)' )

	plt.show()

	return

if __name__ == '__main__':
	main()
