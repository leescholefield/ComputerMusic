import unittest
import generator
import sys


class TestGetNotesInScale(unittest.TestCase):

    def test_get_notes_in_major_scale(self):
        scale = {"C": ["C", "D", "E", "F", "G", "A", "B", "C"], "C#":["C#", "D#", "F", "F#", "G#", "A#", "C", "C#"], 
                 "D":[ "D","E","F#","G","A","B","C#","D"], "D#" :[ "D#", "F", "G", "G#", "A#", "C", "D", "D#"], 
                 "E": ["E", "F#", "G#", "A", "B", "C#", "D#", "E"], "F": ["F", "G", "A", "A#", "C", "D", "E", "F"], 
                 "F#": ["F#",  "G#",  "A#",  "B",  "C#",  "D#", "F", "F#"], "G": ["G", "A", "B", "C", "D", "E", "F#", "G"], 
                 "G#": ["G#", "A#", "C", "C#", "D#", "F", "G", "G#"], "A": ["A", "B", "C#", "D", "E", "F#", "G#", "A"], 
                 "A#": ["A#", "C", "D", "D#", "F", "G", "A", "A#"], "B": ["B", "C#", "D#", "E", "F#", "G#", "A#", "B"] }
        
        for name, notes in scale.items():
            res = generator.get_notes_in_major_scale(name)
            self.assertEqual(res, notes)
    
    def test_get_notes_in_minor_scale(self):
        scale = {"C": ["C", "D", "D#", "F", "G", "G#", "A#", "C"], "C#":["C#", "D#", "E", "F#", "G#", "A", "B", "C#"], 
                 "D":["D", "E", "F", "G", "A", "A#", "C", "D"], "D#" :["D#", "F", "F#", "G#", "A#", "B", "C#", "D#" ], 
                 "E": ["E", "F#", "G", "A", "B", "C", "D", "E"], "F": ["F", "G", "G#", "A#", "C", "C#", "D#", "F"], 
                 "F#": ["F#", "G#", "A", "B", "C#", "D", "E","F#"], "G": ["G", "A", "A#", "C", "D", "D#", "F", "G"], 
                 "G#": ["G#", "A#", "B", "C#", "D#", "E", "F#", "G#"], "A": ["A", "B", "C", "D", "E", "F", "G", "A"], 
                 "A#": ["A#", "C", "C#", "D#", "F", "F#", "G#", "A#"], "B": ["B", "C#", "D", "E", "F#", "G","A", "B"] }
        
        for name, notes in scale.items():
            res = generator.get_notes_in_minor_scale(name)
            self.assertEqual(res, notes)

