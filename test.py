
from AMSpi import AMSpi
import time

if __name__ == '__main__':
	with AMSpi() as amspi:

		#find which motor corresponds to which?
		push_motor, conveyer_belt, bucket = amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3

		# Set PINs for controlling shift register (GPIO numbering)
		amspi.set_74HC595_pins(21, 20, 16)

		# Set PINs for controlling all 4 motors (GPIO numbering)

		amspi.set_L293D_pins(5, 6, 13, 19)

		print("GO: clockwise with 50% of maximum speed")
		amspi.run_dc_motors([amspi.DC_Motor_1], speed=52)
		print("Stop")
		amspi.stop_dc_motors([amspi.DC_Motor_1])
		time.sleep(2)
