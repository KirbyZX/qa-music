from mido import Message, MidiFile, MidiTrack
import midi

mid = MidiFile('fur_elise.mid')

new = MidiFile()
track = MidiTrack()
new.tracks.append(mid.tracks[0])
new.tracks.append(track)

for msg in mid.tracks[1]:
    if not msg.is_meta and msg.channel == 0:
        track.append(msg)


new.save("new.mid")
midi.playMidi("new.mid")