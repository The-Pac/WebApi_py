#include <WiFi.h>
#include <WiFiAP.h>
#include <WiFiMulti.h>
#include <WiFiUdp.h>
#include <WiFiScan.h>
#include <ETH.h>
#include <WiFiClient.h>
#include <WiFiSTA.h>
#include <WiFiServer.h>
#include <WiFiType.h>
#include <WiFiGeneric.h>


const char *ssid     = "******";
const char *password = "******";

void setup() {
  Serial.begin(115200);
  // put your setup code here, to run once:
Serial.println("Connected to server");
}

void loop() {

WiFi.mode(wifi_mode_t::WIFI_MODE_STA);
WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)  // Tant que le module n'est pas connecte
  {
    delay(1000);
    Serial.print(".");
  }
  

/*WiFiClient client;
if(client.connect(HOST_NAME, HTTP_PORT)) {
  Serial.println("Connected to server");
} else 
{
 Serial.println("connection failed");
}*/
  }
