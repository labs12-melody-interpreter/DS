import pretty_midi

md = pretty_midi.PrettyMIDI('test_output.mid')
for i in md.instruments:
   for j, note in enumerate(i.notes):
     print(note)
