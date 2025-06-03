from basic_pitch.inference import predict
import soundfile as sf


audio, sr = sf.read("ornek_ses.wav") 
model_output, midi_data, note_events = predict(audio, sr)
for note in note_events:
    print(f"Note: {note['note']}, Start Time: {note['start_time']:.2f}s, End Time: {note['end_time']:.2f}s")
