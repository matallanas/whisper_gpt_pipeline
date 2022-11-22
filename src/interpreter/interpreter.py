from abc import ABC, abstractmethod


class Interpreter(ABC):
    """An interpreter to make audio operations to transcribe or translate the video 
    content.
    """

    @abstractmethod
    def transcribe(self):
        pass

    @abstractmethod
    def translate(self):
        pass
