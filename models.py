# contains wrapper classes used by all files in this program

class Note(object):
    """
    Wrapper class for a midi note.
    
    ...
    
    Attributes
    ----------
    midi_val : int
        Value of this note in the MIDI format. Only values on or between 0 and 127 are valid. See http://computermusicresource.com/midikeys.html for a complete list.

    velocity : int
        The 'force' with which a note is played. Only values on or between 0 and 127 are valid. Some midi files have note_on events with a velocity of 0; these should be 
          treated the same as a 'note_off' event.
    """
    
    def __init__(self, midi_note, beat_span = 1, velocity = 64, length = None):
        self.midi_note = midi_note
        self.beat_span = beat_span
        self.velocity = velocity
        self.length = length
        
    def __str__(self):
        return "midi value = {midi}, beat span = {bs}, velocity = {v}, length={l}".format(midi=self.midi_note, bs=self.beat_span, v=self.velocity, l=self.length) 

class Beat(object):
    
    def __init__(self, num, note):
        self.num = num
        self.note = note
    
    def __str__(self):
        return "Beat number = {bn}, note = {n}".format(bn=self.num, n=self.note)

class Bar(object):

    def __init__(self, num_beats = 4, beat_length = 20):
        self.num_beats = num_beats
        self.beat_length = beat_length
        self.beats = [Beat(num=x, note=None) for x in range(num_beats)]
    
    def __str__(self):
        return "Number of beats = {nb}, Length of beat = {lb}, values = {b}".format(nb=self.num_beats, lb=self.beat_length, b=self.beats)

class Track(object):

    def __init__(self, name, bars, program, channel = None, tempo = 120):
        self.name = name
        self.bars = bars
        self.program = program
        self.channel = channel
        self.tempo = tempo


class Configuration:
    """
    Contains configuration options for generating notes
    
    ...
    
    Attributes
    ----------
    times_to_loop : int
        The number of times the generated note pattern should loop in the end file. Set to None to prevent looping.
    ppq : int
        The Pulses Per Quarternote (PPQ) of the midi file. This is sometimes called 'ticks per quarternote'.
    tempo : int
        The starting tempo of a track. Note, this could be changed multiple times in the track itself.
    midi_program : int
        The 'program' the midi file should be initially set to. See https://www.recordingblogs.com/wiki/midi-program-change-message for a list of program values.
    model_location : str
        The location of the CSV file that the resulting midi file should be modeled on.
    root_note : int 0-127
        The starting note of the track. This will be used to generate the following notes.
    note_selection_lower_bound : int
    note_selection_upper_bound : int
        In order to prevent large jumps in octaves you can specify an upper and lower bound. This will ensure that the subsequent note falls within this bound.
    same_note_bias : float
        An additional bias that is applied when calculating that next notes probabilities to prevent the same note being chosen too often.
    max_beat_length : int
        The maximum number of beats a note can be played for continiously.
    min_beat_length : int
        The minimum number of beats a note can be played for continiously.
    max_silence_beat_length : int
        The maximum number of beats a silent note can be played for.
    min_silence_beat_length: int
        The minimum number of beats a silent note can be played for.
    weight_to_play_note : int
        The chance that a note will be played.
    weight_to_not_play : int
        The chance that a note will not be played.
    rhythm_length : int
        How many notes are played. This includes silent notes.
    velocity : int
        The velocity with which a note is played
    velocity_lower_bound : int (optional)
        If set this will randomly set a velocity for a note between velocity and the lower bound.
    velocity_upper_bound : int (optional)
        If set this will randomly set a velicity for a note between velocity and the upper bound.
    """
    
    def __init__(self, ppq, tempo, root_note, midi_program = 26, times_to_loop = None, note_selection_lower_bound = 6, note_selection_upper_bound = 6, 
                        same_note_bias = 0.5, max_beat_length = 80, min_beat_length = 1, max_silence_beat_length = 10, min_silence_beat_length = 1, 
                        weight_to_play_note = 30, weight_to_not_play = 70, rhythm_length = 8, velocity = 100, velocity_lower_bound = None, velocity_upper_bound = None):
        self.ppq = ppq
        self.tempo = tempo
        self.midi_program = midi_program
        self.root_note = root_note
        self.times_to_loop = times_to_loop
        self.note_selection_lower_bound = note_selection_lower_bound
        self.note_selection_upper_bound = note_selection_upper_bound
        self.same_note_bias = same_note_bias
        self.max_beat_length = max_beat_length
        self.min_beat_length = min_beat_length
        self.max_silence_beat_length = max_silence_beat_length
        self.min_silence_beat_length = min_silence_beat_length
        self.weight_to_play_note = weight_to_play_note
        self.weight_to_not_play = weight_to_not_play
        self.rhythm_length = rhythm_length
        self.velocity = velocity
        self.velocity_lower_bound = velocity_lower_bound
        self.velocity_upper_bound = velocity_upper_bound

    
