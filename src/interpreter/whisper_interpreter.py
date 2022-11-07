import glob
from typing import Any, Optional
import whisper, os
from interpreter import Interpreter
from utils import SEGMENTS_INFO, AUDIO_FILES, json_dump

class WhisperInterpreter(Interpreter):
  
  def __init__(self, model_size: str) -> None:
    self.model = whisper.load_model(model_size)
  
  def transcribe(self, file_path: str, **kwargs: Optional[Any]) -> dict:
    return self._execute_task("transcribe", file_path, **kwargs)

  def translate(self, file_path: str, **kwargs: Optional[Any]) -> dict:
    return self._execute_task("translate", file_path, **kwargs)

  def _execute_task(self, mode: str, file_path: str, **kwargs: Optional[Any]) -> dict:
    options = dict(task=mode)
    options.update(kwargs)

    if os.path.isdir(file_path):
      result = []
      files = [x for x in glob.glob(os.path.join(file_path,"*")) if os.path.splitext(x)[1] in AUDIO_FILES]
      for file in files:
        file_processed = dict(filename=file)
        file_processed.update(self._file_extraction(file, **options))
        result.append(file_processed)
    else:
      result = self._file_extraction(file_path, **options)

    return result

  def _formatter_result(self, input: dict) -> dict:
    output = dict()
    output["text"] = input["text"]
    output["segments"] = [{key: segment[key] for key in SEGMENTS_INFO} for segment in input["segments"]]
    return output

  def _file_extraction(self, file_path: str, **kwargs: Optional[Any]) -> dict:
    write = kwargs.pop("write",False)
    result = self._formatter_result(
            self.model.transcribe(file_path, **kwargs)
          )
    if write:
      json_dump(result, f"{file_path.split('.')[0]}.json")
    
    return result