#include "EyeDisplay.h"
#include "FirebaseManager.h"

EyeDisplay::EyeDisplay(Adafruit_SH1106G& display, String& connexionToken, FirebaseManager& firebaseManager)
  : display(display), connexionToken(connexionToken), firebaseManager(firebaseManager) {}

void EyeDisplay::update(int xd, int m, int design, String& connexionToken, String text) {
  display.clearDisplay();

  if (connexionToken != "") {
    display.setTextSize(1);
    display.setTextColor(SH110X_WHITE);
    display.setCursor(22, 20);
    display.print(connexionToken);
    currentTime += 1;

    if (interval - currentTime >= 0) {

      display.setCursor(7, 40);
      String textR = "Reconnexion dans " + String(interval - currentTime);
      display.print(textR);
      display.display();
    } else {
      currentTime = 0;
      display.setCursor(37, 40);
      display.print("Connexion");
      display.display();

      FirebaseJson jsonData = firebaseManager.firestoreRead(connexionToken);

      FirebaseJsonData jsonDataField;
      if (jsonData.get(jsonDataField, "fields/connexion/booleanValue/")) {
        Serial.println(jsonDataField.stringValue);
        if (jsonDataField.stringValue != "false") {
          Serial.println("click");
          connexionToken = "";
        }
      }
    }

    delay(1000);
  } else {
    if (m == 6) {
      display.drawBitmap(16 + xd, 8, eye0, 32, 32, SH110X_WHITE);
      display.drawBitmap(80 + xd, 8, eye0, 32, 32, SH110X_WHITE);

      display.setTextSize(1);
      display.setTextColor(SH110X_WHITE);
      display.setCursor((128 - (text.length() * 6)) / 2, 55);
      display.print(text);

      display.display();
      delay(100);
    } else {
      switch (design) {
        case 1:
          display.drawBitmap(16 + xd, 8, eye1, 32, 32, SH110X_WHITE);
          display.drawBitmap(80 + xd, 8, eye1, 32, 32, SH110X_WHITE);
          break;
        case 2:
          display.drawBitmap(16 + xd, 8, eye2, 32, 32, SH110X_WHITE);
          display.drawBitmap(80 + xd, 8, eye3, 32, 32, SH110X_WHITE);
          break;
        case 3:
          display.drawBitmap(16 + xd, 8, eye3, 32, 32, SH110X_WHITE);
          display.drawBitmap(80 + xd, 8, eye2, 32, 32, SH110X_WHITE);
          break;
        case 4:
          display.drawBitmap(16 + xd, 8, eye4, 32, 32, SH110X_WHITE);
          display.drawBitmap(80 + xd, 8, eye4, 32, 32, SH110X_WHITE);
          break;
      }

      display.setTextSize(1);
      display.setTextColor(SH110X_WHITE);
      display.setCursor((128 - (text.length() * 6)) / 2, 55);
      display.print(text);

      display.display();
      delay(750);
    }
  }
}
