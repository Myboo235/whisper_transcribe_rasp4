#!/usr/bin/env python3
import sys
import json
import queue
import difflib
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import RPi.GPIO as GPIO

# ========================
# Config
# ========================
config = {
    "device": None,
    "samplerate": None,
    "model": "en-us",
    "filename": None,
    "blocksize": 8000,
}

q = queue.Queue()

# ========================
# GPIO setup
# ========================
led_pins = {
    "red": 17,    # GPIO17 (chân vật lý 11)
    "blue": 27,   # GPIO27 (chân vật lý 13)
    "green": 22   # GPIO22 (chân vật lý 15)
}

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

for pin in led_pins.values():
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

# ========================
# Audio callback
# ========================
def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

# ========================
# Helper: so khớp alias + fuzzy
# ========================
def is_match(word, text):
    words = text.split()
    # check alias trực tiếp
    if word in words:
        return True
    # fuzzy match (từ gần giống)
    close = difflib.get_close_matches(word, words, cutoff=0.7)
    return bool(close)

# ========================
# Command handler
# ========================
def handle_command(text: str):
    text = text.lower()

    turn_on_cmds = ["turn on"]
    turn_off_cmds = ["turn off", "turn up"]  

    color_map = {
        "red": ["red"],
        "blue": ["blue", "below"],           
        "green": ["green"]
    }

    print(f"\nDEBUG (final): [{text}]")

    for color, aliases in color_map.items():
        if any(cmd in text for cmd in turn_on_cmds) and any(is_match(alias, text) for alias in aliases):
            GPIO.output(led_pins[color], GPIO.HIGH)
            print(f"👉 Bật đèn màu {color}")
            return
        elif any(cmd in text for cmd in turn_off_cmds) and any(is_match(alias, text) for alias in aliases):
            GPIO.output(led_pins[color], GPIO.LOW)
            print(f"👉 Tắt đèn màu {color}")
            return

# ========================
# Main loop
# ========================
try:
    if config["samplerate"] is None:
        device_info = sd.query_devices(config["device"], "input")
        config["samplerate"] = int(device_info["default_samplerate"])

    model = Model(lang=config["model"])
    rec = KaldiRecognizer(model, config["samplerate"])

    dump_fn = open(config["filename"], "wb") if config["filename"] else None

    print("#" * 80)
    print("Nói: turn on red / turn off blue / turn on green ...")
    print("Press Ctrl+C to stop")
    print("#" * 80)

    last_partial = ""

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
                    handle_command(new_text)   # xử lý khi có kết quả cuối
            else:
                partial = json.loads(rec.PartialResult())
                if partial.get("partial"):
                    new_text = partial["partial"]
                    if new_text != last_partial:
                        sys.stdout.write("\rNhận dạng: " + new_text[:100] + " ...")
                        sys.stdout.flush()
                        last_partial = new_text

            if dump_fn is not None:
                dump_fn.write(data)

except KeyboardInterrupt:
    print("\nDone")
    GPIO.cleanup()  # tắt hết đèn khi thoát
    sys.exit(0)
except Exception as e:
    GPIO.cleanup()
    sys.exit(type(e).__name__ + ": " + str(e))
