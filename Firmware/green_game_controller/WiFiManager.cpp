#include "WiFiManager.h"
#include "FirebaseManager.h"
#include <WiFi.h>

WiFiManager::WiFiManager(Adafruit_SH1106G& display, String& connexionToken, FirebaseManager& firebaseManager)
    : display(display), server(80), connexionToken(connexionToken), firebaseManager(firebaseManager) {}


void WiFiManager::connectWiFi(const char* ssid, const char* password) {
    WiFi.mode(WIFI_STA);
    WiFi.begin(ssid, password);

    if (WiFi.waitForConnectResult() != WL_CONNECTED) {
        Serial.println("Connexion au WiFi échouée, création du point d'accès...");
        createAccessPoint();
    } else {
        Serial.print("Connecté au WiFi: ");
        Serial.println(WiFi.localIP());
        randomSeed(analogRead(0));
        
        firebaseManager.firestoreStart();
    }
}

void WiFiManager::handleClient() {
    server.handleClient();
}

void WiFiManager::createAccessPoint() {
    WiFi.mode(WIFI_AP);
    WiFi.softAP("ESP32_CONFIG", "12345678");

    IPAddress IP = WiFi.softAPIP();
    Serial.print("Point d'accès créé avec IP: ");
    Serial.println(IP);

    display.clearDisplay();
    display.setCursor(0, 0);
    display.setTextSize(1);
    display.setTextColor(SH110X_WHITE);
    display.print("Connexion Wi-Fi\n");
    display.print("\n");
    display.print("Name: ESP32_CONFIG\n");
    display.print("MDP: 12345678\n");
    display.print("\n");
    display.print("Web Page: ");
    display.print(IP);
    display.display();

    server.on("/", std::bind(&WiFiManager::handleRoot, this));
    server.on("/connect", std::bind(&WiFiManager::handleConnect, this));
    server.begin();
    Serial.println("Serveur HTTP démarré");
}

void WiFiManager::handleRoot() {
    String html = "<html><body>";
    html += "<form action='/connect' method='POST'>";
    html += "SSID: <input type='text' name='ssid'><br>";
    html += "Password: <input type='password' name='password'><br>";
    html += "<input type='submit' value='Connect'>";
    html += "</form>";
    html += "</body></html>";

    server.send(200, "text/html", html);
}

void WiFiManager::handleConnect() {
    String newSSID = server.arg("ssid");
    String newPassword = server.arg("password");

    if (!newSSID.isEmpty() && !newPassword.isEmpty()) {
        server.send(200, "text/html", "<h1>Connexion en cours...</h1>");
        delay(1000);

        WiFi.softAPdisconnect(true);
        WiFi.mode(WIFI_STA);
        WiFi.begin(newSSID.c_str(), newPassword.c_str());

        if (WiFi.waitForConnectResult() == WL_CONNECTED) {
            server.send(200, "text/html", "<h1>Connecté avec succès ! Redémarrez l'ESP32.</h1>");
            ESP.restart();
        } else {
            server.send(200, "text/html", "<h1>Échec de la connexion. Vérifiez vos informations et réessayez.</h1>");
            createAccessPoint();
        }
    } else {
        server.send(400, "text/html", "<h1>Erreur : SSID et mot de passe ne doivent pas être vides.</h1>");
    }
}

String generateRandomString() {
    String randomString = "";

    for (int i = 0; i < 4; i++) {
        randomString += String(random(0, 10));
    }
    randomString += "-";
    for (int i = 0; i < 5; i++) {
        randomString += String(random(0, 10));
    }
    randomString += "-";
    for (int i = 0; i < 4; i++) {
        randomString += String(random(0, 10));
    }

    return randomString;
}
