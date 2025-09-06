## 🎙️ Real-Time Speech Transcription with Vosk

This project provides a real-time speech-to-text demo using [Vosk](https://alphacephei.com/vosk/) with microphone input.
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
docker compose run --rm app python transcribe.py
```

---

## 🐍 Option 2: Run without Docker

### 1. Create a virtual environment (recommended)

```python
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
```

### 2. Install dependencies

```bash
apt-get update && apt-get install -y \
    git libportaudio2 libportaudiocpp0 portaudio19-dev \
    pulseaudio alsa-utils ffmpeg \
    python3-dev build-essential \
    && rm -rf /var/lib/apt/lists/*
```

```python
pip install -r requirements.txt
```

### 3. Run the transcription script

```bash
python transcribe.py
```

---

## 📝 REF

- [VOSK](https://alphacephei.com/vosk/)
- https://github.com/alphacep/vosk-api/blob/master/python/example/test_microphone.py
