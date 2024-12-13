#include "FirebaseManager.h"

FirebaseData fbdo;
FirebaseAuth auth;
FirebaseConfig config;

#define API_KEY "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
#define FIREBASE_PROJECT_ID "green-genius-fb24"
#define USER_EMAIL "portail@green-genius-quiz.com"
#define USER_PASSWORD "xxxxxxxxxx"

int zeros[10];



FirebaseManager::FirebaseManager(String& connexionToken, String& token)
  : connexionToken(connexionToken), token(token) {}



String FirebaseManager::generateRandomString() {
  String randomString = "";

  for (int i = 0; i < 4; i++) {
    randomString += String(random(0, 10));
  }
  randomString += "-";
  for (int i = 0; i < 4; i++) {
    randomString += String(random(0, 10));
  }
  randomString += "-";
  for (int i = 0; i < 4; i++) {
    randomString += String(random(0, 10));
  }

  return randomString;
}



void FirebaseManager::firestoreStart() {
  config.api_key = API_KEY;
  config.database_url = String(FIREBASE_PROJECT_ID) + ".firebaseio.com";
  auth.user.email = USER_EMAIL;
  auth.user.password = USER_PASSWORD;

  // Assurez-vous que Firebase se reconnecte automatiquement
  Firebase.reconnectWiFi(true);
  Firebase.reconnectNetwork(true);
  Firebase.setDoubleDigits(5);

  fbdo.setBSSLBufferSize(4096 /* Rx buffer size in bytes from 512 - 16384 */, 1024 /* Tx buffer size in bytes from 512 - 16384 */);
  fbdo.setResponseSize(4096);

  config.timeout.networkReconnect = 10 * 1000;
  config.timeout.socketConnection = 10 * 1000;
  config.timeout.serverResponse = 10 * 1000;
  config.timeout.rtdbKeepAlive = 45 * 1000;
  config.timeout.rtdbStreamReconnect = 1 * 1000;
  config.timeout.rtdbStreamError = 3 * 1000;
  config.tcp_data_sending_retry = 1;

  Firebase.begin(&config, &auth);

  if (Firebase.ready()) {
    String randomID = generateRandomString();
    connexionToken = randomID;
    token = randomID;

    FirebaseJson content;
    content.set("fields/connexion/booleanValue", false);

    if (Firebase.Firestore.createDocument(&fbdo, FIREBASE_PROJECT_ID, "", "Portail/" + randomID, content.raw())) {
      for (int i = 0; i < 10; ++i) {
        zeros[i] = 0;
      }

      Serial.print("Données écrites avec succès, token: ");
      Serial.println(randomID);
    } else {
      Serial.println("Échec de l'écriture des données");
      Serial.println(fbdo.errorReason());
    }
  } else {
    Serial.println("Firebase is not ready");
  }
}



FirebaseJson FirebaseManager::firestoreRead(const String& ID) {
  FirebaseJson jsonData;

  if (Firebase.ready()) {
    
    String documentPath = "Portail/" + ID;
    Serial.println("Get a document");

    if (Firebase.Firestore.getDocument(&fbdo, FIREBASE_PROJECT_ID, "", documentPath.c_str())) {
      jsonData.setJsonData(fbdo.payload().c_str());
    } else {
      Serial.print("Failed to get document: ");
      Serial.println(fbdo.errorReason());
    }

    fbdo.clear();
  } else {
    Serial.println("Firebase is not ready");
  }
  return jsonData;
}



void FirebaseManager::firestoreSelectQuestion(const String& ID, int questionNumber, int response) {

  if (Firebase.ready()) {

    String documentPath = "Portail/" + ID;

    zeros[questionNumber] = response;

    FirebaseJson content;
    for (int i = 0; i < 10; i++) {
      String progressPath = "fields/progress/arrayValue/values/[" + String(i) + "]/integerValue";
      content.set(progressPath, zeros[i]);
    }

    String updateMask = "progress, connexion";

    Serial.println("Edit question");

    if (Firebase.Firestore.patchDocument(&fbdo, FIREBASE_PROJECT_ID, "", documentPath.c_str(), content.raw(), updateMask.c_str())) {
      Serial.println("Document updated successfully!");
    } else {
      Serial.println("Failed to update document: " + fbdo.errorReason());
    }

  } else {
    Serial.println("Firebase is not ready");
  }
}
