#include <HTTPClient.h>
#include <WiFi.h>
#include <Arduino_JSON.h>

bool hasError = false;
bool firstLoop = true;


void setup() 
{
  //setup serial
  const long bitRate = 115200;
  Serial.begin(bitRate); 
  
  //setup wifi
  setupWifi(); 
}


void loop()
{ 
  static String city = "Porto";
  static String countryCode = "PT";
  static String openWeatherMapApiKey = "16162bdd1ddfb16357b5a37724505b31";

  // executes once 
  if (firstLoop)
  {
    // check Wifi connection
    if(WiFi.status() != WL_CONNECTED )
    {
      hasError = true;
      return;
    }
    
    // create http request
    String weatherRequest = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "," + countryCode + "&APPID=" + openWeatherMapApiKey;
  
    //send http request and get Json object
    String requestOutput = httpGETRequest(weatherRequest.c_str());
    
    // display Json
    Serial.println(requestOutput);
    JSONVar myObject = JSON.parse(requestOutput);
    
  
    if (JSON.typeof(myObject) == "undefined") {
      Serial.println("Parsing input failed!");
      return;
    }
  
    Serial.print("JSON object = ");
    Serial.println(myObject);
    Serial.print("Temperature: ");
    Serial.println(myObject["main"]["temp"]);
    Serial.print("Pressure: ");
    Serial.println(myObject["main"]["pressure"]);
    Serial.print("Humidity: ");
    Serial.println(myObject["main"]["humidity"]);
    Serial.print("Wind Speed: ");
    Serial.println(myObject["wind"]["speed"]);
    
    firstLoop = false;
  }
   
  
  
}


void setupWifi()
{ 
  //initialize network settings
  
  const char* ssid = "Galaxy A40BFB5";
  const char* password = "qoew9678";
  WiFi.begin(ssid, password);
  
  Serial.println("Connecting");
  waitUntilWifiConnected();
}

void waitUntilWifiConnected()
{ 
  int attemptsLeft = 10;
  
  while(WiFi.status() != WL_CONNECTED && attemptsLeft != 0) 
  {
    delay(500);
    Serial.print(".");
    -- attemptsLeft;
  }

  Serial.println("");
  
  if(WiFi.status() != WL_CONNECTED)
  {
    hasError = true;
    Serial.println("Wifi connection impossible");
  }
  else
  {
    Serial.print("Connected to WiFi network with IP Address: ");
    Serial.println(WiFi.localIP());
  }
}


String httpGETRequest(const char* serverName) {
  WiFiClient client;
  HTTPClient http;
    
  // Your Domain name with URL path or IP address with path
  http.begin(client, serverName);
  
  // Send HTTP POST request
  int httpResponseCode = http.GET();
  
  String payload = "{}"; 
  
  if (httpResponseCode>0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    payload = http.getString();
  }
  else {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
  }
  // Free resources
  http.end();

  return payload;
}
