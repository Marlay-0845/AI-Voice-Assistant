import asyncio
import edge_tts
import pygame
import time

from AI_Assistant.config import VOICE, OUTPUT_FILE



class VoiceSpeaker():
    def __init__(self):
        pygame.mixer.init()

    def say(self, text_from_user):
        self.stop()
        
        asyncio.run(self.generate_audio(text_from_user=text_from_user))


        pygame.mixer.music.load(OUTPUT_FILE)
        pygame.mixer.music.play()


    def stop(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()


    def is_speaking(self):
        return pygame.mixer.music.get_busy()
    

    async def generate_audio(self, text_from_user):
        communicate = edge_tts.Communicate(text_from_user, VOICE)
        await communicate.save(OUTPUT_FILE)