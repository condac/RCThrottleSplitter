//#include <Servo.h> 
#include <EEPROM.h>

//Servo myservo;  
int pos = 0;    

int CH2pin = 2;
int CH3pin = 3;

int CH2outpin = 6;
int CH3outpin = 8;

int CH2pulse = 0;
int CH3pulse = 0;

int CH2out = 0;
int CH3out = 0;

long NEUTRAL = 0;
int NEUTRALaddress = 10;
long CH2REVERSE = 0;
int CH2REVERSEaddress = 20;
long CH3REVERSE = 0;
int CH3REVERSEaddress = 30;


volatile unsigned long startAuxPulse = 0;
volatile unsigned long stopAuxPulse = 0;
volatile unsigned long startCH3Pulse = 0;
volatile unsigned long stopCH3Pulse = 0;

void setup() 
{ 
  readSavedData();
  //myservo.attach(9);  
  //attachInterrupt(0, interuptHandle, RISING);
  Serial.begin(9600);
  pinMode(CH2pin, INPUT);
  pinMode(CH3pin, INPUT);
  pinMode(CH2outpin, OUTPUT);
  pinMode(CH3outpin, OUTPUT);
  attachInterrupt(0, auxSignal, CHANGE);
  attachInterrupt(1, ch3Signal, CHANGE);
} 

void readSavedData() {
  NEUTRAL = EEPROMReadlong(NEUTRALaddress);
  CH2REVERSE = EEPROMReadlong(CH2REVERSEaddress);
  CH3REVERSE = EEPROMReadlong(CH3REVERSEaddress);
}
void saveSavedData() {
  EEPROMWritelong(NEUTRALaddress, NEUTRAL);
  EEPROMWritelong(CH2REVERSEaddress, CH2REVERSE);
  EEPROMWritelong(CH3REVERSEaddress, CH3REVERSE);
  Serial.println("saved data to eeprom");
}

void loop() { 
  
  


    if(Serial.available() > 0)  {
        int x;
        int y;
        int z;
        String str;

        str = Serial.readStringUntil('$');
        str = Serial.readStringUntil(':');
        if (str == "save") {
          NEUTRAL = Serial.parseInt();
          CH2REVERSE = Serial.parseInt();
          CH3REVERSE = Serial.parseInt();
          Serial.print(str);
          Serial.print(NEUTRAL);
          Serial.print(CH2REVERSE);
          Serial.println(CH3REVERSE);
          saveSavedData();
        }
        if (str == "load") {
          Serial.print("LOAD:");
          Serial.print(NEUTRAL);
          Serial.print(" , ");
          Serial.print(CH2REVERSE);
          Serial.print(" , ");
          Serial.print(CH3REVERSE);
          Serial.println(" , ");
        }
        Serial.print("arduino got:");
        Serial.println(str);
    }

  
  Serial.print("CH2: ");    
  Serial.println(CH2pulse);
  Serial.print("CH3: ");    
  Serial.println(CH3pulse);
  Serial.print("CH2out: ");    
  Serial.println(CH2out);
  Serial.print("CH3out: ");    
  Serial.println(CH3out);
  delay(1000);
} 

void pulseOut(int pin, int us) {
   
   digitalWrite(pin, HIGH);
   us = max(us - 4, 1);
   delayMicroseconds(us);
   digitalWrite(pin, LOW);
}

void interuptHandle() {
  CH2pulse = pulseIn(CH2pin, HIGH, 20000) +100;
  
}

void auxSignal() {
  if(digitalRead(CH2pin) == HIGH)    {
    startAuxPulse = micros();
  }
  else {
    stopAuxPulse = micros();
    CH2pulse = (stopAuxPulse - startAuxPulse) +0;
    //calculate();
    //sendServo();
  }
}
void ch3Signal() {
  if(digitalRead(CH3pin) == HIGH)    {
    startCH3Pulse = micros();
  }
  else {
    stopCH3Pulse = micros();
    CH3pulse = (stopCH3Pulse - startCH3Pulse) +0;
    calculate();
    sendServo();
  }
}
void calculate() {
  int ch2 = CH2pulse;
  int ch3 = CH3pulse;
  if (CH2REVERSE) {
    ch2 = 3000 - CH2pulse;
  }
  
  
  CH2out = ch2;
  CH3out = (1000 - (CH2pulse - 1000))+1000;
}
void sendServo() {
  pulseOut(CH2outpin, 1000);
  pulseOut(CH3outpin, CH3pulse);
}

void EEPROMWritelong(int address, long value)      {
      //Decomposition from a long to 4 bytes by using bitshift.
      //One = Most significant -> Four = Least significant byte
      byte four = (value & 0xFF);
      byte three = ((value >> 8) & 0xFF);
      byte two = ((value >> 16) & 0xFF);
      byte one = ((value >> 24) & 0xFF);

      //Write the 4 bytes into the eeprom memory.
      EEPROM.write(address, four);
      EEPROM.write(address + 1, three);
      EEPROM.write(address + 2, two);
      EEPROM.write(address + 3, one);
}

//This function will return a 4 byte (32bit) long from the eeprom
//at the specified address to adress + 3.
long EEPROMReadlong(long address)      {
      //Read the 4 bytes from the eeprom memory.
      long four = EEPROM.read(address);
      long three = EEPROM.read(address + 1);
      long two = EEPROM.read(address + 2);
      long one = EEPROM.read(address + 3);

      //Return the recomposed long by using bitshift.
      return ((four << 0) & 0xFF) + ((three << 8) & 0xFFFF) + ((two << 16) & 0xFFFFFF) + ((one << 24) & 0xFFFFFFFF);
}
