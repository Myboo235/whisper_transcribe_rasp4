FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN apt-get update && apt-get install -y \
    git libportaudio2 libportaudiocpp0 portaudio19-dev \
    pulseaudio alsa-utils ffmpeg \
    python3-dev build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

CMD python3 transcribe.py
