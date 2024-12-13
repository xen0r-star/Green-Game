#ifndef WIFI_MANAGER_H
#define WIFI_MANAGER_H

#include <WiFi.h>
#include <WebServer.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>
#include "FirebaseManager.h"

class WiFiManager {
public:
    WiFiManager(Adafruit_SH1106G& display, String& connexionToken, FirebaseManager& firebaseManager);
    void connectWiFi(const char* ssid, const char* password);
    void handleClient();
    void createAccessPoint();

private:
    Adafruit_SH1106G& display;
    WebServer server;
    String& connexionToken;
    FirebaseManager& firebaseManager;

    void handleRoot();
    void handleConnect();
};

#endif
