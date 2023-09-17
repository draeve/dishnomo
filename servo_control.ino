
/*#include <Arduino.h>
#include <Servo.h>
#include <ESP8266WiFi.h> //wifi library
#include <ESP8266WebServer.h>

Servo s1;
int angle = 0;
//int previousButtonState = LOW;
//int currentButtonState = LOW;
unsigned long lastDebounceTime = 0;
const long debounceDelay = 50; // Adjust debounce delay as needed

//wifi stuff
const char* ssid = "HackTheNorth";
const char* password = "HTNX2023";
ESP8266WebServer server(80);//server


enum State { ANGLE_0, ANGLE_180 };
State currentState = ANGLE_0;

const int buttonPin = D1;
int receivedValue = 0; //storing value sent over wifi
//0 = open
// 1 = closed
void setup() {
  s1.attach(D3);  // Attach servo to D3 pin
  pinMode(buttonPin, INPUT_PULLUP); // Enable internal pull-up resistor for button
  s1.write(angle); // Initialize servo angle to 0 degrees
  pinMode(LED_BUILTIN,OUTPUT);

  //setting wifi, starting serial communication
  Serial.begin(115200);
  delay(10);
  Serial.println('\n');

  WiFi.begin(ssid,password);
  Serial.print("Connecting to: ");
  Serial.print(ssid); Serial.print(' ');
  int i =0;
  while(WiFi.status()!=WL_CONNECTED){ //waiting for wifi to connect
    delay(1000);
    Serial.print(++i); Serial.print(' ');
  }
  Serial.println('\n');
  Serial.println("Connection established");
  Serial.print("ip address:\t" );
  Serial.print(WiFi.localIP());

  //setup http server
  server.on("/setServoPos",HTTP_POST, handleServo); //define post request handler
  server.begin();

}

void handleServo(){
  if (server.hasArg("value")){
    receivedValue = server.arg("value").toInt();
    //Serial.println(receivedValue);
  }
  server.send(200,"text/plain","Success");
}

void loop() {
  /*if (receivedValue == 42){
      Serial.print("Received value: "+receivedValue);
  */
//wifi stuff
/*
  server.handleClient();
    //Serial.println("ReceivedValue: "+receivedValue);
    //Serial.println("CurrentState: "+currentState );
   if (receivedValue == 0 && currentState == ANGLE_180){
    s1.write(0);
    currentState = ANGLE_0;
    digitalWrite(LED_BUILTIN,HIGH);
    }
    if (receivedValue == 1 && currentState == ANGLE_0){
      s1.write(180);
      currentState = ANGLE_180;
      digitalWrite(LED_BUILTIN,LOW);
    }
    */

/*
  // Read the button state with debounce
  int reading = digitalRead(buttonPin);
  if (reading != previousButtonState) {
    lastDebounceTime = millis();
  }
  if ((millis() - lastDebounceTime) > debounceDelay) {
    if (reading != currentButtonState) {
      currentButtonState = reading;

      if (currentButtonState == LOW) {
        // Button is pressed
        if (currentState == ANGLE_0) {
          // Transition to 180 degrees
          s1.write(180);
          currentState = ANGLE_180;
          digitalWrite(LED_BUILTIN,LOW);
        } else {
          // Transition to 0 degrees
          s1.write(0);
          currentState = ANGLE_0;
          digitalWrite(LED_BUILTIN,HIGH);
        }
      }
    }
  }
  */
//receivedValue = 0;
//previousButtonState = reading;
//}


#include <Arduino.h>
#include <Servo.h>
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

Servo s1;
int angle = 0;
//open = 0
//closed = 180

const char* ssid = "HackTheNorth";
const char* password = "HTNX2023";
ESP8266WebServer server(80);

enum State { ANGLE_0,
             ANGLE_180 };
State currentState = ANGLE_0;

const int buttonPin = D1;
int receivedValue = -1;  // Initialize to an invalid value

void setup() {
  s1.attach(D3);
  pinMode(buttonPin, INPUT_PULLUP);
  s1.write(angle);
  pinMode(LED_BUILTIN, OUTPUT);

  Serial.begin(115200);
  delay(10);
  Serial.println('\n');

  WiFi.begin(ssid, password);
  Serial.print("Connecting to: ");
  Serial.print(ssid);
  Serial.print(' ');
  int i = 0;
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(++i);
    Serial.print(' ');
  }
  Serial.println('\n');
  Serial.println("Connection established");
  Serial.print("IP address: ");
  Serial.print(WiFi.localIP());

  server.on("/setAngle", HTTP_POST, handleSetAngle);
  server.begin();
}

void loop() {
  if (receivedValue != -1) {
    if (receivedValue != angle) {
      //Serial.println("rotating servo \"apparently\"");
      s1.write(receivedValue);
      angle = receivedValue;
      digitalWrite(LED_BUILTIN, LOW);
    }
    receivedValue = -1;
  }

  server.handleClient();

  // Rest of your loop code (if needed)
}

void handleSetAngle() {
  if (server.hasArg("value")) {
    int newValue = server.arg("value").toInt();
    if (newValue == 0 || newValue == 180) {
      Serial.print("Received value: ");
      Serial.println(newValue);
      receivedValue = newValue;
      server.send(200, "text/plain", "OK");
    } else {
      server.send(406, "text/plain", "Invalid angle");
    }
  } else {
    server.send(400, "text/plain", "Bad Request");
  }
}
