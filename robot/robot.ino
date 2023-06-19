

#include <AFMotor.h>

AF_DCMotor fetching_motor(1);
AF_DCMotor belt_motor(2);
AF_DCMotor bucket_motor(4);


char last_disk = 'B';
void setup() {
    Serial.begin(9600);
}

void loop() {
      if(Serial.available() > 0)
      {
        char data = Serial.read();
        bool motion = true;
        bool color_received = false;
        
        if (data == 'M')
        {
          // start fetching
            delay(6500);
            fetching_motor.setSpeed(speed(50)); 
            fetching_motor.run(FORWARD);
            delay(1000);
            fetching_motor.run(RELEASE);
            
          //start conveyer belt
            delay(2000);  
            belt_motor.setSpeed(speed(50));
            belt_motor.run(BACKWARD);
            delay(2200);
            belt_motor.run(RELEASE);
         //Tell pi to detect and send the color detected
            Serial.println("Detect color");
            delay(7000);
         //get data about color and send info to bucket sorting mechanism
            while (color_received == false)
            {
              if (Serial.available() > 0)
              {
                char color = Serial.read();
                if (color == 'B')
                {
                  if (last_disk == 'W') {
                    rotate_bucket();
                  }
                  last_disk = 'B';
                } 
                else if (color == 'W') {
                  if (last_disk == 'B') {
                    rotate_bucket();
                  }
                  last_disk = 'W';
                } else {
                  halt();
                }
                color_received = true;
              }
            }
            
          //continue belt
            belt_motor.setSpeed(speed(100));
            belt_motor.run(BACKWARD);
            delay(5000);
            belt_motor.run(RELEASE);
            
          //after fetching is done send info to pi
            Serial.println("Check if track is clear");
            while (motion == true)
            {
              char ready = Serial.read();
              if (ready == 'G')
              {
                motion = false;
              }
            }
            
            //reset fetching mechanism
            fetching_motor.setSpeed(speed(100)); 
            fetching_motor.run(BACKWARD);
            delay(1000);
            fetching_motor.run(RELEASE);
        }
     }
}

void rotate_bucket()
{
  bucket_motor.setSpeed(speed(50));
  bucket_motor.run(FORWARD);
  delay(2750);
  bucket_motor.run(RELEASE);
}

int  speed(int percent)
{
  return map(percent, 0, 100, 0, 255);
}

void halt()
{
  while (true)
  {
    fetching_motor.run(RELEASE);
    belt_motor.run(RELEASE);
    belt_motor.run(RELEASE);
  }
}
