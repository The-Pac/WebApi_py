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


   ///////////
    int arr = 34;
    int posi = 11 ;
    int etat = 0;
   while (1)
      {
        //Croisement
        if (digitalRead(C2) == 1 && digitalRead(C3) == 1  &&( digitalRead(C1) == 1 || digitalRead(C4) == 1)){

          ///////COHORDONNES
          // arriver 
          int arr1 = (arr / 10 )*10;
          int arr2 = arr - arr1;
          
          // position actuelle
          int posi1 = (posi / 10)*10;
          int posi2 = posi - posi1;
          
          Serial.print("arrivé  ");
          Serial.println(arr);
          
          Serial.print("position  ");
          Serial.println(posi);

          //DEPLACEMENT JUSQUA ARRIVE

          if(posi1 != arr1){
            Serial.print("arrivé1  ");
            Serial.println(arr1);
            
            Serial.print("position1  ");
            Serial.println(posi1);
            if (posi1 < arr1){
              DAvant();
              posi = posi + 10;
              Serial.println("c avant");
              delay(1000);
              
            }
            else if (posi1 > arr1) {
              DArriere();
              posi = posi - 10;
              Serial.println("c arriere");
              delay(1000);
            }
            
          }
          else if(posi2 != arr2){
            Serial.print("arrivé2  ");
            Serial.println(arr2);
            
            Serial.print("position2  ");
            Serial.println(posi2);

            while (digitalRead(C1) == 1 && digitalRead(C4) == 1){
              DAvant();
            }
            DStop();
            if (posi2 < arr2){
              DGauche();
              posi = posi + 1;
              Serial.println("c gauche");
              delay(1000);

              while (digitalRead(C1) == 1 && digitalRead(C4) == 1){
                DAvant();
              }
              DStop();
            
              while (digitalRead(C2) == 1 && digitalRead(C3) == 1){
                DGauche();
              }
              DStop();
            }
            else if (posi2 > arr2) {
              DDroit();
              posi = posi - 1;
              Serial.println("c droit");
              delay(1000);

              while (digitalRead(C1) == 1 && digitalRead(C4) == 1){
                DAvant();
              }
              DStop();
            
              while (digitalRead(C2) == 1 && digitalRead(C3) == 1){
                DDroit();
              }
              DStop();
            }
            
          }
          else if (posi2 == arr2 && posi1 == arr1 ) {
            DStop();
            delay(10000);
            posi = arr;
            arr = 11;
            
          }

          
        }
        
        // AVANCER
        else if ((digitalRead(C2) == 1 || digitalRead(C3) == 1 ) && digitalRead(C1) == 0 && digitalRead(C4) == 0){
          DAvant();
          Serial.println("d avant");
        }

        // CORRECTION DE LIGNE
        else if ( digitalRead(C1) == 0 && digitalRead(C4) == 1){
          DDroit();
          Serial.println("d droit");
        }
        else if ( digitalRead(C1) == 1 && digitalRead(C4) == 0){
          DGauche();
          Serial.println("d gauche");
        }


        
         

        
      }

      
   ///////////
  
  delay(50);
}