class TestGetChordsInScale(unittest.TestCase):
    
    def test_get_chords_in_major_scale(self):
        expected = {"C": [["C", "E", "G"], ["D", "F", "A"], ["E", "G", "B"], ["F", "A", "C"], ["G", "B", "D"], ["A", "C", "E"], ["B", "D", "F"]],
                    "C#":[["C#", "F", "G#"], ["D#", "F#", "A#"], ["F", "G#", "C"], ["F#", "A#", "C#"], ["G#", "C", "D#"], ["A#", "C#", "F"], ["C", "D#", "F#"]],
                    "D": [["D", "F#", "A"], ["E", "G", "B"], ["F#", "A", "C#"], ["G", "B", "D"], ["A", "C#", "E"], ["B", "D", "F#"], ["C#", "E", "G"]],
                    "D#":[["D#", "G", "A#"], ["F", "G#", "C"], ["G", "A#", "D"], ["G#", "C", "D#"], ["A#", "D", "F"], ["C", "D#", "G"], ["D", "F", "G#"]],
                    "E": [["E", "G#", "B"], ["F#", "A", "C#"], ["G#", "B", "D#"], ["A", "C#", "E"], ["B", "D#", "F#"], ["C#", "E", "G#"], ["D#", "F#", "A"]],
                    "F": [["F", "A", "C"], ["G", "A#", "D"], ["A", "C", "E"], ["A#", "D", "F"], ["C", "E", "G"], ["D", "F", "A"], ["E", "G", "A#"]],
                    "F#":[["F#", "A#", "C#"], ["G#", "B", "D#"], ["A#", "C#", "F"], ["B", "D#", "F#"], ["C#", "F", "G#"], ["D#", "F#", "A#"], ["F", "G#", "B"]],
                    "G": [["G", "B", "D"], ["A", "C", "E"], ["B", "D", "F#"], ["C", "E", "G"], ["D", "F#", "A"], ["E", "G", "B"], ["F#", "A", "C"]],
                    "G#":[["G#", "C", "D#"], ["A#", "C#", "F"], ["C", "D#", "G"], ["C#", "F", "G#"], ["D#", "G", "A#"], ["F", "G#", "C"], ["G", "A#", "C#"]],
                    "A": [["A", "C#", "E"], ["B", "D", "F#"], ["C#", "E", "G#"], ["D", "F#", "A"], ["E", "G#", "B"], ["F#", "A", "C#"], ["G#", "B", "D"]],
                    "A#":[["A#", "D", "F"], ["C", "D#", "G"], ["D", "F", "A"], ["D#", "G", "A#"], ["F", "A", "C"], ["G", "A#", "D"], ["A", "C", "D#"]],
                    "B": [["B", "D#", "F#"], ["C#", "E", "G#"], ["D#", "F#", "A#"], ["E", "G#", "B"], ["F#", "A#", "C#"], ["G#", "B", "D#"], ["A#", "C#", "E"]]}
        
        for name, chords in expected.items():
            res = generator.get_chords_in_major_scale(name)
            self.assertEqual(res, chords)
    
    def test_get_chords_in_minor_scale(self):
        expected = {"C": [["C", "D#", "G"], ["D", "F", "G#"], ["D#", "G", "A#"], ["F", "G#", "C"], ["G", "A#", "D"], ["G#", "C", "D#"], ["A#", "D", "F"]],
                    "C#":[["C#", "E", "G#"], ["D#", "F#", "A"], ["E", "G#", "B"], ["F#", "A", "C#"], ["G#", "B", "D#"], ["A", "C#", "E"], ["B", "D#", "F#"]],
                    "D": [["D", "F", "A"], ["E", "G", "A#"], ["F", "A", "C"], ["G", "A#", "D"], ["A", "C", "E"], ["A#", "D", "F"], ["C", "E", "G"]],
                    "D#":[["D#", "F#", "A#"], ["F", "G#", "B"], ["F#", "A#", "C#"], ["G#", "B", "D#"], ["A#", "C#", "F"], ["B", "D#", "F#"], ["C#", "F", "G#"]],
                    "E": [["E", "G", "B"], ["F#", "A", "C"], ["G", "B", "D"], ["A", "C", "E"], ["B", "D", "F#"], ["C", "E", "G"], ["D", "F#", "A"]],
                    "F": [["F", "G#", "C"], ["G", "A#", "C#"], ["G#", "C", "D#"], ["A#", "C#", "F"], ["C", "D#", "G"], ["C#", "F", "G#"], ["D#", "G", "A#"]],
                    "F#":[["F#", "A", "C#"], ["G#", "B", "D"], ["A", "C#", "E"], ["B", "D", "F#"], ["C#", "E", "G#"], ["D", "F#", "A"], ["E", "G#", "B"]],
                    "G": [["G", "A#", "D"], ["A", "C", "D#"], ["A#", "D", "F"], ["C", "D#", "G"], ["D", "F", "A"], ["D#", "G", "A#"], ["F", "A", "C"]],
                    "G#":[["G#", "B", "D#"], ["A#", "C#", "E"], ["B", "D#", "F#"], ["C#", "E", "G#"], ["D#", "F#", "A#"], ["E", "G#", "B"], ["F#", "A#", "C#"]],
                    "A": [["A", "C", "E"], ["B", "D", "F"], ["C", "E", "G"], ["D", "F", "A"], ["E", "G", "B"], ["F", "A", "C"], ["G", "B", "D"]],
                    "A#":[["A#", "C#", "F"], ["C", "D#", "F#"], ["C#", "F", "G#"], ["D#", "F#", "A#"], ["F", "G#", "C"], ["F#", "A#", "C#"], ["G#", "C", "D#"]],
                    "B": [["B", "D", "F#"], ["C#", "E", "G"], ["D", "F#", "A"], ["E", "G", "B"], ["F#", "A", "C#"], ["G", "B", "D"], ["A", "C#", "E"]]}
        
        for name, chords in expected.items():
            res = generator.get_chords_in_minor_scale(name)
            self.assertEqual(res, chords)
        
 

class TestGetMidiValue(unittest.TestCase):

    def test_0th_octave_scale(self):
        scale = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        expected_values = [12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
        
        for i in range(12):
            res = generator.get_midi_value(scale[i], octave=0)
            self.assertEqual(res, expected_values[i])       

    def test_1st_octave_scale(self):
        scale = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        expected_values = [24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
        
        for i in range(12):
            res = generator.get_midi_value(scale[i], octave=1)
            self.assertEqual(res, expected_values[i])
    
    def test_4th_octave_scale(self):
        scale = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        expected_values = [60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71]
        
        for i in range(12):
            res = generator.get_midi_value(scale[i], octave=4)
            self.assertEqual(res, expected_values[i])
    
    def test_minus_1_octave_scale(self):
        scale = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        expected_values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        
        for i in range(12):
            res = generator.get_midi_value(scale[i], octave=-1)
            self.assertEqual(res, expected_values[i])

    def test_8th_octave_scale(self):
        scale = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        expected_values = [108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119]
        
        for i in range(12):
            res = generator.get_midi_value(scale[i], octave=8)
            self.assertEqual(res, expected_values[i])
            
    def test_9th_octave_scale(self):
        scale = ["C", "C#", "D", "D#", "E", "F", "F#", "G"]
        expected_values = [120, 121, 122, 123, 124, 125, 126, 127]
        
        for i in range(8):
            res = generator.get_midi_value(scale[i], octave=9)
            self.assertEqual(res, expected_values[i])
    
    def test_9th_octave_scale_returns_8th_octave_for_last_4_notes(self):
        """
        The last 4 notes of the 9th octave do not have a midi value associated with them. Instead of throwing an exception we just return the notes' value from the 8th
        octave. This behaviour may change in the future.
        """
        scale = ["G#", "A", "A#", "B"]
        expected_values = [116, 117, 118, 119]
        
        for i in range(4):
            res = generator.get_midi_value(scale[i], octave=9)
            self.assertEqual(res, expected_values[i])
            
            
if __name__ == '__main__':
    unittest.main()