// Include the Servo library 
#include <Servo.h> 
// Declare the Servo pin 
int servoPin = 9; 
int angle;
int pos;
// Create a servo object 
Servo servo; 

void setup() { 
   // We need to attach the servo to the used pin number 
   Serial.begin(115200);
   servo.attach(servoPin);  // attaches the servo on pin 9 to the servo object
   servo.write(0); 
   angle = 0;
   pos = 0;
}
void loop(){ 
   // Make servo go to 0 degrees 
  if (Serial.available() > 0) { 
    String x = Serial.readString(); 
    angle = x.toInt();
  }
  if(pos <= angle){
    for (pos = pos; pos <= angle; pos += 1) {
    // in steps of 1 degree
    servo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);                       // waits 15ms for the servo to reach the position
  }
  else{
    for (pos = pos; pos >= angle; pos -= 1) {
    servo.write(pos);              // tell servo to go to position in variable 'pos'
    delay(15);               // waits 15ms for the servo to reach the position
  }  
  } 