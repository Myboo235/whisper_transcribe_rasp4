## 🎙️ Real-Time Speech Transcription with Whisper

This project provides a real-time speech-to-text demo using [OpenAI Whisper](https://github.com/openai/whisper) with microphone input.
You can run it **with Docker** or **without Docker** depending on your setup.

---

## 📦 Requirements

* **Option 1 (Docker)**

  * [Docker](https://docs.docker.com/get-docker/)
  * [Docker Compose](https://docs.docker.com/compose/install/)

* **Option 2 (No Docker)**

  * Python **3.7+**
  * A working C++ build toolchain (needed for PyAudio)
  * `portaudio` development headers (Linux/Mac only)

---

## 🚀 Option 1: Run with Docker

### 1. Build the container

```bash
docker compose build
```

### 2. Start transcription

```bash
docker compose run --rm app python transcribe_demo.py
```

---

## 🐍 Option 2: Run without Docker

### 1. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the transcription script

```bash
python transcribe.py
```

---

## ⚙️ Configuration

All configuration is done inside [`transcribe_demo.py`](./transcribe_demo.py).
Edit the variables at the top of the file to adjust behavior:

```python
MODEL = "base"                # Options: "tiny", "base", "small", "medium", "large"
NON_ENGLISH = False           # True = multilingual model, False = english-only
ENERGY_THRESHOLD = 1000       # Mic sensitivity
RECORD_TIMEOUT = 2            # Seconds between audio processing
PHRASE_TIMEOUT = 3            # Silence gap before new line
DEFAULT_MICROPHONE = "pulse"  # Linux only; set to "list" to show available devices
```

---

## 📝 REF

- [Real Time Whisper Transcription](https://github.com/davabase/whisper_real_time)
