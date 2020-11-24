""" 
    midi.py : Contains utility methods for interacting with midi files. The main purpose of this class in terms of this project is to pull 
    note events from a track, and convert note events into a midi file.
    
    From the command line:
    Since the track make-up of each file could be different a little manual exploration is neccessary before attempting to parse a file. For this 
    purpose this file can be called directly from the command line with the following options:
        -m --midi (required) : location of the midi file to explore
        -t --tracks (optional) : prints information for each track in the file
        -d --detailed (optional) : prints detailed information about a specified track. Calling this requires a valid track number
"""
from models import Note
import mido
import sys, getopt
from midiutil import MIDIFile

def create_midi_file(tracks, ppq = 120):
    file = MIDIFile(len(tracks), ticks_per_quarternote=ppq, eventtime_is_ticks=True) # one track
    
    for i in range(len(tracks)):
        # add program change and tempo to file object
        file.addProgramChange(i, i, 0, tracks[i].program)
        channel = tracks[i].channel or i
        file.addTempo(i, channel, tracks[i].tempo)
        
        bars = tracks[i].bars
        cur_tick = 0
        for bar in bars:
            for beat in bar.beats:
                if beat.note is not None:
                    # check if single or list of notes
                    if isinstance(beat.note, list):
                        for n in beat.note:
                            length = n.length or bar.beat_length
                            file.addNote(i, channel, n.midi_note, cur_tick, length * n.beat_span, n.velocity)
                    else:
                        file.addNote(i, channel, beat.note.midi_note, cur_tick, bar.beat_length * beat.note.beat_span, beat.note.velocity)
                cur_tick += bar.beat_length
    
    return file

def calculate_tick_duration(tempo, ppq):
	"""
	Returns the duration of a single 'tick'.
	
	Paramters
	---------
	tempo: number
		the current tempo. If this changes in the MIDI file the tick duration would need to be recalculated.
	ppq: number
		Pulses-Per-Quater (sometimes refered to as Ticks-Per-Quater). This should be defined in a MIDI header and won't change.
	"""
	bpm = (60 * 1000000) / tempo
	dur = 60000 / (bpm * ppq)
	return dur
 
def extract_notes_in_track(midi_track, tick_dur):
    notes = {}
    count = 0
    
    notes = []
    
    # some midi files have note_on events with a velocity of 0. These are treated the same as note_off events
    # dirty trick to make sure a note_on event is treated the same as a note_off
    velocity_zero_flag = False
    current_tick = 0 # current tick we're on
    for msg in midi_track:
        if msg.type == 'note_on':
            velocity = msg.velocity
            # note_on events with a velocity of 0 are the same as a note_off event
            if (velocity == 0):
                velocity_zero_flag = True
            else:
                # reset flag if previous msg caused it to set
                velocity_zero_flag = False
                
                on_time = tick_dur * current_tick
                n = msg.note
                ty = msg.type
                notes.append(Note(n, current_tick, on_time, None, None,  velocity))
                
                current_tick += msg.time
                
        if (velocity_zero_flag and msg.type == 'note_on') or msg.type == 'note_off':
            n = msg.note
            # get first message with that note in notes list
            el = [x for x in notes if x.midi_note == n and x.tick_off is None][0]
            # having issues where time off is same value as time on
            # if this is the case set the duration to be one tick
            if (current_tick == el.tick_on):
                current_tick += 1
                
            el.tick_off = current_tick
            el.time_off = tick_dur * current_tick
            
            current_tick += msg.time
    
    return notes
    
def main(argv):
    if len(argv) < 2:
      print('midi_utils.py -m <midifile>')
      sys.exit(2)
      
    midi_file = ''
    # flags detected in argv
    tracks_flag = False # whether we should print track info of the midifile
    detailed_flag = False # whether we should print detailed track information about a specific track
    extract_flag = False # whether we should extract the notes from a track
    
    output_loc = None
    
    try:
        opts, args = getopt.getopt(argv,"hm:td:e:o:",["help", "midi=", "tracks", "detailed=", "extract=", "output="])
    except getopt.GetoptError:
      print('midi_utils.py -m <midifile>')
      sys.exit(2)
    for opt, arg in opts:
      if opt == '-h':
         print('midi_utils.py -m <midifile>')
         sys.exit()
      elif opt in ("-m", "--midi"):
         midi_file = arg
      elif opt in ("-t", "--tracks"):
         tracks_flag = True
      elif opt in ("-d", "--detailed"):
        if arg is None or arg == "":
            print("Error: calling with arg -d without specifying a track number")
            sys.exit(2)
        track_num = int(arg)
        detailed_flag = True
      elif opt in ("-e", "--extract"):
        if arg is None or arg == "":
            print("Error: calling with arg -e without specifying a track number")
            sys.exit(2)
        extract_flag = True
        e_track_num = int(arg)
      elif opt in ("-o", "--output"):
        if arg is None or arg == "":
            print("Error: calling with arg -o without specifying an output location")
            sys.exit(2)
        output_loc = arg
    
    # try to open file
    try:
        mf = mido.MidiFile(midi_file)
    except FileNotFoundError:
        print("Error: Could not find file at location " + midi_file)
        sys.exit(2)
    except OSError:
        print("Error: Could not read file at location " + midi_file + "\nAre you sure it's a MIDI file?")
        sys.exit(2)
    
    # print out information about the file
    num_tracks = len(mf.tracks)
    ppq = mf.ticks_per_beat
    print("Number of tracks: {num_tracks} \nPPQ: {ppq}\nType: {t}\nLength : {l}".format(num_tracks=num_tracks, ppq=ppq,t=mf.type, l=mf.length))
    
    # print out info about the tracks if flag set
    if (tracks_flag):
        for i, track in enumerate(mf.tracks):
            # try to find name
            name = [x for x in track if x.type == 'track_name']
            name_val = None
            if (len(name) > 0):
                name_val = name[0].name
            print("Track {index} : \nName = {name}".format(index=i, name=name_val))
    
    # print out info about a specified track if flag is set
    if (detailed_flag):
        print("\nMessages in track {index}".format(index=track_num))
        for i, msg in enumerate(mf.tracks[track_num]):
            print("N = {num}, T = {note}".format(num=i, note=msg))
    
    if(extract_flag):
        track = mf.tracks[e_track_num]
        notes = extract_notes_in_track(track, calculate_tick_duration(666666, ppq)) # need to change 666666
        for i, n in enumerate(notes):
            print("N = {num}, T = {note}".format(num=i, note=n))
        

if __name__ == "__main__":
   main(sys.argv[1:])

