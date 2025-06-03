import librosa
import numpy as np

def hz_to_note_name(hz):
    """Frekansı en yakın nota ismine çevir (örn. 440 Hz -> A4)"""
    note_names = ['C', 'C#', 'D', 'D#', 'E', 'F',
                  'F#', 'G', 'G#', 'A', 'A#', 'B']
    if hz == 0:
        return None
    midi_num = int(np.round(69 + 12 * np.log2(hz / 440.0)))
    note_index = midi_num % 12
    return note_names[note_index] + str(midi_num // 12 - 1)

def extract_notes(audio_path, output_txt_path='detected_notes.txt'):
    y, sr = librosa.load(audio_path)
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    times = librosa.times_like(onset_env, sr=sr)
    tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)

    pitches, magnitudes = librosa.piptrack(y=y, sr=sr)

    note_names = []

    for t in range(pitches.shape[1]):
        index = magnitudes[:, t].argmax()
        freq = pitches[index, t]
        note = hz_to_note_name(freq)
        if note:
            note_names.append(note)

    # Tekrarları filtrele: Aynı notaların ardışık tekrarlarını kaldır
    filtered_notes = []
    last = None
    for n in note_names:
        if n != last:
            filtered_notes.append(n)
            last = n

    with open(output_txt_path, 'w') as f:
        for note in filtered_notes:
            f.write(note + '\n')

    print(f"{len(filtered_notes)} nota tanındı ve '{output_txt_path}' dosyasına yazıldı.")

# Örnek kullanım:
extract_notes("example.wav")
