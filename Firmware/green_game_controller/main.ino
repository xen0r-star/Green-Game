#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>
#include "MelodyPlayer.h"
#include "EyeDisplay.h"
#include "WiFiManager.h"
#include "FirebaseManager.h"

#define SCREEN_ADDRESS 0x3C
Adafruit_SH1106G display = Adafruit_SH1106G(128, 64, &Wire, -1);

const int buzzerPin = 19;

const int buttonPins[] = { 14, 33, 5, 18 };
const int ledPins[] = { 12, 25, 17, 23 };

const int messageButtonPin = 13;
const int rgbPins[] = { 2, 16, 4 };


int question = 1;
int xd = 0;
int design = 1;
int currentQuestion = 0;
int buttonPressed = -1;
int buttonPressedOld = -2;
int scoreResult = 0;
String connexionToken = "";
String token = "";

MelodyPlayer melodyPlayer(buzzerPin);
FirebaseManager firebaseManager(connexionToken, token);
WiFiManager wifiManager(display, connexionToken, firebaseManager);
EyeDisplay eyeDisplay(display, connexionToken, firebaseManager);





void setup() {
  Serial.begin(115200);
  Wire.begin(26, 27);

  if (!display.begin(SCREEN_ADDRESS, true)) {
    Serial.println(F("SH1106 allocation failed"));
  }

  display.clearDisplay();
  eyeDisplay.update(0, 6, 1, connexionToken, "");

  for (int i = 0; i < 4; i++) {
    pinMode(buttonPins[i], INPUT_PULLUP);
    pinMode(ledPins[i], OUTPUT);
    digitalWrite(ledPins[i], LOW);
  }

  for (int i = 0; i < 3; i++) {
    pinMode(rgbPins[i], OUTPUT);
    digitalWrite(rgbPins[i], LOW);
  }

  pinMode(messageButtonPin, INPUT_PULLUP);

  wifiManager.connectWiFi("Maximus Decimus Meridius", "44e00a13ca3a");

  esp_sleep_enable_ext0_wakeup(GPIO_NUM_33, 0);

  melodyPlayer.playStartupMelody();
}



void loop() {
  wifiManager.handleClient();

  if (WiFi.status() == WL_CONNECTED) {
    if (connexionToken == "") {
      handleButton();
    }
    updateEyes();
  }
}

void handleButton() {
  if (digitalRead(messageButtonPin) == LOW) {
    FirebaseJson jsonData = firebaseManager.firestoreRead(token);
    FirebaseJsonData jsonDataField;

    String number = "";
    String documentPath = "fields/listQuestion/arrayValue/values/[" + String(currentQuestion) + "]/integerValue/";
    if (jsonData.get(jsonDataField, documentPath.c_str())) {
      number = jsonDataField.stringValue;
    }

    String result = "";
    documentPath = "fields/question/arrayValue/values/[" + number + "]/mapValue/fields/answer/booleanValue/";
    if (jsonData.get(jsonDataField, documentPath.c_str())) {
      if (jsonDataField.stringValue == "true") {
        result = 2;
      } else {
        result = 3;
      }
    }
    documentPath = "fields/question/arrayValue/values/[" + number + "]/mapValue/fields/answer/integerValue/";
    if (jsonData.get(jsonDataField, documentPath.c_str())) {
      result = jsonDataField.stringValue;
    }

    documentPath = "fields/question/arrayValue/values/[" + number + "]/mapValue/fields/answer/integerValue/";
    if (jsonData.get(jsonDataField, documentPath.c_str())) {
      Serial.println(jsonDataField.stringValue);
    }

    Serial.println("data: ");
    Serial.println(result);
    Serial.println(buttonPressed + 1);
    if (result == String(buttonPressed + 1)) {
      question = 1;
    } else {
      question = 0;
    }

    Serial.println("Validate");
    switch (question) {
      case 0:
        setRGB(255, 0, 0);  // Red
        eyeDisplay.update(xd, 1, 2, connexionToken, "");
        melodyPlayer.playDefeatMelody();
        break;
      case 1:
        scoreResult += 1;
        setRGB(0, 255, 0);  // Green
        eyeDisplay.update(xd, 1, 3, connexionToken, "");
        melodyPlayer.playVictoryMelody();
        break;
      case 2:
        setRGB(255, 0, 255);  // Pink
        eyeDisplay.update(xd, 1, 4, connexionToken, "");
        melodyPlayer.playVictoryMelody();
        break;
      default:
        setRGB(0, 0, 0);  // Off
        break;
    }
    for (int j = 0; j < 4; j++) {
      digitalWrite(ledPins[j], LOW);
    }
    delay(2000);      // Wait for 3 seconds
    setRGB(0, 0, 0);  // Turn off the RGB LED

    firebaseManager.firestoreSelectQuestion(token, currentQuestion, 5);

    currentQuestion += 1;
    buttonPressedOld = -2;
    buttonPressed = -1;
  }

  for (int i = 0; i < 4; i++) {
    if (digitalRead(buttonPins[i]) == LOW) {
      buttonPressed = i;
      break;
    }
  }

  if (buttonPressed != -1 && buttonPressed != buttonPressedOld) {
    for (int j = 0; j < 4; j++) {
      digitalWrite(ledPins[j], LOW);
    }

    FirebaseJson jsonData = firebaseManager.firestoreRead(token);
    FirebaseJsonData jsonDataField;

    String number = "";
    String documentPath = "fields/listQuestion/arrayValue/values/[" + String(currentQuestion) + "]/integerValue/";
    if (jsonData.get(jsonDataField, documentPath.c_str())) {
      number = jsonDataField.stringValue;
    }

    Serial.println(number);

    String type = "";
    documentPath = "fields/question/arrayValue/values/[" + number + "]/mapValue/fields/type/stringValue/";
    if (jsonData.get(jsonDataField, documentPath.c_str())) {
      type = jsonDataField.stringValue;
    }

    Serial.println(type);
    if (type == "choice2") {
      Serial.println(buttonPressed);
      if (buttonPressed + 1 == 1 || buttonPressed + 1 == 4) {
        digitalWrite(ledPins[buttonPressed], LOW);
      } else {
        firebaseManager.firestoreSelectQuestion(token, currentQuestion, buttonPressed);
        digitalWrite(ledPins[buttonPressed], HIGH);
      }
    } else {
      firebaseManager.firestoreSelectQuestion(token, currentQuestion, buttonPressed + 1);
      digitalWrite(ledPins[buttonPressed], HIGH);
    }

    buttonPressedOld = buttonPressed;
  }
}



void setRGB(int red, int green, int blue) {
  analogWrite(rgbPins[0], red);
  analogWrite(rgbPins[1], green);
  analogWrite(rgbPins[2], blue);
}



void updateEyes() {
  int n = random(0, 11);
  int m = random(0, 8);

  xd -= (n < 5) ? 1 : 0;
  xd += (n > 5) ? 1 : 0;
  xd = (xd < -4) ? -3 : xd;
  xd = (xd > 4) ? 3 : xd;

  if (currentQuestion <= 9) {
    eyeDisplay.update(xd, m, design, connexionToken, "Question " + String(currentQuestion + 1) + " / 10");
  } else {
    eyeDisplay.update(xd, m, design, connexionToken, "Score : " + String(scoreResult * 10) + "%");
  }
}