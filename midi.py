import pygame
from midiutil import MIDIFile
import re


NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
OCTAVES = range(11)
NOTES_IN_OCTAVE = len(NOTES)
PATTERN = r"([A-G]#?)(\d)"


def notes_to_numbers(notes: list[str]) -> list[int]:

    numbers = []
    
    
    for note in notes:
        m = re.match(PATTERN, note)
        pitch = m.group(1)
        octave = int(m.group(2))
        
        assert pitch in NOTES
        assert octave in OCTAVES

        num = NOTES.index(pitch)
        num += (NOTES_IN_OCTAVE * octave)

        assert 0 <= num <= 127
        numbers.append(num)

    return numbers

def writeToMidi(notes: list[str], filename: str):
   
    track = 0
    channel = 0
    time = 0  # In beats
    duration = 1  # In beats
    tempo = 100  # In BPM
    volume = 100  # 0-127, as per the MIDI standard

    midi = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
    # automatically)
    midi.addTempo(track, time, tempo)

    for i, pitch in enumerate(notes_to_numbers(notes)):
        midi.addNote(track, channel, pitch, time + i, duration, volume)

    with open(filename, "wb") as output_file:
        midi.writeFile(output_file)
   
def playMidi(filename):

    clock = pygame.time.Clock()
    # Mixer config
    freq = 44100  # audio CD quality
    bitsize = -16   # unsigned 16 bit
    channels = 1  # 1 is mono, 2 is stereo
    buffer = 1024   # number of samples
    pygame.mixer.init(freq, bitsize, channels, buffer)
    pygame.mixer.music.set_volume(0.8) # 0-1
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    
    try:
        while pygame.mixer.music.get_busy():
            clock.tick(30) # Check if playback has finished
    
    except KeyboardInterrupt:
        # If user hits Ctrl/C then exit
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.stop()
        raise SystemExit


seq = ['C6','D4','D#4','F4','C5','A#4','B4']
filename = "test.mid"

writeToMidi(seq, filename)
playMidi(filename)