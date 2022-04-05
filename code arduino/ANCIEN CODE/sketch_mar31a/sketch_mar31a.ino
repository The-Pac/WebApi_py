

/*
 * Ce programme permet de controller un robot grâce à une connexion WiFi.
 * Le robot utilise des codeurs optiques pour calculer sa position.
 * 
 * Les connexions entre
 * le NodeMCU et les driver et capteur sont les suivantes :
 *   - les pins D1, D2, D3, D4 sont utilisées par le driver moteur
 *   - la pin D5 est utilisée pour lire l'état de la roue codeuse gauche
 *   - la pin D6 est utilisée pour lire l'état de la roue codeuse droite
 * 
 * Le programme utilise deux interruptions pour gérer les informations capteur.
 * 
 * REMARQUE : le port UART est ouvert le temps de donner l'adresse IP du serveur.
 */

#include <ESP8266wifi.h>


//######################################
//##                                  ##
//##           DEFINITION             ##
//##                                  ##
//######################################

#define D1 5
#define D2 4
#define D3 0
#define D4 2
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
const char *ssid     = "IMERIR_IoT";
const char *password = "kohWoong5oox";
String demande_client;


// Positionnement du robot :
struct Position
{
  double position_x;  // position X du robot
  double position_y;  // position Y du robot
  float angle;       // orientation du robot
};


// Odometrie :
struct Position odometrie;



//######################################
//##                                  ##
//##          RoueGauche              ##
//##                                  ##
//######################################

ICACHE_RAM_ATTR void RoueGauche()
{
  // EN FONCTION DU SENS DE ROTATION DU MOTEUR GAUCHE :
  
  if (digitalRead(D3) == LOW)  // marche avant
  {
    odometrie.position_x += 2.5*cos( odometrie.angle );
    odometrie.position_y += 2.5*sin( odometrie.angle );
    odometrie.angle += -0.038;
  }
  else  // marche arriere
  {
    odometrie.position_x += -2.5*cos( odometrie.angle );
    odometrie.position_y += -2.5*sin( odometrie.angle );
    odometrie.angle += 0.038;
  }
}



//######################################
//##                                  ##
//##          RoueDroite              ##
//##                                  ##
//######################################

ICACHE_RAM_ATTR void RoueDroite()
{
  // EN FONCTION DU SENS DE ROTATION DU MOTEUR DROIT :
  
  if (digitalRead(D4) == LOW)  // marche avant
  {
    odometrie.position_x += 2.5*cos( odometrie.angle );
    odometrie.position_y += 2.5*sin( odometrie.angle );
    odometrie.angle += 0.038;
  }
  else  // marche arriere
  {
    odometrie.position_x += -2.5*cos( odometrie.angle );
    odometrie.position_y += -2.5*sin( odometrie.angle );
    odometrie.angle += -0.038;
  }
}



//######################################
//##                                  ##
//##             SETUP                ##
//##                                  ##
//######################################

void setup()
{
  // Reglage du port UART :
  Serial.begin(9600);

  
  // Connection au wifi :  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)  // Tant que le module n'est pas connecte
  {
    delay(1000);
    Serial.print(".");
  }

  
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

  
  // REGLAGE DE LA PIN DE LA ROUE CODEUSE GAUCHE :
  pinMode(D5, INPUT);
  attachInterrupt( digitalPinToInterrupt(D5), RoueGauche, CHANGE );


  // REGLAGE DE LA PIN DE LA ROUE CODEUSE DROITE :
  pinMode(D6, INPUT);
  attachInterrupt( digitalPinToInterrupt(D6), RoueDroite, CHANGE );


  // INITIALISATION DE LA VARIABLE :
  odometrie.position_x = 0;
  odometrie.position_y = 0;
  odometrie.angle = 0;
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
      digitalWrite(D1, HIGH);
      digitalWrite(D2, HIGH);
      digitalWrite(D3, LOW);
      digitalWrite(D4, LOW);
    }
    
    if(demande_client.indexOf("GET /GAUCHE") >= 0)
    {
      digitalWrite(D1, HIGH);
      digitalWrite(D2, HIGH);
      digitalWrite(D3, HIGH);
      digitalWrite(D4, LOW);
    }
    
    if(demande_client.indexOf("GET /DROITE") >= 0)
    {
      digitalWrite(D1, HIGH);
      digitalWrite(D2, HIGH);
      digitalWrite(D3, LOW);
      digitalWrite(D4, HIGH);
    }
    
    if(demande_client.indexOf("GET /RECULE") >= 0)
    {
      digitalWrite(D1, HIGH);
      digitalWrite(D2, HIGH);
      digitalWrite(D3, HIGH);
      digitalWrite(D4, HIGH);
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
    client.println("Radiocommande WiFi avec odometrie<br>");
    client.println("<br><b>Position X : </b>");
    client.println(odometrie.position_x);
    client.println("<br><b>Position Y : </b>");
    client.println(odometrie.position_y);
    client.println("<br><b>Orientation : </b>");
    client.println(odometrie.angle);
    client.println("</body></html>");

    
    // Deconnexion du client :
    client.stop();
  }
  
  delay(50);
}
