#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include "RTClib.h"
#include <Wire.h>
 
const char* ssid = "Cresencia";
const char* password = "56755675";
WiFiClient wifiClient;
HTTPClient http; 

String str;
String payload;
String gm;
String ga;
String gn;
RTC_DS1307 RTC;


void setup() {
  // put your setup code here, to run once:
  pinMode(D3,INPUT);
  pinMode(D4,OUTPUT);
  pinMode(D5,OUTPUT);
  pinMode(D6,OUTPUT);
  pinMode(D7,OUTPUT);

 Serial.begin(115200);
 Serial.println();
 Serial.print("Connecting to ");
 Serial.print(ssid);
 WiFi.begin(ssid, password);
 while (WiFi.status() != WL_CONNECTED)
 {
 delay(500);
 Serial.print(".");
 } 
 Serial.println("");
 Serial.print("WiFi connected, IP address: ");
 Serial.println(WiFi.localIP());
  
 
    Wire.begin();
    RTC.begin();
  if (! RTC.isrunning())
  {
    Serial.println("RTC is NOT running!");
    // following line sets the RTC to the date & time this sketch was compiled
    RTC.adjust(DateTime(__DATE__, __TIME__));
    RTC.adjust(DateTime(2019,6,21,9,58,0));
  }

Serial.println("Requesting ......."); 
http.begin("http://rinsyiot.eu-gb.mybluemix.net/data");  //Specify request destination
int httpCode = http.GET();                                                                  //Send the request
String payload = http.getString();   //Get the request response payload
Serial.println(payload); //Print the response payload
gm = payload;
delay(2000);
 
http.begin("http://rinsyiot.eu-gb.mybluemix.net/data2"); 
int httpCode_2 = http.GET(); //Send the request
String payload2 = http.getString();   //Get the request response payload
Serial.println(payload2);                     //Print the response payload
ga = payload2;
delay(2000);
  
http.begin("http://rinsyiot.eu-gb.mybluemix.net/data3");  
int httpCode_3= http.GET(); //Send the request
String payload3 = http.getString();   //Get the request response payload
Serial.println(payload3);                     //Print the response payload
gn = payload3;
http.end();   //Close connection
delay(2000); 

}

void loop() {
  // put your main code here, to run repeatedly:

  DateTime now = RTC.now();
  str = (String(now.hour(),DEC)+String(now.minute(),DEC));
  Serial.println (str);  
  delay(1000);
  if(gm == str || ga == str || gn == str)
{
  digitalWrite(D4,HIGH);
  delay(1000);
  digitalWrite(D4,LOW);
  delay(1000);
} 
if(gm == str)
{
  digitalWrite(D5,HIGH);
  delay(1000);
  digitalWrite(D5,LOW);
  delay(1000);
} 
if(ga == str)
{
  digitalWrite(D6,HIGH);
  delay(1000);
  digitalWrite(D6,LOW);
  delay(1000);
} 
if(gn == str)
{
  digitalWrite(D7,HIGH);
  delay(1000);
  digitalWrite(D7,LOW);
  delay(1000);
} 

}   
