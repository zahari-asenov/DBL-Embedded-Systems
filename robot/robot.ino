

#include <AFMotor.h>

AF_DCMotor fetching_motor(1);
AF_DCMotor belt_motor(2);
AF_DCMotor bucket_motor(3);
AF_DCMotor motor4(4);

void setup() {
    Serial.begin(9600);
}

void loop() {
      String data = ReadData();
      bool track_clear = false;
      bool color_recieved = false;
      
      if (data == "motion")
      {
        delay(6500);
        fetch_disk();
        Serial.println("Fetched");
        run_belt();
        Serial.println("Conveyer belt running");
        
      }
   }

void fetch_disk()
{
  fetching_motor.setSpeed(speed(100)); 
  fetching_motor.run(FORWARD);
  delay(1000);
  fetching_motor.run(RELEASE);
}

void run_belt()
{
  belt_motor.setSpeed(speed(100));
  belt_motor.run(BACKWARD);
  delay(10000);
  belt_motor.run(RELEASE);
}

String ReadData() {
  String data = Serial.readStringUntil('\n');
  while (Serial.available() > 0) {
    Serial.read(); // Clear remaining characters in the serial buffer
  }
  return data;
}

int  speed(int percent)
{
  return map(percent, 0, 100, 0, 255);
}
