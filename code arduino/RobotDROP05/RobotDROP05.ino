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
const char *ssid     = "IMERIR_IoT";
const char *password = "kohWoong5oox";
String demande_client;

//URL de l'API
String serverName = "http://10.3.1.235:8000";

//mesure de temps
unsigned long lastTime = 0;
//Intervalle de 5 seconde
unsigned long timerDelay = 5000;



//######################################
//##                                  ##
//##         VOID DIRECTION           ##
//##                                  ##
//######################################

void DAvant(){
  digitalWrite(D1, HIGH);
  digitalWrite(D2, LOW);
  digitalWrite(D3, HIGH);
  digitalWrite(D4, LOW);
  
}

void DArriere(){
  digitalWrite(D1, LOW);
  digitalWrite(D2, HIGH);
  digitalWrite(D3, LOW);
  digitalWrite(D4, HIGH);
}
void DStop(){
  digitalWrite(D1, LOW);
  digitalWrite(D2, LOW);
  digitalWrite(D3, LOW);
  digitalWrite(D4, LOW);
}

// Rotation sur lui-meme
void DDroit(){
  digitalWrite(D1, HIGH);
  digitalWrite(D2, LOW);
  digitalWrite(D3, LOW);
  digitalWrite(D4, HIGH);
}

void DGauche(){
  digitalWrite(D1, LOW);
  digitalWrite(D2, HIGH);
  digitalWrite(D3, HIGH);
  digitalWrite(D4, LOW);
  
}

// rotation autour de la roue immobile
void CGauche(){
  digitalWrite(D1, LOW);
  digitalWrite(D2, LOW);
  digitalWrite(D3, HIGH);
  digitalWrite(D4, LOW);
  
 
 }

void CDroite(){
digitalWrite(D1, HIGH);
digitalWrite(D2, LOW);
digitalWrite(D3, LOW);
digitalWrite(D4, LOW); 
 
 }
 
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


  // Demarrage du serveur :
  server.begin();
  ///////////////////////////////

  // REGLAGE DES PINS DU DRIVER MOTEUR :
  pinMode(D1, OUTPUT);
  pinMode(D2, OUTPUT);
  pinMode(D3, OUTPUT);
  pinMode(D4, OUTPUT);
  
  digitalWrite(D1, LOW);
  digitalWrite(D2, LOW);
  digitalWrite(D3, LOW);
  digitalWrite(D4, LOW);

  // REGLAGE DES PINS DES CAPTEURS :
  pinMode(C1, INPUT);
  pinMode(C2, INPUT);
  pinMode(C3, INPUT);
  pinMode(C4, INPUT);
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


  if ((millis() - lastTime) > timerDelay) {
    //Vérification connection WIFI
    if(WiFi.status()== WL_CONNECTED){
      HTTPClient http;
      String serverPath = serverName + "/croisements/";

      // Connection communication API
      http.begin(serverPath.c_str());

      // HTTP GET requette
      int httpResponseCode = http.GET();
      Serial.println(serverPath);

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
    lastTime = millis();

    // teste deplacemnt en A3 T2 MAISON 8 
    // Etat Deplacement led // ou ecran
    const char* ResponseCode = "{\"adresse\":328,\"deplacement\":['A','A','D','A','I','D','D','A','G']}";
    //           ["A1T1","A1T2","A2T2","A3T2","A3T2","A3T1","A2T1","A1T1","POSTE"]
    //char json[] =  ResponseCode ;

    // JSON => "char"
    DynamicJsonDocument doc(1024);
    deserializeJson(doc, ResponseCode);

    //Déoupage
    //char tab_position[] = doc["deplacement"];
    //const int adresse = doc["adresse"];
    //
    char tab_position[] = {'A','A','D','A','I','D','D','A','G'};

   ///////////
    int i = 0;
    int A = 1 ;
    int T = 0;
    int r = 0;
    
    //HTTPClient http;
    //http.addHeader("string", "http://10.3.1.235:8000/Robot");

    //int httpResponseCode = http.POST("{\"position\":\"AxBx\"}");
   while (i< 9)
      {
        //Croisement
        if ((digitalRead(C2) == 1 && digitalRead(C3) == 1  &&( digitalRead(C1) == 1 || digitalRead(C4) == 1))
              || T == 0){

          //DEPLACEMENT JUSQUA ARRIVE SWITCH CASE
          switch (tab_position[i]){
            
            case 'A':
              DAvant();
              i ++;
              break;
          
            case 'G':// tourner à gauche à l'intersection
              DStop();
              delay(3000);
              
              DAvant();
              delay(1000);
              while(digitalRead(C2) == 0 || digitalRead(C1) == 0 ){
               CGauche();
              }
              DStop();
              delay(3000);
              i++;
              r++;
              break;

            case 'D':// tourner à droite à l'intersection
              DStop();
              delay(3000);
              
              DAvant();
              delay(1000);
              while(digitalRead(C2) == 0 || digitalRead(C1) == 0 ){
               CDroite();
              }
              DStop();
              delay(3000);
              i++;
              r++;
              break;

             case 'R':
              DArriere();
              i ++;
              break;

             case 'I':
              DStop();
              delay(1000);
              i ++;
              break;
              
          }
          if (r%2 == 0){
            T++;
          }
          else{
            A++;
          }
          Serial.print("A= ");
          Serial.println(A); 
          Serial.print("T= %");
          Serial.print(T);
          //char posi = "A"+A+"T"+T;
          //int httpResponseCode = http.POST("{\"position\":posi}");
          
          /*//DEPLACEMENT JUSQUA ARRIVE if

          if(tab_position[i] == 'A'){
            DAvant();
            i ++;
          }
          else if(tab_position[i] == 'G'){ // tourner à gauche à l'intersection
            
            DStop();
            delay(3000);
            
            DAvant();
            delay(1000);
           while(digitalRead(C2) == 0 || digitalRead(C1) == 0 ){
            CGauche();
           }
           i++;
           DStop();
           delay(3000);
          }
          else if (tab_position[i] == 'D') { // tourner à droite à l'intersection
            DStop();
            delay(3000);
            
            DAvant();
            delay(1000);
            while(digitalRead(C2) == 0 || digitalRead(C1) == 0 ){
             CDroite();
            }
           i++;
           DStop();
           delay(3000);
          }
          else if(tab_position[i] == 'R'){
            DArriere();
            i ++;
          }*/
            
        }

        ///////////////////////////////////////////////////////

        // CORRECTION DE LIGNE
        else if ( digitalRead(C1) == 1 && digitalRead(C4) == 0){
          DDroit();
        }
        else if ( digitalRead(C1) == 0 && digitalRead(C4) == 1){
          DGauche();
        }
        //////////////////////////////////////////////////////

      }

      
   ///////////
  
  delay(50);
  }
}
