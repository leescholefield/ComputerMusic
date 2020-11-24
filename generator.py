import random
from models import Note, Bar

# the standard 12 notes starting at C
notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def get_notes_in_major_scale(root_note):
    """
    Returns an array containing all the notes in the major scale of root_note
    
    The notes in a scale are determined according to the following formula:
        WWHWWWH
    W = whole-step
    H = half-step
    """
    result = [root_note]
    
    index = notes.index(root_note)
    offsets = [2,2,1,2,2,2,1]
    for x in offsets:
        index += x
        wrapped_index = index % 12
        result.append(notes[wrapped_index])
        #print(result)
     
    return result

def get_notes_in_minor_scale(root_note):
    """
    Returns an array containing all the notes in the minor scale of root_note.
    
    The notes in a scale are determined according to the following formula:
        WHWWHWW
    W = whole-step
    H = half-step
    """
    result = [root_note]
    # get starting notes index
    
    index = notes.index(root_note)
    offsets = [2,1,2,2,1,2,2]
    for x in offsets:
        index += x
        wrapped_index = index % 12
        result.append(notes[wrapped_index])
     
    return result

def get_chords_in_major_scale(root_note):
    notes = get_notes_in_major_scale(root_note)
    # delete the repeating root note from our scale since it messes up our algorithm
    del notes[-1]
    
    res = [] # list of lists
    for i in range(len(notes)):
        n = [notes[i], notes[ (i + 2) % len(notes)], notes[ (i + 4) % len(notes)]]
        res.append(n)
    
    return res

def get_chords_in_minor_scale(root_note):
    notes = get_notes_in_minor_scale(root_note)
    # delete the repeating root note from our scale since it messes up our algorithm
    del notes[-1]
    
    res = [] # list of lists
    for i in range(len(notes)):
        n = [notes[i], notes[ (i + 2) % len(notes)], notes[ (i + 4) % len(notes)]]
        res.append(n)
    
    return res

# octave -1
first_octave_vals = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5,
        "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}
def get_midi_value(s_note, octave = 4):
    """
    Returns the midi value of a note in the specified octave.
    
    The midi spec has 11 octaves from -1 to 9. Each time we go up an octave we add 12 to the notes base value (its value in the -1 - the first - octave). 
    """
    # there are no values for these notes in the 9th octave
    # for now return the values in the 8th octave -- may want to throw error in future
    if s_note in ["G#", "A", "A#", "B"] and octave == 9:
        octave = 8
    
    return first_octave_vals[s_note] + ( (octave+1) * 12)

def get_note_name(midi_val, octave):
    val = (octave-2) / 12
    
    return first_octave_vals[val]

def convert_chords_to_midi_values(chords, key, octave = 4):
    
    root_note_val = first_octave_vals[key] + ( (octave+2) * 12)
    
    res = []
    for chord in chords:
        # todo -- clean this mess up
        first = first_octave_vals[chord[0]] + ( (octave+2) * 12)
        if first < root_note_val:
            first += 12
        second = first_octave_vals[chord[1]] + ( (octave+2) * 12)
        while second < first:
            second += 12
        third = first_octave_vals[chord[2]] + ( (octave+2) * 12)
        while third < first:
            third += 12
        res.append([first, second, third])
    
    return res
        
def generate_melody(bars, root_note, octave = 4, available_note_lengths = [1, 2, 4, 8], available_note_lengths_weights = [60, 20, 15, 5]):
    # for every beat in the bar decide if we want to play note
    # how many beats should the note last?
    available_notes = get_notes_in_major_scale(root_note)
    
    # probability a note will be played on a beat
    # is adjusted based on last value
    to_play = 30
    to_not_play = 70
    
    for bar in bars:
        for i in range(bar.num_beats):
            should_play = random.choices([1,0], weights=[to_play, to_not_play], k=1)[0]
            if should_play == 1:
                note_val = random.choices(available_notes, k=1)[0]
                note_val = get_midi_value(note_val, octave) # 4th octave for now

                length = random.choices(available_note_lengths, weights=available_note_lengths_weights, k=1)[0]
                note = Note(note_val, 1, 100, length)
                
                bar.beats[i].note = note
                
                # adjust probabilities
                to_play -= 5
                to_not_play += 5
                # need to decide on length -- can play over multiple beats
            else:
                to_play += 5
                to_not_play -= 5
    return bars

