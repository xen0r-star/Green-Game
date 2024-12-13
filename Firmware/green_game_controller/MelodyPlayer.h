#ifndef MELODY_PLAYER_H
#define MELODY_PLAYER_H

#include <Arduino.h>

class MelodyPlayer {
public:
    MelodyPlayer(int pin);
    void playStartupMelody();
    void playVictoryMelody();
    void playDefeatMelody();
private:
    int _pin;
    void playMelody(int melody[], int noteDurations[], int length);
};

#endif
