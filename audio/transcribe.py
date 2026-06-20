import threading
from faster_whisper import WhisperModel

from AI_Assistant.config import voice_path 



class VoiceTranscribe():
    def __init__(self):
        self.model_size = "small"
        self.model = WhisperModel(self.model_size, device="cpu", compute_type="int8")

    def transcribe(self, full_audio):
        full_text = ""
        segments, info = self.model.transcribe(full_audio, beam_size=1, condition_on_previous_text=False, language="ru")

        for segment in segments:
            print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
            full_text += segment.text

        return full_text
    

        