
import note_seq
import librosa
import pretty_midi
from datetime import datetime

# WAV dosyasını oku
audio_path = "ornek_muzik.wav"  # buraya kendi dosyanı yaz
audio, sr = librosa.load(audio_path, sr=16000)

# Onsets and Frames kullanarak transkripsiyon yap
transcription = note_seq.midi_io.audio_to_note_sequence(audio, sample_rate=sr)

# Notaları çıkar
notes = []
for note in transcription.notes:
    pitch = note.pitch
    start = note.start_time
    end = note.end_time
    notes.append((pitch, start, end))

# TXT dosyasına yaz
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
txt_file = f"transcription_{timestamp}.txt"
with open(txt_file, "w") as f:
    for pitch, start, end in notes:
        name = pretty_midi.note_number_to_name(pitch)
        f.write(f"{start:.2f}s - {name} - {end:.2f}s\n")

# MIDI dosyası oluştur
midi = pretty_midi.PrettyMIDI()
instrument = pretty_midi.Instrument(program=0)
for pitch, start, end in notes:
    note = pretty_midi.Note(velocity=100, pitch=pitch, start=start, end=end)
    instrument.notes.append(note)
midi.instruments.append(instrument)
midi_file = f"transcription_{timestamp}.mid"
midi.write(midi_file)

print(f"TXT dosyası: {txt_file}")
print(f"MIDI dosyası: {midi_file}")

# import pretty_midi
# from datetime import datetime

# # Örnek notalar (MIDI pitch, start, end) — çok sesli olabilir
# example_notes = [
#     (60, 0.0, 0.5),  # C4
#     (64, 0.5, 1.0),  # E4
#     (67, 1.0, 1.5),  # G4
#     (72, 1.5, 2.0)   # C5
# ]

# def midi_pitch_to_note_name(pitch):
#     return pretty_midi.note_number_to_name(pitch)

# def write_txt(notes, filename):
#     with open(filename, "w") as f:
#         for pitch, start, end in notes:
#             f.write(f"{start:.2f}s - {midi_pitch_to_note_name(pitch)} - {end:.2f}s\n")

# def write_midi(notes, filename):
#     midi = pretty_midi.PrettyMIDI()
#     instrument = pretty_midi.Instrument(program=0)
#     for pitch, start, end in notes:
#         note = pretty_midi.Note(velocity=100, pitch=pitch, start=start, end=end)
#         instrument.notes.append(note)
#     midi.instruments.append(instrument)
#     midi.write(filename)

# # Dosya adları
# timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
# txt_filename = f"transcribed_{timestamp}.txt"
# midi_filename = f"transcribed_{timestamp}.mid"

# # Kaydet
# write_txt(example_notes, txt_filename)
# write_midi(example_notes, midi_filename)
