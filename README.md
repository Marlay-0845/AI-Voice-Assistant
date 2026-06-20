# AI Voice Assistant

A local AI voice assistant built with Python.

The assistant supports voice interaction using speech recognition, wake words, local language models, text-to-speech synthesis, and interruption handling. Designed for communication in Russian 

## Features

* Wake word activation ("Томас")
* Voice Activity Detection (WebRTC VAD)
* Speech-to-Text using Whisper
* Text generation with a local LLM via Ollama
* Text-to-Speech responses
* Barge-in support (interrupt assistant while speaking)
* Automatic sleep mode after inactivity
* Voice command system
* Multi-threaded architecture for low latency

## Architecture

Voice Input

↓

WebRTC VAD

↓

Audio Buffer

↓

Whisper STT

↓

Wake Word Detection

↓

Command Handler / LLM

↓

TTS

↓

Voice Output

## Technologies

* Python 3.11+
* WebRTC VAD
* Faster-Whisper
* Ollama
* NumPy
* SoundDevice
* Threading
* Local LLMs (Gemma, Qwen, etc.)

## Current Commands

Examples:

* Open browser
* Open YouTube
* Wake assistant
* Sleep assistant

Additional commands can be easily added through the command registry.

## Project Structure

```text
assistant/
├── core/
│   ├── state_manager.py
│   ├── wake_word.py
│   ├── commands.py
│   └── ...
│
├── audio/
│   ├── voice_buffer.py
│   ├── transcribe.py
│   ├── voice_speaker.py
│   └── ...
│
├── main.py
└── requirements.txt
```

## How It Works

1. Audio is captured from the microphone.
2. WebRTC VAD detects speech activity.
3. Audio chunks are combined into phrases.
4. Whisper transcribes speech into text.
5. Wake word detection checks whether the assistant should respond.
6. Commands are executed directly when detected.
7. Other requests are forwarded to the local LLM.
8. Responses are spoken through TTS.

## Future Improvements

* Streaming speech recognition
* Memory and conversation history
* RAG support
* Smart home integrations
* Browser automation
* Web search support
* Calendar and reminder system

## Demo

The assistant supports:

* Natural conversations
* Wake word activation
* Voice commands
* Local execution without cloud dependency

## License

MIT License
