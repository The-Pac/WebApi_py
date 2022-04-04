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
#include <ArduinoJson.h>


//######################################
//##                                  ##
//##           DEFINITION             ##
//##                                  ##
//######################################

#define D1 32
#define D2 26
#define D3 33
#define D4 27
#define D5 14
#define D6 12



//######################################
//##                                  ##
//##            VARIABLES             ##
//##                                  ##
//######################################

// Reglage de la connexion :
WiFiServer server(80);
WiFiClient client;
const char *ssid     = "Bbox-4203C802";
const char *password = "7VfWnXXzz<Mg,gRk";
String demande_client;




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
  if (WiFi.status() != WL_CONNECTED)  // Tant que le module n'est pas connecte
  {

    long rnd = random(1,10);
    HTTPClient client;

    client.begin("http://jsonplaceholder.typicode.com/comments?id=" + String(rnd));
    int httpCode = client.GET();

    if (httpCode > 0){
      String payload = client.getString();
      Serial.println("\nStatuscode: " + String(httpCode));
      Serial.println(payload);
    }
  }
  else{
    Serial.println("\n failed connection ");
  }

  
  /*// Affichage de adresse IP sur le moniteur serie :
  Serial.println("\n adresse IP : ");
  Serial.println(WiFi.localIP());*/


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
  if (client)  // Si il y a un client
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
    
    
    /*// Envoie du site internet :
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
    client.stop();*/
  }
  
  delay(50);
}
