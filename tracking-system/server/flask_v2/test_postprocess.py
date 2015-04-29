from math import *

# input: [ raw_ax, raw_ay, raw_az, raw_gx, raw_gy, raw_gz, dt ]
# -----------------------------------------------------

#   acceleration, unit: [9.81*meter/second**2]
raw_ax = 1
raw_ay = 1
raw_az = 1

#   angular velocity, unit: [131*degree/second]
raw_gx = 1
raw_gy = 1
raw_gz = 1

#   unit: [second]
dt = 1

###################################
#   todo: Complete the processes
###################################

#   define constant
g = 1 # [9.81*meter/second**2]
#tau = 4 # [second]
#alpha = tau / ( tau + dt ) # unitless
alpha = 0.98

#   initilization, todo: correct these
roll_filtered_previous = 0 # [131*degree/second]
pitch_filtered_previous = 0 # [131*degree/second]
velocity_previous = 0
distance_previous = 0

############################
#   calculation

#   roll
roll = raw_gx * dt # [131*degree/second]
roll_accel = atan( raw_ay / sqrt( raw_ax**2 + raw_az**2 ) ) # [131*degree/second]
roll_filtered = alpha * ( roll_filtered_previous + roll ) + ( 1 - alpha ) * roll_accel # [131*degree/second]

#   pitch
pitch = raw_gy * dt # [131*degree/second]
pitch_accel = atan( raw_ax / sqrt( raw_ay**2 / raw_az**2 ) ) # [131*degree/second]
pitch_filtered = alpha * ( pitch_filtered_previous + pitch ) + ( 1 - alpha ) * pitch_accel # [131*degree/second]

#   linear acceleration
linear_ax = raw_ax + pitch_filtered * g # [9.81*meter/second**2]
linear_ay = raw_ay - roll_filtered * g # [9.81*meter/second**2]
linear_az = raw_az - g # [9.81*meter/second**2]

#   distance
velocity = linear_ax * dt + velocity_previous
distance = velocity * dt + distance_previous

# -----------------------------------------------------------------
# expected output: [ linear_ax, linear_ay, linear_az, distance ]

print linear_ax, linear_ay, linear_az, distance
