#include <ESP8266WiFi.h>--------

#include <ESP8266HTTPClient.h>
#include <ESP8266WiFi.h>--------

#include <ESP8266HTTPClient.h>

#include <SPI.h>
 #include <RFID.h>
#define SS_PIN D4
#define RST_PIN D3
 const char* ssid = "Cse Dept";
const char* password = "Csedept@789";

WiFiClient wifiClient;//to publish client
 
 
#include <PubSubClient.h>

  
  RFID rfid(SS_PIN,RST_PIN);
  int serNum[5];
  

  String cancat_card = " ";
  #include <Wire.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_GFX.h>
#define SSD1306_LCDHEIGHT 64

// OLED display TWI address
#define OLED_ADDR   0x3C

Adafruit_SSD1306 display(-1);

#if (SSD1306_LCDHEIGHT != 64)
#error("Height incorrect, please fix Adafruit_SSD1306.h!");
#endif

void setup() 
    {
              Serial.begin(115200);
               Serial.println();
              SPI.begin();
              rfid.init();
              Serial.print("Connecting to ");
 Serial.print(ssid);
 WiFi.begin(ssid, password);
 while (WiFi.status() != WL_CONNECTED) {
  //HTTPClient http;  //Declare an object of class HTTPClient
 delay(500);
 Serial.print(".");
 } 
 Serial.println("");
 
 Serial.print("WiFi connected, IP address: ");
 Serial.println(WiFi.localIP());

  pinMode(D0,OUTPUT);
  pinMode(D8,OUTPUT);
             }

  void loop()
      {
           if(rfid.isCard()){
                              if(rfid.readCardSerial()){
                                       
                                      cancat_card = String(rfid.serNum[0])+String(rfid.serNum[1])+String(rfid.serNum[2])+String(rfid.serNum[3])+String(rfid.serNum[4]);
                                      Serial.println(cancat_card);
                                      //Serial.println("Requesting .......");
                          
                                  
 
delay(100);
}

 HTTPClient http;  //Declare an object of class HTTPClient
 
 
http.begin("http://billsystem.eu-gb.mybluemix.net/search?id="+ cancat_card);
 

int httpCode = http.GET();                                                                  //Send the request
  //Serial.println("Response from Server");
String payload = http.getString();   //Get the request response payload
Serial.println(payload);                     //Print the response payload

int pos;

if(payload=="valid"){

   digitalWrite(D8,HIGH);
  delay(100);
   digitalWrite(D0,LOW);
  delay(100);

    display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR);
  display.clearDisplay();//clears display
  

  
// display a line of text
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0,10);//(x,y)
  display.print("Access Granted!!");
 
 
  // update display with all of the above graphics
  display.display();//displayed in OLED
}
else{

   digitalWrite(D0,HIGH);
  delay(100);
   digitalWrite(D8,LOW);
  delay(100);
    display.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR);
  display.clearDisplay();//clears display
  

  
// display a line of text
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.setCursor(0,10);//(x,y)
  display.print("Access Denied!!");
 
 
  // update display with all of the above graphics
  display.display();//displayed in OLED
    
}

http.end();   //Close connection         
 

 
      }
     

    rfid.halt();
     
 
 }
      
 
