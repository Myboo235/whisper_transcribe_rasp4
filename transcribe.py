#! python3.7
import os
import numpy as np
import speech_recognition as sr
import whisper
import torch

from datetime import datetime, timedelta
from queue import Queue
from time import sleep
from sys import platform

# =========================
# Configuration Variables
# =========================
MODEL = "base"                # Options: "tiny", "base", "small", "medium", "large"
NON_ENGLISH = False           # True = multilingual model, False = english-only
ENERGY_THRESHOLD = 1000       # Mic sensitivity
RECORD_TIMEOUT = 2            # Seconds between audio processing
PHRASE_TIMEOUT = 3            # Silence gap before new line
DEFAULT_MICROPHONE = "pulse"  # Linux only. Use "list" to see devices
# =========================

def main():
    phrase_time = None
    data_queue = Queue()
    phrase_bytes = bytes()

    recorder = sr.Recognizer()
    recorder.energy_threshold = ENERGY_THRESHOLD
    recorder.dynamic_energy_threshold = False

    # Microphone setup
    if 'linux' in platform:
        mic_name = DEFAULT_MICROPHONE
        if not mic_name or mic_name == 'list':
            print("Available microphone devices are: ")
            for index, name in enumerate(sr.Microphone.list_microphone_names()):
                print(f"Microphone with name \"{name}\" found")
            return
        else:
            for index, name in enumerate(sr.Microphone.list_microphone_names()):
                if mic_name in name:
                    source = sr.Microphone(sample_rate=16000, device_index=index)
                    break
    else:
        source = sr.Microphone(sample_rate=16000)

    # Load Whisper model
    model_name = MODEL
    if MODEL != "large" and not NON_ENGLISH:
        model_name = model_name + ".en"
    audio_model = whisper.load_model(model_name)

    transcription = ['']

    with source:
        recorder.adjust_for_ambient_noise(source)

    def record_callback(_, audio: sr.AudioData) -> None:
        data = audio.get_raw_data()
        data_queue.put(data)

    recorder.listen_in_background(source, record_callback, phrase_time_limit=RECORD_TIMEOUT)
    print(f"Model '{model_name}' loaded.\n")

    while True:
        try:
            now = datetime.utcnow()
            if not data_queue.empty():
                phrase_complete = False
                if phrase_time and now - phrase_time > timedelta(seconds=PHRASE_TIMEOUT):
                    phrase_bytes = bytes()
                    phrase_complete = True

                phrase_time = now
                audio_data = b''.join(data_queue.queue)
                data_queue.queue.clear()
                phrase_bytes += audio_data

                audio_np = np.frombuffer(phrase_bytes, dtype=np.int16).astype(np.float32) / 32768.0
                result = audio_model.transcribe(audio_np, fp16=torch.cuda.is_available())
                text = result['text'].strip()

                if phrase_complete:
                    transcription.append(text)
                else:
                    transcription[-1] = text

                os.system('cls' if os.name == 'nt' else 'clear')
                for line in transcription:
                    print(line)
                print('', end='', flush=True)
            else:
                sleep(0.25)
        except KeyboardInterrupt:
            break

    print("\n\nTranscription:")
    for line in transcription:
        print(line)


if __name__ == "__main__":
    main()
