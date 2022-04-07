/*
 * Ce programme permet de controller un robot grâce à une connexion WiFi.
 * Le robot utilise des codeurs optiques pour calculer sa position.
 * 
 * Le programme utilise deux interruptions pour gérer les informations capteur.
 * 
 * REMARQUE : le port UART est ouvert le temps de donner l'adresse IP du serveur.
 */


#include <WiFi.h>
#include <WiFiServer.h>
#include <WiFiClient.h>
#include <HTTPClient.h>

//######################################
//##                                  ##
//##           DEFINITION             ##
//##                                  ##
//######################################

//roue 1
#define D1 32
#define D3 33
//roue 2
#define D2 26
#define D4 27

//Capteur detection de ligne
#define C1 14
#define C2 4
#define C3 18
#define C4 19


//######################################
//##                                  ##
//##            VARIABLES             ##
//##                                  ##
//######################################

// Reglage de la connexion :
WiFiServer server(80);
WiFiClient client;
//const char *ssid     = "IMERIR_IoT";
//const char *password = "kohWoong5oox";
String demande_client;

//URL de l'API
String serverName = "http://10.3.3.131:8000";

//mesure de temps
unsigned long lastTime = 0;
//Intervalle de 5 seconde
unsigned long timerDelay = 5000;



//######################################
//##                                  ##
//##         VOID DIRECTION           ##
//##                                  ##
//######################################


 
//######################################
//##                                  ##
//##             SETUP                ##
//##                                  ##
//######################################

void setup()
{
  // Reglage du port UART :
  Serial.begin(115200);

  ////////////////////////////////
  // Connection au wifi :  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)  // Tant que le module n'est pas connecte
  {
    delay(1000);
    Serial.print(".");
  }

  
  // Affichage de adresse IP sur le moniteur serie :
  Serial.println("\n adresse IP ESP32: ");
  Serial.println(WiFi.localIP());

  ///////////////////////////////
}


//######################################
//##                                  ##
//##             LOOP                 ##
//##                                  ##
//######################################

void loop()
{
  /*
   * DEPLACEMENT DE LA VOITURE
   * 
   */

  Serial.println(millis() - lastTime);
  Serial.println(timerDelay);
  if ((millis() - lastTime) > timerDelay/20) {
    //Vérification connection WIFI
    if(WiFi.status()== WL_CONNECTED){
      Serial.println("Connect");
      HTTPClient http;
      String serverPath = serverName + "/paquets/";

      // Connection communication API
      http.begin(serverPath.c_str());
    Serial.println(serverPath.c_str());
      Serial.println("avant get");
      int httpResponseCode = http.GET();

      // recoit reponse de l'API ou les erreur de connextion comme l'erreur "404"
      if (httpResponseCode>0) {
        Serial.print("HTTP Response code: ");
        Serial.println(httpResponseCode);
        String payload = http.getString();
        Serial.println(payload);
      }
      // Erreur dans la reception du message
      else {
        Serial.print("Error code: ");
        Serial.println(httpResponseCode);
      }

      // Free resources
      http.end();
    }
    else {
      Serial.println("WiFi Disconnected");
    }
  }
    lastTime = millis();
      
   ///////////
  
  delay(500);
}
