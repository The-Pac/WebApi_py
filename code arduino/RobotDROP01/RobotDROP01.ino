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
#include "ArduinoJson.h"


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

#define C1 14
#define C2 4
#define C3 18
#define C4 19


//######################################
//##                                  ##
//##            VARIABLES             ##
//##                                  ##
//######################################




//######################################
//##                                  ##
//##         VOID DIRECTION           ##
//##                                  ##
//######################################

void DStop(){
  digitalWrite(D1, LOW);
  digitalWrite(D2, LOW);
  digitalWrite(D3, LOW);
  digitalWrite(D4, LOW);
}

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
  char tab_Direction[] = "ADGDGA";
  int i = 0;
   while (i < sizeof(tab_Direction)-1)
      {
        //Croisement
        if (digitalRead(C2) == 1 && digitalRead(C3) == 1  &&( digitalRead(C1) == 1 || digitalRead(C4) == 1)){
          char c = tab_Direction[i];
          Serial.println(c);
          Serial.println(i);
          switch( c )
          {
              case 'A':
                  DAvant();
                  i++;
                  break;
                  
              case 'D':
                  DAvant();
                  delay(2000);
                  while(digitalRead(C2) == 0 || digitalRead(C1) == 0 ){
                   CGauche();
                  }
                  DStop();
                  i++;
                  break;
                  
              case 'G' :
                  DAvant();
                  delay(2000);
                  while(digitalRead(C2) == 0 || digitalRead(C1) == 0 ){
                    CDroite();
                  }
              
                  DStop();
                  i++;
                  break;
          }
        }
        //////////////////////////////////////////////////////
        // CORRECTION DE LIGNE
         if ( digitalRead(C1) == 0 && digitalRead(C4) == 1){
          DDroit();
        }
        else if ( digitalRead(C1) == 1 && digitalRead(C4) == 0){
          DGauche();
        }
        //////////////////////////////////////////////////////

      }

      
   ///////////
  
  delay(50);
}
