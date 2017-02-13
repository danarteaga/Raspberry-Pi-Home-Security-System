/*
  RF_Sniffer
  
  Hacked from http://code.google.com/p/rc-switch/
  
  by @justy to provide a handy RF code sniffer
*/

#include "RCSwitch.h"
#include <stdlib.h>
#include <stdio.h>
#include <string>
#include <sstream>

     
RCSwitch mySwitch;
 

int main(int argc, char *argv[]) {  
  
     // This pin is not the first pin on the RPi GPIO header!
     int PIN = 6;
     
     if(wiringPiSetup() == -1)
       return 0;

     mySwitch = RCSwitch();
     mySwitch.enableReceive(PIN);  // Receiver on inerrupt 0 => that is pin #2
    
     while(1) {
  
      if (mySwitch.available()) {
    
        int value = mySwitch.getReceivedValue();
        int new_value = value/1000;
    
        if (value == 0) {
          printf("Unknown encoding\n");
        } else {
   
          printf("Received %i\n", mySwitch.getReceivedValue() );
          // printf("Received %i\n", new_value );

          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line		  
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line	
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line	
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line	
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line	
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line	
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line	
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line	
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line	
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line
          //new_line			  
		  
        }

        mySwitch.resetAvailable();
    
      }
      
  }

  exit(0);


}

