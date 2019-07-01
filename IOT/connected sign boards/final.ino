#include <ESP8266WiFi.h>--------
#include <PubSubClient.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <DHT.h>
#include <ESP8266HTTPClient.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels
// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

#define DHTPIN D3    // Digital pin connected to the DHT sensor

// Uncomment the type of sensor in use:
#define DHTTYPE    DHT11     // DHT 11
//#define DHTTYPE    DHT22     // DHT 22 (AM2302)
//#define DHTTYPE    DHT21     // DHT 21 (AM2301)

DHT dht(DHTPIN, DHTTYPE);
 
//-------- Customise these values -----------
const char* ssid = "naveen prakash";
const char* password = "shivanii";

 
#define ORG "aa6ixo"
#define DEVICE_TYPE "meow"
#define DEVICE_ID "14062502"
#define TOKEN "14062502"
//-------- Customise the above values --------
 
char server[] = ORG ".messaging.internetofthings.ibmcloud.com";
char topic[] = "iot-2/evt/Data/fmt/json";
char authMethod[] = "use-token-auth";
char token[] = TOKEN;
char clientId[] = "d:" ORG ":" DEVICE_TYPE ":" DEVICE_ID;
 
WiFiClient wifiClient;
PubSubClient client(server, 1883,wifiClient);

void setup() {
 Serial.begin(115200);
 Serial.println();
 dht.begin();
 Serial.print("Connecting to ");
 Serial.print(ssid);
 WiFi.begin(ssid, password);
 while (WiFi.status() != WL_CONNECTED) {
 delay(500);
 Serial.print(".");
 } 
 Serial.println("");
 
 Serial.print("WiFi connected, IP address: ");
 Serial.println(WiFi.localIP());

 
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("SSD1306 allocation failed"));
    for(;;);
  }
  delay(2000);
  display.clearDisplay();
  display.setTextColor(WHITE);

}
 
void loop() {
float h = dht.readHumidity();
float t = dht.readTemperature();

if (isnan(h) || isnan(t))
{
Serial.println("Failed to read from DHT sensor!");
delay(1000);
return;
}
PublishData(t,h);
delay(100);
}

void PublishData(float temp, float humid){
 if (!!!client.connected()) {
 Serial.print("Reconnecting client to ");
 Serial.println(server);
 while (!!!client.connect(clientId, authMethod, token)) {
 Serial.print(".");
 delay(500);
 }
 Serial.println();
 }

 display.clearDisplay();
  
  // display temperature
  display.setTextSize(1);
  display.setCursor(0,0);
  display.print("Temperature: ");
  display.setTextSize(1);
  display.setCursor(0,10);
  display.print(temp);
  display.print(" ");
  display.setTextSize(1);
  display.cp437(true);
  display.write(167);
  display.setTextSize(1);
  display.print("C");
  
  // display humidity
  display.setTextSize(1);
  display.setCursor(0, 35);
  display.print("Humidity: ");
  display.setTextSize(1);
  display.setCursor(0, 45);
  display.print(humid);
  display.print(" %"); 
  
  display.display(); 
  delay(2000);

 display.clearDisplay();
  
  // display temperature
  display.setTextSize(1);
  display.setCursor(0,0);
    display.print("Speed Limit: ");
  display.setTextSize(2);
  display.setCursor(0,10);
  display.print("50KM/HR");
  display.print(" ");

  display.display(); 
  delay(2000);

  HTTPClient http;  //Declare an object of class HTTPClient
 
http.begin("http://nashi.eu-gb.mybluemix.net/oled");  //Specify request destination
int httpCode = http.GET();                                                                  //Send the request
 
 
String payload1 = http.getString();   //Get the request response payload
Serial.println(payload1);                     //Print the response payload
 
 
http.end();   //Close connection
 

 
delay(3000);    //Send a request every 30 seconds

 display.clearDisplay();
  
  // display temperature
  display.setTextSize(2);
  display.setCursor(0,10);
  display.print(payload1);
  display.print(" ");

  display.display(); 
  delay(2000);
 
  String payload = "{\"d\":{\"temperature\":";
  payload += temp;
  payload+="," "\"humidity\":";
  payload += humid;
  payload += "}}";
 Serial.print("Sending payload: ");
 Serial.println(payload);
 
  
 if (client.publish(topic, (char*) payload.c_str())) {
 Serial.println("Publish ok");
 } else {
 Serial.println("Publish failed");




 delay(5000);

  //read temperature and humidity
  float t = dht.readTemperature();
  float h = dht.readHumidity();

  if (isnan(h) || isnan(t)) {
    Serial.println("Failed to read from DHT sensor!");
  }
  // clear display

 
}
 }
