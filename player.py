import mido
import generator
import midi
import waltz
import copy
from models import Bar, Track

def main():

   bars_bass = [Bar(), Bar(), Bar(), Bar()]
   bass = generator.generate_bass(bars_bass, "C", octave=1) * 20
   
   melody = None
   for x in range(5):
        bars_melody = [Bar(), Bar(), Bar(), Bar(), Bar(), Bar(), Bar(), Bar()]
        if melody is None:
            melody = (generator.generate_melody(bars_melody, "C") * 2)
        else:
            melody += (generator.generate_melody(bars_melody, "C") * 2)
   
   drum_bars = [Bar(), Bar(), Bar(), Bar(), Bar(), Bar(), Bar(), Bar()]
   drums = generator.generate_drums(drum_bars) * 10
   
   chord_bars = [Bar(), Bar(), Bar(), Bar()]
   chords = generator.generate_chords(chord_bars, "C", major=True, beats=[0]) * 20
    
   #file = midi.create_midi_file([Track("drums", bass, 38, tempo=50)])
   file = midi.create_midi_file([Track("bass", bass, 38), Track("melody", melody, 81), Track("drums", drums, 0, 9, 50), Track("chords", chords, 50)])
   #file = midi.create_midi_file([Track("chords", melody, 38)])
   # save file
   with open('testing.mid', 'wb') as out_file:
        file.writeFile(out_file)

def gen_waltz():
    bars = [Bar(3), Bar(3), Bar(3), Bar(3), Bar(3), Bar(3), Bar(3), Bar(3)]
    chords = waltz.generate_chord_progression(bars, "C") * 5
    
    melody_bars = [Bar(3), Bar(3), Bar(3), Bar(3), Bar(3), Bar(3), Bar(3), Bar(3)]
    melody = generator.generate_melody(melody_bars, "C") * 5
    
    file = midi.create_midi_file([Track("chords", chords, 3, 0, tempo = 60), Track("melody", melody, 3,1,  tempo = 30)], 80)
    
    with open('waltz.mid', 'wb') as out_file:
       file.writeFile(out_file)

def alter_test():
    melody = generator.generate_melody([Bar(), Bar()], "C", octave=4)
    # deep copy
    for x in range(5):
        c = copy.deepcopy(melody[:2])
        melody.extend(generator.alter_melody(c, "C", octave=4, alter_chance=30))
        
    for bar in melody:
        for beat in bar.beats:
            print(beat.note)
    
    file = midi.create_midi_file([Track("melody", melody, 81)], 80)
    
    with open('alter.mid', 'wb') as out_file:
       file.writeFile(out_file)
   
if __name__ == "__main__":
    main()