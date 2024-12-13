#include "MelodyPlayer.h"

MelodyPlayer::MelodyPlayer(int pin) : _pin(pin) {
    pinMode(_pin, OUTPUT);
}

void MelodyPlayer::playStartupMelody() {
    int melody[] = {262, 294, 330, 349, 392, 440, 494, 523};
    int noteDurations[] = {4, 4, 4, 4, 4, 4, 4, 4};
    int length = sizeof(melody) / sizeof(melody[0]);
    playMelody(melody, noteDurations, length);
}

void MelodyPlayer::playVictoryMelody() {
    int melody[] = {523, 587, 659, 698, 784, 880, 988, 1047};
    int noteDurations[] = {4, 4, 4, 4, 4, 4, 4, 4};
    int length = sizeof(melody) / sizeof(melody[0]);
    playMelody(melody, noteDurations, length);
}

void MelodyPlayer::playDefeatMelody() {
    int melody[] = {523, 494, 440, 392, 349, 330, 294, 262};
    int noteDurations[] = {4, 4, 4, 4, 4, 4, 4, 4};
    int length = sizeof(melody) / sizeof(melody[0]);
    playMelody(melody, noteDurations, length);
}

void MelodyPlayer::playMelody(int melody[], int noteDurations[], int length) {
    for (int thisNote = 0; thisNote < length; thisNote++) {
        int noteDuration = 1000 / noteDurations[thisNote];
        tone(_pin, melody[thisNote], noteDuration);

        int pauseBetweenNotes = noteDuration * 1.30;
        delay(pauseBetweenNotes);

        noTone(_pin);
    }
}
