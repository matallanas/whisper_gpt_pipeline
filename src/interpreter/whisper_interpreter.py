import whisper
from interpreter import Interpreter

class WhisperInterpreter(Interpreter):
  
  def __init__(self, model_size) -> None:
    self.model = whisper.load_model(model_size)
  
  def transcribe(self, file_path, **kwargs) -> dict:
    options = dict(task="transcribe")
    options.update(kwargs)
    result = self.model.transcribe(file_path, **options)
    #with open("imagine_dragons.json","w") as file:
    #  json.dump(result, file)
    return result

  def translate(self, file_path, **kwargs):
    options = dict(task="translate")
    options.update(kwargs)
    result = self.model.transcribe(file_path, **options)
    return result
