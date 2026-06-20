import re
from enum import Enum, auto



class AssistantState(Enum):
    SLEEPING = auto()
    ACTIVE = auto()


class StateManager:
    def __init__(self):
        self.state = AssistantState.SLEEPING
        self.last_activity_time = 0


    def wake_up(self):
        self.state = AssistantState.ACTIVE


    def fall_asleep(self):
        self.state = AssistantState.SLEEPING


    # def catch_silence_time(self, silence_time):
    #     if silence_time > self.last_activity_time:
    #         self.last_activity_time


class WakeWordManager():
    def __init__(self):
        self.wake_word = "томас"


    def detect_wake_word(self, text_from_user: str):
        if self.wake_word in text_from_user.lower():
            text_no_wake_word = re.sub(rf'\b{self.wake_word}\b', '', text_from_user).strip()

            if text_no_wake_word:
                return text_no_wake_word
            else:
                return None
        else:
            return False