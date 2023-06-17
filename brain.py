import serial
import time
import distance
import color

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.reset_input_buffer()

while True:
	motion = False
	color = ""
	received_data = False
	while motion == False:
		motion = distance.get_motion()
	#when motion is detected
	ser.write(b"M")
	#wait until disk is under light sensor
	time.sleep(12.5)
	color = color.get_color()
	ser.write(color.encode())
	#wait for instructions from the arduino
	while received_data == False:
		if ser.in_waiting > 0:
			data = ser.readline().decode().rstrip()
			print(data)
			received_data = True

	if data == "check if track is clear":
		while motion == True:
			motion = distance.get_motion()
		#Tell the arduino that track is clear ->  Go extend fetching mechanism
		ser.write(b"G")

