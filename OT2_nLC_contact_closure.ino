/*
(Long awaited) contact closure - Meissner Lab
Script establishes interface between OpenTrons liquid handling robot and ThermoFischer nanoLC.
Arduino should be connected to OpenTrons Raspberry Pi via USB, and pin 2 and ground should be connected to nanoLC.
Script reads pin 2 and then sends a contact closure start or stop signal over serial (USB) to OpenTrons.
created on 20230412
by Onur Serce <http://www.onurserce.com>
modified from Yasin Kaya's TinyLab script
*/

// Constants won't change. They're used here to set pin numbers:
const int PIN = 2;  // the number of the read-in pin

// Variables will change:
int contactClosure = 0;  // variable for reading the contact closure status, LOW by default.

void setup() {
 // initialize the LED pin as an output:
 Serial.begin(9600);
 // initialize the pin 2 as an input:
 pinMode(PIN, INPUT);
}

void loop() {
 // read the state of the pin 2:
 contactClosure = digitalRead(PIN);
   if (contactClosure == LOW) {
 // turn LED on and relay the signal over serial:
 Serial.println("Contact_Closure_Start");
 }
 else {
 // turn LED off and relay the signal over serial:
 Serial.println("Contact_Closure_Stop");
 }
 delay(1);  // delay in between reads for stability
}
