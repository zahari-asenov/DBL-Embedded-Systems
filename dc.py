#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from AMSpi import AMSpi
import time

with AMSpi() as amspi:

#find which motor corresponds to which?
    push_motor, conveyer_belt, bucket = amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3

    # Set PINs for controlling shift register (GPIO numbering)
    amspi.set_74HC595_pins(21, 20, 16)

    # Set PINs for controlling all 4 motors (GPIO numbering)

    amspi.set_L293D_pins(5, 6, 13, 19)

    def read_motion():
         pass
    def reset_pushing_mechanism():
        #find the exact configuration to reste the pushing mechanism
        amspi.run_dc_motors(push_motor)
        time.sleep(5)
        amspi.stop_dc_motors(push_motor)

    def motor_fetch():
        #fetch the disk
        amspi.run_dc_motors(push_motor, clockwise=True)
        time.sleep(5)
        amspi.stop_dc_motors(push_motor)


    def conveyer_belt():
        #read color sensor value and call bucket_sorter with the propper signal
        amspi.run_dc_motors(conveyer_belt)
        time.sleep(5)
        amspi.stop_dc_motors(conveyer_belt)

    def color_sensor():
        pass
    def bucket_sorter():
         pass

#constantly listen for motion
while True:
    # listen for motion
    motion = read_motion()

    # When motion is sensed
    if motion:
        #we only keep listening for motion when the disk is processed
        time.sleep(5)
        motor_fetch()
        conveyer_belt()
        bucket_sorter()
        #Reset the fetching mechanism to its initial position when track is clear
        while True:
             motion = read_motion()
             if motion == 0:
                  reset_pushing_mechanism()
                  break

