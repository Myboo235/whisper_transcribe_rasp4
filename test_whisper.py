import whisper

# load the model (tiny is fastest, base/small/medium/large are more accurate)
model = whisper.load_model("tiny")

# transcribe an audio file
result = model.transcribe("harvard.wav")

print(result["text"])
