import numpy as np
np.complex = complex  # Fix for librosa compatibility with numpy 1.24+

import librosa
import pretty_midi
import soundfile as sf
import crepe


def hz_to_note_name(hz):
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F',
                  'F#', 'G', 'G#', 'A', 'A#', 'B']
    if hz <= 0:
        return None, None
    midi = int(round(69 + 12 * np.log2(hz / 440.0)))
    note = note_names[midi % 12]
    return note, midi


def extract_notes_with_timing(audio_path, output_txt="notes_with_time.txt"):
    y, sr = librosa.load(audio_path)
    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    times = librosa.frames_to_time(np.arange(pitches.shape[1]), sr=sr)

    results = []
    last_midi = None

    for t in range(pitches.shape[1]):
        index = magnitudes[:, t].argmax()
        pitch = pitches[index, t]
        note, midi = hz_to_note_name(pitch) if pitch > 0 else (None, None)
        if note and midi != last_midi:
            results.append((times[t], note))
            last_midi = midi

    with open(output_txt, "w") as f:
        for time, note in results:
            f.write(f"{time:.2f}s - {note}\n")

    print(f"{len(results)} zamanlı nota bulundu. '{output_txt}' dosyasına kaydedildi.")
    return results


def convert_to_midi(note_events, output_midi='output.mid'):
    midi = pretty_midi.PrettyMIDI()
    piano = pretty_midi.Instrument(program=0)

    for time, note_name in note_events:
        try:
            note_number = pretty_midi.note_name_to_number(note_name + '4')
        except:
            continue
        note = pretty_midi.Note(velocity=100, pitch=note_number,
                                start=time, end=time + 0.5)
        piano.notes.append(note)

    midi.instruments.append(piano)
    midi.write(output_midi)
    print(f"MIDI dosyası oluşturuldu: {output_midi}")


def crepe_detect_notes(audio_path, confidence_threshold=0.9):
    audio, sr = sf.read(audio_path)
    time, frequency, confidence, _ = crepe.predict(audio, sr, viterbi=True)

    result = []
    for t, f, c in zip(time, frequency, confidence):
        if c > confidence_threshold:
            note, _ = hz_to_note_name(f)
            if note:
                result.append((t, note))
    return result


def full_process(audio_path, use_crepe=False):
    if use_crepe:
        print("CREPE modeli kullanılıyor...")
        note_events = crepe_detect_notes(audio_path)
    else:
        print("Librosa piptrack kullanılıyor...")
        note_events = extract_notes_with_timing(audio_path)

    convert_to_midi(note_events, output_midi="exported_song.mid")
    return note_events


# Örnek Kullanım:
full_process("example.wav", use_crepe=True)


# import numpy as np
# np.complex = complex  # Fix for librosa compatibility with numpy 1.24+

# import librosa
# import pretty_midi
# import soundfile as sf
# import crepe


# def hz_to_note_name(hz):
#     note_names = ['C', 'C#', 'D', 'D#', 'E', 'F',
#                   'F#', 'G', 'G#', 'A', 'A#', 'B']
#     if hz <= 0:
#         return None, None
#     midi = int(round(69 + 12 * np.log2(hz / 440.0)))
#     note = note_names[midi % 12]
#     return note, midi


# def extract_notes_with_timing(audio_path, output_txt="notes_with_time.txt"):
#     y, sr = librosa.load(audio_path)
#     pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
#     times = librosa.frames_to_time(np.arange(pitches.shape[1]), sr=sr)

#     results = []
#     last_midi = None

#     for t in range(pitches.shape[1]):
#         index = magnitudes[:, t].argmax()
#         pitch = pitches[index, t]
#         note, midi = hz_to_note_name(pitch) if pitch > 0 else (None, None)
#         if note and midi != last_midi:
#             results.append((times[t], note))
#             last_midi = midi

#     with open(output_txt, "w") as f:
#         for time, note in results:
#             f.write(f"{time:.2f}s - {note}\n")

#     print(f"{len(results)} zamanlı nota bulundu. '{output_txt}' dosyasına kaydedildi.")
#     return results


# def convert_to_midi(note_events, output_midi='output.mid'):
#     midi = pretty_midi.PrettyMIDI()
#     piano = pretty_midi.Instrument(program=0)

#     for time, note_name in note_events:
#         try:
#             note_number = pretty_midi.note_name_to_number(note_name + '4')
#         except:
#             continue
#         note = pretty_midi.Note(velocity=100, pitch=note_number,
#                                 start=time, end=time + 0.5)
#         piano.notes.append(note)

#     midi.instruments.append(piano)
#     midi.write(output_midi)
#     print(f"MIDI dosyası oluşturuldu: {output_midi}")


# def crepe_detect_notes(audio_path, confidence_threshold=0.9):
#     audio, sr = sf.read(audio_path)
#     time, frequency, confidence, _ = crepe.predict(audio, sr, viterbi=True)

#     result = []
#     for t, f, c in zip(time, frequency, confidence):
#         if c > confidence_threshold:
#             note, _ = hz_to_note_name(f)
#             if note:
#                 result.append((t, note))
#     return result


# def full_process(audio_path, use_crepe=False):
#     if use_crepe:
#         print("CREPE modeli kullanılıyor...")
#         note_events = crepe_detect_notes(audio_path)
#     else:
#         print("Librosa piptrack kullanılıyor...")
#         note_events = extract_notes_with_timing(audio_path)

#     convert_to_midi(note_events, output_midi="exported_song.mid")
#     return note_events


# # Örnek Kullanım:
# # full_process("ornek_ses.wav", use_crepe=True)




# import librosa
# import numpy as np
# import soundfile as sf

# def hz_to_note_name(hz):
#     """Frekansı en yakın nota ismine çevirir (A4 = 440Hz)."""
#     note_names = ['C', 'C#', 'D', 'D#', 'E', 'F',
#                   'F#', 'G', 'G#', 'A', 'A#', 'B']
#     if hz <= 0:
#         return None
#     midi = int(round(69 + 12 * np.log2(hz / 440.0)))
#     return note_names[midi % 12]

# def extract_notes(audio_path, output_txt_path='detected_notes.txt'):
#     print(f"Ses dosyası yükleniyor: {audio_path}")
#     y, sr = librosa.load(audio_path)

#     print("Pitch tahmini yapılıyor...")
#     pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
    
#     notes = []
#     last_note = None

#     for t in range(pitches.shape[1]):
#         index = magnitudes[:, t].argmax()
#         pitch = pitches[index, t]
#         note = hz_to_note_name(pitch)
#         if note and note != last_note:
#             notes.append(note)
#             last_note = note

#     with open(output_txt_path, "w") as f:
#         for note in notes:
#             f.write(note + "\n")

#     print(f"Toplam {len(notes)} nota bulundu. '{output_txt_path}' dosyasına kaydedildi.")

# # Örnek kullanım:
# extract_notes("example.wav")
