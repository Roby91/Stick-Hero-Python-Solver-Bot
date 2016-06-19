#include <Servo.h>

Servo myservo;
int i=0;
char buf[4];
int pos = 0;    // variable to store the servo position
int distanza = -1;
int msCalcolati = 0;



void setup() {
  Serial.begin(57600);
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
}
 
 
void loop() {
   
  //myservo.write(70);
  //myservo.write(80);
  
  while (Serial.available()) {
    
    buf[i]= Serial.read(); 
   
    //Serial.println(pos);
    
    if (int(buf[i])==13 || int(buf[i])==11 ){  //If Carriage return has been reached
     
      int result=atoi(buf);
      Serial.print("Numero letto: '");
      Serial.print(result);
      Serial.println("'");
      
      if (result<10000) {
        distanza = (int) result;
        
        // PROVA OFFSETT:
        distanza = distanza-9;
        
        if (distanza<100) {
          msCalcolati = (int) (distanza*1.2);
        } else if (distanza<150) {
          msCalcolati = (int) (distanza*1.32);
        } else if (distanza<170) {
          msCalcolati = (int) (distanza*1.42);
        } else if (distanza<220) {
          msCalcolati = (int) (distanza*1.54);
        } else if (distanza<250) {
          msCalcolati = (int) (distanza*1.6);
        } else if (distanza<300) {
          msCalcolati = (int) (distanza*1.7);
        } else if (distanza<369) {
          msCalcolati = (int) (distanza*1.75);
        } else {
          msCalcolati = (int) (distanza*1.8);
        }
      }
        
    for(int x=0;x<=4;x++){
      buf[x]=' ';
    }
    i=0;  //start over again
    } //if enter
     i++;    
         
  }
  
  
  
  if (distanza!=-1) {
    for(pos = 75; pos>=60; pos-=1)     // goes from 180 degrees to 0 degrees
    {                                
      myservo.write(pos);              // tell servo to go to position in variable 'pos'
      //delay(15);                       // waits 15ms for the servo to reach the position
      delay(5);                       // waits 15ms for the servo to reach the position
    }
    delay(msCalcolati);
    for(pos = 60; pos < 75; pos += 1)  // goes from 0 degrees to 180 degrees
    {                                  // in steps of 1 degree
      myservo.write(pos);              // tell servo to go to position in variable 'pos'
      //delay(15);                       // waits 15ms for the servo to reach the position   
      delay(5);                       // waits 15ms for the servo to reach the position   
    }
    distanza=-1;
  }     
  
  
    

     
}
  

