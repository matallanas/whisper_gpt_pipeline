from typing import List

from youtube_transcriber.video import YoutubeVideo
from youtube_transcriber.transforming.transform import Transform
from youtube_transcriber.utils import accepts_types

class BatchTransformer:
    
    """Class that applies multiple transforms to YouTube video object."""
    
    def __init__(self, transforms: List[Transform]) -> None:
        self._transforms = transforms
        
    @property
    def transforms(self) -> List[Transform]:
        return self._transforms
    
    @transforms.setter
    def transforms(self, transforms: List[Transform]) -> None:
        self._transforms = transforms
        
    @accepts_types(list)
    def apply(self, videos: List[YoutubeVideo]) -> List[YoutubeVideo]:
        for transform in self._transforms:
            videos = list(map(transform.apply, videos))
        return videos