import RPi.GPIO as GPIO
import time


def get_color():
  s2 = 23
  s3 = 24
  signal = 25
  NUM_CYCLES = 10


  def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(signal,GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(s2,GPIO.OUT)
    GPIO.setup(s3,GPIO.OUT)
    print("\n")





  def loop():
    temp = 1
    while(1):

      GPIO.output(s2,GPIO.LOW)
      GPIO.output(s3,GPIO.LOW)
      time.sleep(0.3)
      start = time.time()
      for impulse_count in range(NUM_CYCLES):
        GPIO.wait_for_edge(signal, GPIO.FALLING)
      duration = time.time() - start      #seconds to run for loop
      red  = NUM_CYCLES / duration   #in Hz
      print("red value - ",red)

      GPIO.output(s2,GPIO.LOW)
      GPIO.output(s3,GPIO.HIGH)
      time.sleep(0.3)
      start = time.time()
      for impulse_count in range(NUM_CYCLES):
        GPIO.wait_for_edge(signal, GPIO.FALLING)
      duration = time.time() - start
      blue = NUM_CYCLES / duration
      print("blue value - ",blue)

      GPIO.output(s2,GPIO.HIGH)
      GPIO.output(s3,GPIO.HIGH)
      time.sleep(0.3)
      start = time.time()
      for impulse_count in range(NUM_CYCLES):
        GPIO.wait_for_edge(signal, GPIO.FALLING)
      duration = time.time() - start
      green = NUM_CYCLES / duration
      print("green value - ",green)


      # Black disk conditions
      if 10000 <= red <= 12500 and 10000 <= blue <= 12500 and 9000 <= green <= 12500:
          print ("B")

      # White disk conditions
      elif 12000 <= red <= 25000 and 12000 <= blue <= 25000 and 12000 <= green <= 25000:
          print ("W")

      # No disk conditions
      elif 10000 <= red <= 12000 and 8500 <= blue <= 10500 and 8500 <= green <= 10500:
          print ("N")

      # If none of the conditions are met
      else:
          print ("U")
      time.sleep(2)



  def endprogram():
      GPIO.cleanup()

  if __name__=='__main__':

      setup()

      try:
          loop()

      except KeyboardInterrupt:
          endprogram()
