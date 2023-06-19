#!/usr/bin/env python3

import serial
import time
import distance
import color

#start serial connection
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.reset_input_buffer()

try:
	while True:
		motion = False
		detect_color = ""
		color_detected = ""
		received_data = False
		#Check for incoming disks
		while motion == False:
			motion = distance.get_motion()
			time.sleep(1)
		#when motion is detected send signal to arduino
		ser.write(b"M")
		#wait for signal indicating that disk is under light sensor
		while detect_color != "Detect color":
			if ser.in_waiting > 0:
				detect_color = ser.readline().decode().rstrip()
				print("Arduino:" + detect_color)

		color_detected = color.get_color()
		if color_detected == 'B':
			print("PI: Black disk");
		elif color_detected == 'W':
			print("PI: White disk")
		elif color_detected == 'U':
			print("PI: Disk is not Black or White")

		ser.write(color_detected.encode())
		if color_detected == 'U':
			raise(Exception())
		#wait for instructions from the arduino to check for motion again
		while received_data == False:
			if ser.in_waiting > 0:
				data = ser.readline().decode().rstrip()
				print("Arduino:" + data)
				received_data = True

		#check if the track is clear
		if data == "Check if track is clear":
			while motion == True:
				motion = distance.get_motion()
				time.sleep(1)

		#Tell the arduino that track is clear ->  Go extend fetching mechanism]
			print("PI: Extend the mechanism")
			ser.write(b"G")
			time.sleep(1)

except KeyboardInterrupt:
            print("PI: Measurement stopped by User")
except Exception:
			print("PI: A Disk that is neither black or white was fetched: restart execution of the code")
