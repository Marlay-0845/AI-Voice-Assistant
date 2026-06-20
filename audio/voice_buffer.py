import numpy as np
from collections import deque


class VoiceBuffer:
    def __init__(self):
        self.pre_buffer = deque(maxlen=20)
        self.chunks = []
        self.recording = False
        self.silence_chunks = 0
        self.pending_silence = []
        self.max_silence_chunks = 15


    def add_chunk(self, chunk, is_speech):
        if not self.recording:
            self.pre_buffer.append(chunk)

        
        if is_speech and self.recording is False:
            self.chunks.extend(self.pre_buffer)
            self.pre_buffer.clear()
            self.chunks.append(chunk)
            self.recording = True
        elif is_speech and self.recording:
            self.chunks.extend(self.pending_silence)
            self.chunks.append(chunk)
            self.pending_silence.clear()
            self.silence_chunks = 0
        elif is_speech is False and self.recording is True:
            self.pending_silence.append(chunk)
            self.silence_chunks += 1
            

    def get_full_audio(self):
        full_audio = np.concatenate(self.chunks)
        return full_audio


    def clear(self):
        self.chunks.clear()
        self.pre_buffer.clear()
        self.pending_silence.clear()
        self.silence_chunks = 0
        self.recording = False


    def is_phrase_finished(self):
        if self.silence_chunks >= self.max_silence_chunks:
            return True
        else:
            return False