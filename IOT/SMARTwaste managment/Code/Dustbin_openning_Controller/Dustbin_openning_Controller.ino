#include <CapacitiveSensor.h>
#include<Servo.h>
#include<stdio.h>

Servo myservo;
Servo myservo2;
int sensorVal;
int pos = 0;
int pos2=0;

void setup(){
  //configure pin2 as an input and enable the internal pull-up resistor
  pinMode(2, INPUT_PULLUP);
  myservo.attach(8);
  myservo2.attach(7);
  pinMode(11, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);
}

void loop(){

  sensorVal = digitalRead(2);
  // The Logic is inverted a low on pin 2 means a sinking switch is activated
  // and a high on pin 2 means the switch is unactivated and pulled up by the internal resistor
  // this is not a problem since the controller can interpret the data any way we tell it to

  if (sensorVal == HIGH) {

  // attaches the servo on pin 9 to the servo object
      myservo2.write(90); // move the servo to 180 degrees.
      delay(100);         // tell servo to go to position in variable 'pos'
                               // waits 15ms for the servo to reach the position
  
      myservo.write(0); // move the servo to 180 degrees.
      delay(100);

    //for (pos2 = 90; pos2 >= 0; pos2 -= 1) { // goes from 180 degrees to 0 degrees
   // myservo2.write(pos2);  
    
   // delay(20);// tell servo to go to position in variable 'pos'
   // }
  
    digitalWrite(11, LOW);
    digitalWrite(12, HIGH);
    noTone(13);


  } 

  else { //sensorVal = LOW

      myservo2.write(0); // move the servo to 180 degrees.
      delay(100);         // tell servo to go to position in variable 'pos'

      myservo.write(90); // move the servo to 180 degrees.
      delay(100);    

   
    digitalWrite(11, HIGH);
    digitalWrite(12, LOW);
    tone(13,1000);
    
  }
}

