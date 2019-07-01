#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <SoftwareSerial.h>
const char* ssid = "Nokia 6";
const char* password = "gopileela";

#define ORG "r0fe4x"
#define DEVICE_TYPE "light"
#define DEVICE_ID "1234"
#define TOKEN "12345678"
String command;
int sensorPin = A0;
int sensorValue = 0;

char server[] = ORG ".messaging.internetofthings.ibmcloud.com";
char topic[] = "iot-2/cmd/home/fmt/String";
char authMethod[] = "use-token-auth";
char token[] = TOKEN;
char clientId[] = "d:" ORG ":" DEVICE_TYPE ":" DEVICE_ID;
//Serial.println(clientID);
void callback(char* topic, byte* payload, unsigned int payloadLength);
WiFiClient wifiClient;
PubSubClient client(server, 1883, callback, wifiClient);
void setup() {
  Serial.begin(115200);
  Serial.println();
  pinMode(D1,OUTPUT);
  pinMode(D2,OUTPUT);
  pinMode(D3,OUTPUT);
  wifiConnect();
  mqttConnect();
}

void loop() {
  
  if (!client.loop()) {
    mqttConnect();
  }
delay(100);
}

void wifiConnect() {
  Serial.print("Connecting to "); Serial.print(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.print("nWiFi connected, IP address: "); Serial.println(WiFi.localIP());
}

void mqttConnect() {
  if (!client.connected()) {
    Serial.print("Reconnecting MQTT client to "); Serial.println(server);
    while (!client.connect(clientId, authMethod, token)) {
      Serial.print(".");
      delay(500);
    }
    initManagedDevice();
    Serial.println();
  }
}
void initManagedDevice() {
  if (client.subscribe(topic)) {
    Serial.println("subscribe to cmd OK");
  } else {
    Serial.println("subscribe to cmd FAILED");
  }
}

void callback(char* topic, byte* payload, unsigned int payloadLength) {
  Serial.print("callback invoked for topic: "); Serial.println(topic);

  for (int i = 0; i < payloadLength; i++) {
    //Serial.println((char)payload[i]);
    command += (char)payload[i];
  }
Serial.println(command);
if(command == "LIGHT1ON"){
  digitalWrite(D1,HIGH);
  Serial.println("Light is Switched ON");
}
else if(command == "LIGHT1OFF"){
  digitalWrite(D1,LOW);
  Serial.println("Light is Switched OFF");
}
if(command == "LIGHT2ON"){
  digitalWrite(D2,HIGH);
  Serial.println("Light is Switched ON");
}
else if(command == "LIGHT2OFF"){
  digitalWrite(D2,LOW);
  Serial.println("Light is Switched OFF");
}
if(command == "LIGHT3ON"){
  digitalWrite(D3,HIGH);
  Serial.println("Light is Switched ON");
}
else if(command == "LIGHT3OFF"){
  digitalWrite(D3,LOW);
  Serial.println("Light is Switched OFF");
}
else if(command == "AUTOMATIC"){
  sensorValue = analogRead(sensorPin);

  Serial.println(sensorValue);
  if(sensorValue>800){
     
digitalWrite(D1,HIGH);
digitalWrite(D2,HIGH);
digitalWrite(D3,HIGH);
     
    Serial.println("Light is Swithed ON");
    delay(1000);
  }
  else if(sensorValue<=800)
  {
    digitalWrite(D1,LOW);
    digitalWrite(D2,LOW);
    digitalWrite(D3,LOW);
    Serial.println("Light is Swithed OFF");
    delay(sensorValue);
    
  }
}

command ="";

}
