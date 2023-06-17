

#include <AFMotor.h>

AF_DCMotor fetching_motor(1);
AF_DCMotor belt_motor(2);
AF_DCMotor bucket_motor(3);
AF_DCMotor motor4(4);

void setup() {
    Serial.begin(9600);
}

void loop() {
      if(Serial.available() > 0)
      {
        motor4.setSpeed(speed(100));
        motor4.run(FORWARD);
        char data = Serial.read();
        bool motion = true;
        bool color_recieved = false;
        
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
            color = Serial.read();
            if (color = 'B')
            {//rotate bucket motor
            } else if (color = 'W')
            {
              
            } else {
              //halt
            }
          //continue belt
            belt_motor.setSpeed(speed(100));
            belt_motor.run(BACKWARD);
            delay(5000);
            belt_motor.run(RELEASE);
        //rotate bucket
        /////
            //after fetching is done send info to pi
            Serial.println("check if track is clear");
            while (motion == true)
            {
              String ready = Serial.read();
              if (ready == 'G')
              {
                motion == false;
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



int  speed(int percent)
{
  return map(percent, 0, 100, 0, 255);
}
