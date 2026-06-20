import time
import logging
import threading
import webrtcvad
import sounddevice as sd
import numpy as np
from queue import Queue

from AI_Assistant.audio.voice_buffer import VoiceBuffer
from AI_Assistant.audio.transcribe import VoiceTranscribe
from AI_Assistant.audio.voice_speaker import VoiceSpeaker
from AI_Assistant.llm.chat import answer_to_text
from AI_Assistant.core.state_manager import StateManager, WakeWordManager, AssistantState
from AI_Assistant.core.commands import commands_list_func



logger = logging.getLogger("AI_Assistant")

raw_audio_queue = Queue()
full_audio_queue = Queue()
text_queue = Queue()
answer_queue = Queue()
say_answer_queue = Queue()

state = StateManager()
wake_word_manager = WakeWordManager()

buffer = VoiceBuffer()
transcriber = VoiceTranscribe()
speaker = VoiceSpeaker()
vad = webrtcvad.Vad(2)  # 0–3 (агрессивность)

SAMPLE_RATE = 16000
FRAME_DURATION = 30  # ms
FRAME_SIZE = int(SAMPLE_RATE * FRAME_DURATION / 1000)



def timer_worker():
    while True:
        if state.state == AssistantState.ACTIVE:
            if speaker.is_speaking():
                state.last_activity_time = time.monotonic()

            print("TIME:", time.monotonic() - state.last_activity_time)
            if (time.monotonic() - state.last_activity_time) > 20:
                state.fall_asleep()

            time.sleep(0.5)
                


def say_answer_worker():
    while True:
        try:
            text_answer = answer_queue.get()

            print("SAY")

            speaker.say(text_from_user=text_answer)
        except Exception as e:
            print(e)
            logger.warning("SPEAKER crashed")
            print("SPEAKER crashed")


def llm_worker():
    while True:
        try:
            text_from_user = text_queue.get()

            print("LLM")

            text_answer = answer_to_text(text_from_user)

            answer_queue.put(text_answer)
        except Exception:
            logger.warning("LLM crashed")
            print("LLM crashed")


def stt_worker():
    while True:
        try:
            full_audio = full_audio_queue.get()
            
            if (len(full_audio) / SAMPLE_RATE) < 1:
                continue

            from_audio_to_text = transcriber.transcribe(full_audio=full_audio)

            text = from_audio_to_text.strip()

            print(repr(from_audio_to_text))

            if not text:
                continue

            if state.state == AssistantState.SLEEPING:
                is_wake_word = wake_word_manager.detect_wake_word(text_from_user=text)

                state.last_activity_time = time.monotonic()

                if commands_list_func(text_from_user=is_wake_word):
                    continue

                if is_wake_word is None:
                    answer_queue.put("Слушаю")
                    state.wake_up()
                    continue
                elif is_wake_word:
                    print("W")
                    text_queue.put(is_wake_word)
                    state.wake_up()
                    continue
                else:
                    print("L")
                    continue
            
            state.last_activity_time = time.monotonic()

            if speaker.is_speaking():
                speaker.stop()

            text_queue.put(from_audio_to_text)
        except Exception:
            logger.warning("STT crashed")
            print("STT crashed")


def vad_worker():
    while True:
        audio_float = raw_audio_queue.get()

        is_speech_or_not = is_speech(audio_float=audio_float)

        buffer.add_chunk(chunk=audio_float, is_speech=is_speech_or_not)

        if buffer.is_phrase_finished():
            full_audio_queue.put(buffer.get_full_audio())
            buffer.clear()


def is_speech(audio_float):
    audio_int16 = (audio_float * 32768).astype(np.int16)

    return vad.is_speech(audio_int16.tobytes(), SAMPLE_RATE)


def callback(indata, frames, time, status):
    audio_float = indata[:, 0].copy()

    raw_audio_queue.put(audio_float)


with sd.InputStream(
    samplerate=SAMPLE_RATE,
    channels=1,
    blocksize=FRAME_SIZE,
    dtype='float32',
    callback=callback
):
    tasks = [vad_worker, stt_worker, llm_worker, say_answer_worker, timer_worker]

    for func in tasks:
        t = threading.Thread(target=func)
        t.start()

    print("Listening...")
    while True:
        time.sleep(1)