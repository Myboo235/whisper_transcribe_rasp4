#!/usr/bin/env python3
import os
import sys
import json
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer

# ========================
# Config
# ========================
config = {
    "device": None,          # input device id or substring, None = default
    "samplerate": None,      # None = use default device rate
    "model": "vn",           # language model, e.g. "en-us", "fr", "vn"
    "filename": None,        # optional file to save raw audio
    "blocksize": 8000,       # audio block size
}

q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

try:
    # get default samplerate if not specified
    if config["samplerate"] is None:
        device_info = sd.query_devices(config["device"], "input")
        config["samplerate"] = int(device_info["default_samplerate"])

    # load model
    model = Model(lang=config["model"])
    rec = KaldiRecognizer(model, config["samplerate"])

    dump_fn = open(config["filename"], "wb") if config["filename"] else None

    print("#" * 80)
    print("Press Ctrl+C to stop the recording")
    print("#" * 80)

    last_output = "[waiting for speech]"

    with sd.RawInputStream(
        samplerate=config["samplerate"],
        blocksize=config["blocksize"],
        device=config["device"],
        dtype="int16",
        channels=1,
        callback=callback,
    ):
        while True:
            data = q.get()
            new_text = None

            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                if result.get("text"):
                    new_text = result["text"]
            else:
                partial = json.loads(rec.PartialResult())
                if partial.get("partial"):
                    new_text = partial["partial"]

            # update only if new text is non-empty
            if new_text:
                os.system("cls" if os.name == "nt" else "clear")
                last_output = new_text

            # print only one line, keep last if no update
            sys.stdout.write("\r" + last_output[:100] + " ...")
            sys.stdout.flush()

            if dump_fn is not None:
                dump_fn.write(data)

except KeyboardInterrupt:
    print("\nDone")
    sys.exit(0)
except Exception as e:
    sys.exit(type(e).__name__ + ": " + str(e))
