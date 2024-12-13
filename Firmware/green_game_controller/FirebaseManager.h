#ifndef FIREBASE_MANAGER_H
#define FIREBASE_MANAGER_H

#include <Firebase_ESP_Client.h>

extern FirebaseData fbdo;
extern FirebaseAuth auth;
extern FirebaseConfig config;

class FirebaseManager {
public:
    FirebaseManager(String& connexionToken, String& token);
    void firestoreStart();
    FirebaseJson firestoreRead(const String& ID);
    void firestoreSelectQuestion(const String& ID, int questionNumber, int response);

private:
    String& connexionToken;
    String& token;
    String generateRandomString();
};

#endif

