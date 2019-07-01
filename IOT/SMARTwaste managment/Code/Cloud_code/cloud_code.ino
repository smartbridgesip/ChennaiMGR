#include <ESP8266WiFi.h>
#include <PubSubClient.h>


const char* ssid = "neww";
const char* password = "12345678";


#define ORG "3j9cvj"
#define DEVICE_TYPE "SmartDustbin"
#define DEVICE_ID "12345"
#define TOKEN "123456789"

char server[] = ORG ".messaging.internetofthings.ibmcloud.com";
char topic[] = "iot-2/cmd/home/fmt/String";
char authMethod[] = "use-token-auth";
char token[] = TOKEN;
char clientId[] = "d:" ORG ":" DEVICE_TYPE ":" DEVICE_ID;

const char eventTopic[] = "iot-2/evt/status/fmt/json";
const char cmdTopic[] = "iot-2/cmd/led/fmt/json";

const int trigPin = D4;  //D4
const int echoPin = D3;  //D3                        
long duration;
int distance;
String command;

WiFiClient wifiClient;

void callback(char* topic, byte* payload, unsigned int payloadLength) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < payloadLength; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();
}

PubSubClient client(server, 1883, callback, wifiClient);

int publishInterval = 5000; 
long lastPublishMillis;

void setup() {
  Serial.begin(115200); Serial.println();
  pinMode(D1,OUTPUT);
  pinMode(D0,OUTPUT);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  wifiConnect();
  mqttConnect();
}

void loop() {
  if (millis() - lastPublishMillis > publishInterval) {
    publishData();
    lastPublishMillis = millis();
  }
  
  
  if (!client.loop()) {
    mqttConnect();
  }

   if(distance<5){
    digitalWrite(D0,HIGH);
   delay(2000);
    }
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
  while (!!!client.connected()) {
    Serial.print("Reconnecting MQTT client to "); Serial.println(server);
    if (!!!client.connect(clientId, authMethod, token)) {
      Serial.print(".");
      delay(500);
    }
    if (client.subscribe(cmdTopic)) {
      Serial.println("subscribe to responses OK");
    } else {
      Serial.println("subscribe to responses FAILED");
    }
    Serial.println();
  }
}

void publishData() {
  
        
    digitalWrite(trigPin, HIGH);
    delayMicroseconds(1000);
    digitalWrite(trigPin, LOW);
    duration = pulseIn(echoPin, HIGH);
    distance= duration*0.034/2;
    Serial.print("Distance: ");
    Serial.println(distance);

   

        
     String payload = "{\"d\":{\"adc\":";
  payload += String(distance);
  payload += "}}";

  Serial.print("Sending payload: "); Serial.println(payload);

  if (client.publish(eventTopic, (char*) payload.c_str())) {
    Serial.println("Publish OK");
  } else {
    Serial.println("Publish FAILED");
  }
}

void initManagedDevice() {
  if (client.subscribe(topic)) {
    Serial.println("subscribe to cmd OK");
  } else {
    Serial.println("subscribe to cmd FAILED");
  }
}

void callbacks(char* topic, byte* payload, unsigned int payloadLength) {
  Serial.print("callback invoked for topic: "); Serial.println(topic);

  for (int i = 0; i < payloadLength; i++) {
    //Serial.println((char)payload[i]);
    command += (char)payload[i];
  }
Serial.println(command);
if(command == "LIGHTON"){
  digitalWrite(D1,HIGH);
  Serial.println("Light is Switched ON");
}
else if(command == "LIGHTOFF"){
  digitalWrite(D1,LOW);
  Serial.println("Light is Switched OFF");
}

command ="";
}
