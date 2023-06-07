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

		amspi.run_dc_motors(push_motor)
		time.sleep(5)
		amspi.stop_dc_motors(push_motor)
		time.sleep(5)
		amspi.run_dc_motors(conveyer_belt)
		time.sleep(5)
		amspi.stop_dc_motors(conveyer_belt)
		time.sleep(5)
		amspi.run_dc_motors(bucket)
		time.sleep(5)
		amspi.stop_dc_motor(bucket)

