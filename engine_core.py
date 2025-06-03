from music_analyzer.analyzer import InstrumentRecognizer, NoteTranscriber

file_path = "example_voice.wav"

# Enstrüman tahmini
instr_recognizer = InstrumentRecognizer()
instrument = instr_recognizer.recognize(file_path)
print(f"Tanımlanan enstrüman: {instrument}")

# Nota çıkarımı
transcriber = NoteTranscriber()
transcriber.transcribe_and_print(file_path)


 