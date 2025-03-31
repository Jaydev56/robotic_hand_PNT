#include <Servo.h>

Servo thumbServo, thumbRestraintServo, indexServo, middleServo, ringServo, pinkyServo;
int indexPin = 8, middlePin = 7, ringPin = 6, pinkyPin = 5, thumbJointPin = 10, thumbRestraintPin = 9;
String receivedData = "";
int input_array_size = 8;

void setup() {
  Serial.begin(9600);
  thumbServo.attach(thumbJointPin);
  thumbRestraintServo.attach(thumbRestraintPin);
  indexServo.attach(indexPin);
  middleServo.attach(middlePin);
  ringServo.attach(ringPin);
  pinkyServo.attach(pinkyPin);
  
  thumbServo.write(0);
  indexServo.write(0);
  middleServo.write(0);
  ringServo.write(0);
  pinkyServo.write(0);
}

void moveServoSmooth(Servo &servo, int target) {
  int current = servo.read();
  if (current > target) {
    for (int i = current; i >= target; i--) {
      servo.write(i);
      delay(5);
    }
  } else {
    for (int i = current; i <= target; i++) {
      servo.write(i);
      delay(5);
    }
  }
}

void loop() {

  if (Serial.available()) {
    String data = Serial.readStringUntil('\n'); 
    Serial.print("Received Angles: ");
    Serial.println(data);  

    int angles[input_array_size];  
    int index = 0;
    char* ptr = strtok((char*)data.c_str(), ","); 
    while (ptr != NULL && index < input_array_size) {
      angles[index] = atoi(ptr); 
      ptr = strtok(NULL, ",");
      index++;
    }

    indexServo.write(180-angles[1]);
    middleServo.write(180-angles[2]);
    ringServo.write(180-angles[3]);
    pinkyServo.write(180-angles[4]);
    thumbServo.write(180-angles[0]);
    thumbRestraintServo.write(angles[5]);
  }
}