def alter_melody(bars, root_note, octave = 4, alter_chance=10):
    available_notes = get_notes_in_major_scale(root_note)
    
    for bar in bars:
        for beat in bar.beats:
            if beat.note is not None:
                # should alter
                should_alter = random.choices([1,0], weights=[alter_chance, 100-alter_chance], k=1)[0]
                if should_alter == 1:
                    # should we move it up or down scale?
                    # up for now
                    beat.note.midi_note = get_midi_value(random.choices(available_notes, k=1)[0], octave)
    return bars
                    

def generate_bass(bars, root_note, octave = 4, available_note_lengths = [1, 2, 4, 8], available_note_lengths_weights = [60, 20, 15, 5]):
    
    available_notes = get_notes_in_major_scale(root_note)
    
    # probability a note will be played on a beat
    # is adjusted based on last value
    to_play = 30
    to_not_play = 70
    
    # play on first beat of bar
    for bar in bars:
        for i in range(bar.num_beats):
            should_play = random.choices([1,0], weights=[to_play, to_not_play], k=1)[0]
            if should_play == 1:
                note_val = random.choices(available_notes, k=1)[0]
                note_val = get_midi_value(note_val, octave)
                
                length = random.choices(available_note_lengths, weights=available_note_lengths_weights, k=1)[0]
                note = Note(note_val, 1, 70, length)
                
                bar.beats[i].note = note
                # adjust probabilities
                to_play -= 5
                to_not_play += 5
                # need to decide on length -- can play over multiple beats
            else:
                to_play += 5
                to_not_play -= 5
                
    return bars

def generate_drums(bars):
    """
    39 - electric snare
    37 - acoustic snare
    """
    
    snare = 39
    kick = 35
    
    # create a pattern in first bar then repeat it for remaining bars
    for i in range(bars[0].num_beats):
            # whether to play note
            should_play = random.choices([1,0], weights=[60, 40], k=1)[0]
            if should_play == 1:
                # what instrument to play
                ins = random.choices([snare, kick], weights=[30, 70], k=1)[0]
                bars[0].beats[i].note = Note(ins, 1, 80)
    
    # repeat pattern for remaining bars
    # this assumes all bars have same num beats
    for bar in bars[1:]:
        bar.beats = bars[0].beats.copy()

    return bars

def generate_constant_drums(bars, *notes):
    """
    Applies a pre-determined pattern to the individual bars.
    
    Parameters
    .........
    *notes : tuples containing the midi note to be played and the index of which beat it should be played on.
    """
    
    for bar in bars:
        for arg in notes:
            midi_note = arg[0]
            for x in arg[1:]: # skip first element
                bar.beats[x].note = Note(midi_note, 1, 80)
    
    return bars
    

def generate_chords(bars, root_note, major=True, beats = None):
    if major:
        chords = get_chords_in_major_scale(root_note)
    else:
        chords = get_chords_in_minor_scale(root_note)
        
    chords = convert_chords_to_midi_values(chords, root_note, 2)   
    
    for bar in bars:
        if beats is not None:
            for i in beats:
                chord_notes = random.choices(chords, k=1)[0]
                notes = [Note(chord_notes[x]) for x in range(len(chord_notes))]
                bar.beats[i].note = notes
        else:
            for i in range(bars[0].num_beats):
                # whether to play note
                should_play = random.choices([1,0], weights=[40, 60], k=1)[0]
                if should_play == 1:
                    chord_notes = random.choices(chords, k=1)[0]
                    notes = [Note(chord_notes[x]) for x in range(len(chord_notes))]
                    bar.beats[i].note = notes
    
    return bars
            
if __name__ == "__main__":
   bars = [Bar(), Bar(), Bar(), Bar(), Bar(), Bar(), Bar(), Bar()]
   res = generate_chords(bars, "A")
   for b in res:
        print(b)
        
    
    
