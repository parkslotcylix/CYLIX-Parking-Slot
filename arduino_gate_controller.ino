#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Servo.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);  
Servo gateServo;

const int irInner = 14;   // D5
const int irOuter = 12;   // D6
const int servoPin = 13;  // D7
const int greenLed = 0;   // D3
const int redLed = 2;     // D4 

//CAMERA SLOT PINS (Add these for your 3 LEDs)
const int slot1_LED = 15; // D8 (Red LED for Slot 1) or use any free pin
const int slot2_LED = 3;  // RX (Red LED for Slot 2) or use any free pin
const int slot3_LED = 1;  // TX (Red LED for Slot 3) or use any free pin

int availableSlots = 3; 

void setup() {
  Serial.begin(115200); 
  Wire.begin(4, 5); 
  
  gateServo.attach(servoPin);
  pinMode(irInner, INPUT_PULLUP);
  pinMode(irOuter, INPUT_PULLUP);
  pinMode(redLed, OUTPUT);
  pinMode(greenLed, OUTPUT);
  
  // Setup Camera Slot LEDs
  pinMode(slot1_LED, OUTPUT);
  // pinMode(slot2_LED, OUTPUT); // Only if pins are free
  // pinMode(slot3_LED, OUTPUT);

  digitalWrite(redLed, HIGH);
  digitalWrite(greenLed, LOW);
  gateServo.write(0); 

  lcd.init();
  lcd.backlight();
  updateDisplay();
}

void loop() {
  checkCameraSerial(); 
  
  if (digitalRead(irInner) == LOW && availableSlots > 0) {
    handleGate("WELCOME!");
  }

  else if (digitalRead(irOuter) == LOW) {
    handleGate("GOODBYE!");
  }
}

void checkCameraSerial() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    
    if (data.length() >= 5) {
      digitalWrite(slot1_LED, data[0] == '1' ? HIGH : LOW);
      
      int count = 0;
      if (data[0] == '0') count++;
      if (data[2] == '0') count++;
      if (data[4] == '0') count++;
      if (availableSlots != count) {
        availableSlots = count;
        updateDisplay();
      }
    }
  }
}

void handleGate(String msg) {
  digitalWrite(redLed, LOW);
  digitalWrite(greenLed, HIGH);
  lcd.clear();
  lcd.print(msg);
  gateServo.write(90); 

  while (digitalRead(irInner) == LOW || digitalRead(irOuter) == LOW) {
    yield(); 
  }
  
  delay(1000); 
  gateServo.write(0);
  digitalWrite(greenLed, LOW);
  digitalWrite(redLed, HIGH);
  updateDisplay();
}

void updateDisplay() {
  lcd.setCursor(0, 0);
  lcd.print("PARKING SYSTEM  "); 
  lcd.setCursor(0, 1);
  if (availableSlots > 0) {
    lcd.print("SLOTS FREE: ");
    lcd.print(availableSlots);
    lcd.print("   "); 
  } else {
    lcd.print("SORRY: FULL    ");
  }
}
