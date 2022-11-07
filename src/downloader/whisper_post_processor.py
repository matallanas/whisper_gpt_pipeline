from interpreter import WhisperInterpreter
from utils import VIDEO_INFO
from yt_dlp.postprocessor import PostProcessor

class WhisperPP(PostProcessor):
  def __init__(self,data,**whisper_options):
    super().__init__()
    self._options = whisper_options
    interpreter = WhisperInterpreter(self._options.pop("model_size"))
    self.data = data
    self._process = getattr(interpreter, self._options.pop("mode"))
  
  def run(self, info):
    self.to_screen(f"Processing Video {info['id']}")
    result = {key: info[key] for key in VIDEO_INFO}
    result.update(self._process(info["filepath"], **self._options))
    self.to_screen(f"Processed Video {info['id']} and appended results.")
    self.data.append(result)
    return [], info