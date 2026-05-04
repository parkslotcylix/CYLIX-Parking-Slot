#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Servo.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);
Servo gateServo;

const int irInner = 14;   // D5
const int irOuter = 12;   // D6
const int servoPin = 13;  // D7

const int slot1 = 16;  // D0
const int slot2 = 15;  // D8
const int slot3 = 5 ;   // D1

int availableSlots = 3;

void setup() {
  Serial.begin(115200);
  Wire.begin(4, 2);  // SDA=D2, SCL=D4

  gateServo.attach(servoPin);
  gateServo.write(0);  

  pinMode(irInner, INPUT_PULLUP);
  pinMode(irOuter, INPUT_PULLUP);

  pinMode(slot1, OUTPUT);
  pinMode(slot2, OUTPUT);
  pinMode(slot3, OUTPUT);

  digitalWrite(slot1, LOW);
  digitalWrite(slot2, LOW);
  digitalWrite(slot3, LOW);

  lcd.init();
  lcd.backlight();
  updateDisplay();
}

void loop() {
  if (digitalRead(irInner) == HIGH && digitalRead(irOuter) == HIGH) {
    checkCameraSerial();
  }

  if (digitalRead(irInner) == LOW && availableSlots > 0) {
    handleGate("WELCOME!");
  } else if (digitalRead(irOuter) == LOW) {
    handleGate("GOODBYE!");
  }
}

void checkCameraSerial() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    data.trim();
    while (Serial.available() > 0) { Serial.read(); }
    if (data.length() >= 5) {
      digitalWrite(slot1, (data[0] == '1'));
      digitalWrite(slot2, (data[2] == '1'));
      digitalWrite(slot3, (data[4] == '1'));

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
  lcd.clear();
  lcd.print(msg);

  gateServo.write(180);
  delay(1000);

  while (digitalRead(irInner) == LOW || digitalRead(irOuter) == LOW) {
    yield();
  }

  delay(1000);
  gateServo.write(0);
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