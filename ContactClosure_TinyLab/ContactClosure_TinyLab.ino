/*
Contact closure - Meissner Lab
Script establishes interface between OpenTrons liquid handling robot and ThermoFisher easy nLC 1200.
LC contact closure state at start must be set to "Close"
Arduino should be powered with an external adaptor (bug: not clear why, grounding issues?)
Arduino should be connected to OpenTrons Raspberry Pi via USB, and pin 2 and ground should be connected to nanoLC.
Script reads pin 2 and then sends a contact closure start or stop signal over serial (USB) to OpenTrons.
created on 20230412
by Onur Serce <http://www.onurserce.com>
modified from Yasin Kaya's TinyLab script
*/

// Constants won't change. They're used here to set pin numbers:
const int PIN = 2;  // the number of the read-in pin
const int LED = 13;

// Variables will change:
int contactClosure = 0;  // variable for reading the contact closure status, LOW by default.

#include "pitches.h"

// notes in the melody:
int melody[] = {
  NOTE_C4, NOTE_G3, NOTE_G3, NOTE_A3, NOTE_G3, 0, NOTE_B3, NOTE_C4
};

// note durations: 4 = quarter note, 8 = eighth note, etc.:
int note_durations[] = {
  4, 8, 8, 4, 4, 4, 4, 4
};

void setup() {
 // initialize the LED pin as an output:
 Serial.begin(9600);
 // initialize the pin 2 as an input:
 pinMode(PIN, INPUT);
 pinMode(LED, OUTPUT);
}

void loop() {
 // read the state of the pin 2:
 contactClosure = digitalRead(PIN);
   if (contactClosure == LOW) {
 // turn LED on and relay the signal over serial:
 Serial.println("Contact_Closure_Start");
 digitalWrite(LED, HIGH);
  // iterate over the notes of the melody:
for (int this_note = 0; this_note < 8; this_note++) {

  // to calculate the note duration, take one second
  // divided by the note type.
  //e.g. quarter note = 1000 / 4, eighth note = 1000/8, etc.
  int note_duration = 1000 / note_durations[this_note];
  tone(A1, melody[this_note], note_duration);

  // to distinguish the notes, set a minimum time between them.
  // the note's duration + 30% seems to work well:
  int pause_between_notes = note_duration * 1.30;
  delay(pause_between_notes);
  // stop the tone playing:
  noTone(A1);
}
 }
 else {
 // turn LED off and relay the signal over serial:
 Serial.println("Contact_Closure_Stop");
digitalWrite(LED, LOW);
 }
 delay(1);  // delay in between reads for stability
}