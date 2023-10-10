import copy
import os
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from PIL import Image

import note_seq
from note_seq.sequences_lib import Pianoroll
import numpy as np
import pretty_midi

#======================================================================
#reading MIDI file

midi_dir = Path('/Users/willsaliba/Documents/Topics/ReaScripts/outputs')
fname = midi_dir / 'original.mid'

with open(fname, 'rb') as f:
    seq = note_seq.midi_to_note_sequence(f.read())

print("\nsuccessfully read file\n") 
#======================================================================
#initialising function to extract variables

MIN_DRUM_PITCH = 27
MAX_DRUM_PITCH = 87

def extract_example(
        seq: note_seq.NoteSequence, start_sec: float, dur_sec: float, roll_freq: float,
        ) -> Optional[Tuple[Dict[int, Pianoroll], Pianoroll]]:
    """Returns example as a roll."""
    # Note: extract_subsequence requires *not* quantized!
    subseq = note_seq.extract_subsequence(seq, start_sec, start_sec + dur_sec)

    drum_subseq = filter_notes(
        subseq,
        pred_fn=lambda note: note.is_drum)
    instrument_subseqs = group_notes(
        subseq,
        key_fn=lambda note: note.program // 8,
        pred_fn=lambda note: True)

    if not instrument_subseqs:
        return None

    drum_roll = note_seq.sequence_to_pianoroll(
        drum_subseq, roll_freq,
        min_pitch=MIN_DRUM_PITCH, max_pitch=MAX_DRUM_PITCH)
    instrument_rolls = {
        group_id: note_seq.sequence_to_pianoroll(
            instrument_subseqs[group_id],
            roll_freq,
            min_pitch=note_seq.MIN_MIDI_PITCH,
            max_pitch=note_seq.MAX_MIDI_PITCH)
        for group_id in instrument_subseqs
    }

    # All pianorolls must have same shape.
    _, = set(tuple(roll.active.shape) for roll in instrument_rolls.values())

    return instrument_rolls, drum_roll

def group_notes(sequence, key_fn, pred_fn, keys=None):
    """Group notes according to key_fn, filtering by pred_fn.

    Operates on notes, control_changes and pitch_bends:
    element types with {instrument, program, is_drum} fields.
    Does not re-index instruments.

    Based on: note_seq.sequences_lib._extract_subsequences
    """

    subsequence = note_seq.NoteSequence()
    subsequence.CopyFrom(sequence)
    del subsequence.notes[:]
    del subsequence.control_changes[:]
    del subsequence.pitch_bends[:]
    del subsequence.text_annotations[:]
    # TODO: subsequence.instrument_infos?

    if not keys:
        keys = set(key_fn(note) for note in sequence.notes if pred_fn(note))

    subsequences = {k: copy.deepcopy(subsequence) for k in keys}
    for field in ['notes', 'control_changes', 'pitch_bends']:
        for elem in getattr(sequence, field):
            if not pred_fn(elem):
                continue
            key = key_fn(elem)
            if key not in subsequences:
                continue
            getattr(subsequences[key], field).extend([elem])

    return subsequences

def filter_notes(sequence, pred_fn):
    """Filter notes according to pred_fn.

    Operates on notes, control_changes and pitch_bends:
    element types with {instrument, program, is_drum} fields.
    Does not re-index instruments.

    Based on: note_seq.sequences_lib._extract_subsequences
    """

    subsequence = note_seq.NoteSequence()
    subsequence.CopyFrom(sequence)
    del subsequence.notes[:]
    del subsequence.control_changes[:]
    del subsequence.pitch_bends[:]
    del subsequence.text_annotations[:]  # unused
    # TODO: subsequence.instrument_infos?

    for field in ['notes', 'control_changes', 'pitch_bends']:
        for elem in getattr(sequence, field):
            if not pred_fn(elem):
                continue
            getattr(subsequence, field).extend([elem])

    return subsequence

print("successfully intialised extract_example function \n") 
#======================================================================
# Wrap bpm to [60, 120) 

bpm = seq.tempos[0].qpm
min_bpm = 60
bpm = 2**(np.log2(bpm / min_bpm) % 1) * min_bpm

beats_per_sec = bpm / 60
dur_sec = 16 / beats_per_sec  # 4 times 4 beats
pixels_per_beat = 12
pixels_per_sec = pixels_per_beat * beats_per_sec

print("successfully wrapped bpm to [60, 120) \n") 
#======================================================================
#extarcting instrument rolls from MIDI segment

instrument_rolls, drum_roll = extract_example(
    seq,
    start_sec=30,
    dur_sec=dur_sec,
    roll_freq=pixels_per_sec)

sorted(instrument_rolls.keys())

list(enumerate(pretty_midi.constants.INSTRUMENT_CLASSES))

print("successfully extarcting instrument rolls \n") 
#======================================================================
#initialise data members for saving loop

# Takes in piano roll numPy array and file name to save the image at this location
def save_pianoroll_as_image(pianoroll, filename):
    img = np.where(pianoroll > 0, 255, 0).astype('uint8')
    img = img.T  # Transpose to make it horizontal
    img = Image.fromarray(img, 'L')
    img.save(filename)

group_id = 0
total_duration = seq.total_time 
segment_duration = 32 / beats_per_sec  
counter = 0

print("successfully prepare to perform saving loop \n") 
#======================================================================
#loop to saves all instrument rolls

# Loop from start to end of song in  32 beat "windows"
for start_time in np.arange(0, total_duration, segment_duration):
    # Extract 
    instrument_rolls, drum_roll = extract_example(
        seq, # This song
        start_sec=start_time, # Start of Segment time
        dur_sec=segment_duration,  # 32 beats
        roll_freq=pixels_per_sec   # Defined in Jack Notebook
    )

    # Go through each instrument of this window
    for group_id, roll in instrument_rolls.items():

        # Create directory to save this piano roll to
        family_name = pretty_midi.constants.INSTRUMENT_CLASSES[group_id]
        family_dir = f"{midi_dir}/{family_name}"
        os.makedirs(family_dir, exist_ok=True)
        
        cropped_roll = roll.active[:384, :128] # Vertical to vertical transformation, transpose is saved to get required dims 
        
        # Save piano roll image in the directory
        filename = f"{family_dir}/segment_{counter}.png"
        save_pianoroll_as_image(cropped_roll, filename)
    
    # Drums
    family_name = "Drums"
    family_dir = f"{midi_dir}/{family_name}"
    os.makedirs(family_dir, exist_ok=True)
    cropped_roll = roll.active[:384, :128] 
    filename = f"{family_dir}/segment_{counter}.png"
    save_pianoroll_as_image(cropped_roll, filename)

    counter += 1


print("SUCESSFULLY SAVED ALL ROLLS!\n")
#/Users/willsaliba/Documents/Topics/ReaScripts/script.py
#source /Users/willsaliba/opt/anaconda3/bin/activate base