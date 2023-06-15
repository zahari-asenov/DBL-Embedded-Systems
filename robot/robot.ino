

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
        char data = Serial.read();
        bool track_clear = false;
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
            belt_motor.setSpeed(speed(100));
            belt_motor.run(BACKWARD);
            delay(5000);
            belt_motor.run(RELEASE);
        }
     }
}



int  speed(int percent)
{
  return map(percent, 0, 100, 0, 255);
}
