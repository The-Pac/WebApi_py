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



//######################################
//##                                  ##
//##            VARIABLES             ##
//##                                  ##
//######################################

// Reglage de la connexion :
WiFiServer server(80);
WiFiClient client;
const char *ssid     = "IMERIR_IoT";
const char *password = "kohWoong5oox";
String demande_client;

//Your Domain name with URL path or IP address with path
String serverName = "http://10.3.3.131:8000";

// the following variables are unsigned longs because the time, measured in
// milliseconds, will quickly become a bigger number than can be stored in an int.
unsigned long lastTime = 0;
// Timer set to 10 minutes (600000)
//unsigned long timerDelay = 600000;
// Set timer to 5 seconds (5000)
unsigned long timerDelay = 5000;




//######################################
//##                                  ##
//##             SETUP                ##
//##                                  ##
//######################################

void setup()
{
  // Reglage du port UART :
  Serial.begin(115200);

  
  // Connection au wifi :  
  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while (WiFi.status() != WL_CONNECTED)  // Tant que le module n'est pas connecte
  {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());

  
  // Affichage de adresse IP sur le moniteur serie :
  Serial.println("\n adresse IP : ");
  Serial.println(WiFi.localIP());


  // Demarrage du serveur :
  server.begin();

  // REGLAGE DES PINS DU DRIVER MOTEUR :
  pinMode(D1, OUTPUT);
  pinMode(D2, OUTPUT);
  pinMode(D3, OUTPUT);
  pinMode(D4, OUTPUT);
  
  digitalWrite(D1, LOW);
  digitalWrite(D2, LOW);
  digitalWrite(D3, LOW);
  digitalWrite(D4, LOW);
}



//######################################
//##                                  ##
//##             LOOP                 ##
//##                                  ##
//######################################

void loop()
{
  // Serveur WEB :
  client = server.available();   // Demande si presence de client

  if ((millis() - lastTime) > timerDelay) {
    //Check WiFi connection status
    if(WiFi.status()== WL_CONNECTED){
      HTTPClient http;
      String serverPath = serverName + "/paquets/";

      // Your Domain name with URL path or IP address with path
      http.begin(serverPath.c_str());

      // Send HTTP GET request
      int httpResponseCode = http.GET();
      Serial.println(serverPath);

      if (httpResponseCode>0) {
        Serial.print("HTTP Response code: ");
        Serial.println(httpResponseCode);
        String payload = http.getString();
        Serial.println(payload);
      }
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
    lastTime = millis();

    
   }
  
  /*if (client)  // Si il y a un client
  {
    
    // Reception
    demande_client = "";
    while ( client.available() )
    {
      demande_client += (char)client.read();  //Serial.print( (char)client.read() );
    }


    // Traitement :
    if(demande_client.indexOf("GET /AVANCE") >= 0)
    {
      digitalWrite(D1, LOW);
      digitalWrite(D2, LOW);
      digitalWrite(D3, HIGH);
      digitalWrite(D4, HIGH);
      
    }
    
    if(demande_client.indexOf("GET /GAUCHE") >= 0)
    {
      digitalWrite(D1, LOW);
      digitalWrite(D2, LOW);
      digitalWrite(D3, HIGH);
      digitalWrite(D4, LOW);
      
    }
    
    if(demande_client.indexOf("GET /DROITE") >= 0)
    {
      digitalWrite(D1, LOW);
      digitalWrite(D2, LOW);
      digitalWrite(D3, LOW);
      digitalWrite(D4, HIGH);
    }
    
    if(demande_client.indexOf("GET /RECULE") >= 0)
    {
      digitalWrite(D1, HIGH);
      digitalWrite(D2, HIGH);
      digitalWrite(D3, LOW);
      digitalWrite(D4, LOW);
    }
    
    if(demande_client.indexOf("GET /STOP") >= 0)
    {
      digitalWrite(D1, LOW);
      digitalWrite(D2, LOW);
      digitalWrite(D3, LOW);
      digitalWrite(D4, LOW);
      
    }
    
    
    // Envoie du site internet :
    client.println("<!DOCTYPE html>");
    client.println("<html>");
    client.println("<head><title>RC robot</title></head>");
    client.println("<body><table width=\"100%\" border=\"0\">");
    client.println("<tr valign=\"center\">");
    client.println("<td></td>");
    client.println("<td height=\"200\" align=\"center\"><a href=\"/AVANCE\"><button style=\"width:100%;height:100%\"class=\"button\">AVANCE</button></a></td></tr>");
    client.println("<tr valign=\"center\">");
    client.println("<td height=\"200\" width=\"30%\" align=\"center\"><a href=\"/GAUCHE\"><button style=\"width:100%;height:100%\"class=\"button\">GAUCHE</button></a></td>");
    client.println("<td height=\"200\" width=\"40%\" align=\"center\"><a href=\"/STOP\"><button style=\"width:100%;height:100%\"class=\"button\">STOP</button></a></td>");
    client.println("<td height=\"200\" width=\"30%\" align=\"center\"><a href=\"/DROITE\"><button style=\"width:100%;height:100%\"class=\"button\">DROITE</button></a></td>");
    client.println("</tr>");
    client.println("<td></td>");
    client.println("<td height=\"200\" align=\"center\"><a href=\"/RECULE\"><button style=\"width:100%;height:100%\"class=\"button\">RECULE</button></a></td>");
    client.println("</table>");
    client.println("Radiocommande WiFi<br>");
    client.println("</body></html>");

    
    // Deconnexion du client :
    client.stop();
  }*/
  
  delay(50);
}
