

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
        
        if (data == 'M')
        {
          // start fetching
            delay(6500);
            fetching_motor.setSpeed(speed(100)); 
            fetching_motor.run(FORWARD);
            delay(1000);
            fetching_motor.run(RELEASE);
            
          //start conveyer belt
            delay(2000);  
            belt_motor.setSpeed(speed(50));
            belt_motor.run(BACKWARD);
            delay(3000);
            belt_motor.run(RELEASE);
            delay(7000);
          //get data about color and send info to bucket sorting mechanism
            delay(1000);
           // char color = Serial.read();
          //rotate bucket motor
            if (color = 'B')
//            {
//              if (last_disk == 'W') {
//                rotate_bucket();
//              }
//              last_disk = 'B';
//            } 
//            else if (color = 'W') {
//              if (last_disk == 'B') {
//                rotate_bucket();
//              }
//              last_disk = 'W';
//            } else {
//              //halt
//            }
            rotate_bucket();
          //continue belt
            belt_motor.setSpeed(speed(100));
            belt_motor.run(BACKWARD);
            delay(5000);
            belt_motor.run(RELEASE);
            
          //after fetching is done send info to pi
            Serial.println("check if track is clear");
            while (motion == true)
            {
              if (Serial.available > 0 ) {
                char ready = Serial.read();
                if (ready == 'G')
                {
                  motion == false;
                }
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
  bucket_motor.setSpeed(speed(100));
  bucket_motor.run(FORWARD);
  delay(2650);
  bucket_motor.run(RELEASE);
}
int  speed(int percent)
{
  return map(percent, 0, 100, 0, 255);
}
