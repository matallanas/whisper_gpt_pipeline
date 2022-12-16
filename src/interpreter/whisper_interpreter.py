import glob
from typing import Any, Optional
import whisper, os
from interpreter import Interpreter
from utils import AUDIO_FEATURE, SEGMENTS_INFO, AUDIO_FILES, json_dump


class WhisperInterpreter(Interpreter):
  """Create a whisper interpreter to transcribe or traslate your audio."""

  def __init__(self, model_size: str):
    """Load whisper model to use

    Args:
      model_size: str, Size of the model to use
    """
    self.model = whisper.load_model(model_size)

  def transcribe(self, file_path: str, **kwargs: Optional[Any]):
    """Transcribe audio file with options specify.

    Args:
      file_path: str, Path of the audio file to transcribe.
      **kwargs: Optional[Any], Options to transcribe.

    Returns:
      dict | list: A dictionary or list of dictionaries with the results.
    """
    return self._execute_task("transcribe", file_path, **kwargs)

  def translate(self, file_path: str, **kwargs: Optional[Any]):
    """Translate audio file with options specify.

    Args:
      file_path: str
      File or path of audio file/s to translate.
    **kwargs: Optional[Any]
      Options to translate.

    Returns:
      dict | list: A dictionary or list of dictionaries with the results.
    """
    return self._execute_task("translate", file_path, **kwargs)

  def _execute_task(self, mode: str, file_path: str, **kwargs: Optional[Any]):
    """Use whisper model to transcribe or traslate an audio file or all files from
    a folder.

    Args:
      file_path: str, File or path of audio file/s to transcribe or translate.
      **kwargs: Optional[Any], Options to translate.

    Returns:
      dict | list: A dictionary or list of dictionaries with the results.
    """
    options = dict(task=mode)
    options.update(kwargs)

    if os.path.isdir(file_path):
      result = []
      files = [
        x for x in glob.glob(os.path.join(file_path, "*"))
          if os.path.splitext(x)[1] in AUDIO_FILES
      ]
      for file in files:
        file_processed = dict(filename=file)
        file_processed.update(self._file_extraction(file, **options))
        result.append(file_processed)
    else:
        result = self._file_extraction(file_path, **options)

    return result

  def _formatter_result(self, input: dict):
    """Create a dictionary with the results.

    Args:
      input: str, Whisper input results.

    Returns:
      dict | list: A dictionary or list of dictionaries with the results.
    """
    output = dict()
    output["text"] = input["text"]
    output["segments"] = [
      {key: segment[key] for key in SEGMENTS_INFO} for segment in input["segments"]
    ]
    return output

  def _file_extraction(self, file_path: str, **kwargs: Optional[Any]):
    """
    Transcribe or traslate audio file.
    
    Args:
      file_path: str, File or path of audio file/s to transcribe or translate.
      **kwargs: Optional[Any], Options to translate.

    Returns:
      dict | list: A dictionary or list of dictionaries with the results.
    """
    write = kwargs.pop("write", False)
    result = self._formatter_result(self.model.transcribe(file_path, **kwargs))
    result[AUDIO_FEATURE] = file_path
    if write:
      json_dump(result, f"{file_path.split('.')[0]}.json")

    return result
