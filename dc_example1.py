#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
   Servo Example - Example of usage ASMpi class
.. Licence MIT
.. codeauthor:: Jan Lipovský <janlipovsky@gmail.com>, janlipovsky.cz
"""

from AMSpi import AMSpi
import time

black = 1
white = 0
other = 0
last_disk = 'black'

if __name__ == '__main__':
    # Calling AMSpi() we will use default pin numbering: BCM (use GPIO numbers)
    # if you want to use BOARD numbering do this: "with AMSpi(True) as amspi:"
    with AMSpi() as amspi:
        
        # Set PINs for controlling shift register (GPIO numbering)
        
        amspi.set_74HC595_pins(21, 20, 16)
        
        # Set PINs for controlling all 4 motors (GPIO numbering)
        
        amspi.set_L293D_pins(5, 6, 13, 19)

        if black == 1:
            


            print("GO: clockwise with 50% of maximum speed")
            amspi.run_dc_motors([amspi.DC_Motor_1], speed=52)
            print("Stop")
            amspi.stop_dc_motors([amspi.DC_Motor_1])
            time.sleep(2)