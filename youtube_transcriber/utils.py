from typing import Dict, List

from youtube_transcriber.video import YoutubeVideo
from youtube_transcriber.errors import DifferentNumberOfArgumentsError

def accepts_types(*expected_types):
    """Decorator that checks that the arguments of a method are valid.
    :raise TypeError: If type of argument isn't valid
    :raise DifferentNumberOfArgumentsError: If number of arguments passed to the
        decorator and to the method (minus self) aren't the same
    """
    def check_types(func):
        def wrapper(*args, **kwargs):
            args_without_self = args[1:]
            _raise_error_if_number_of_passed_and_expected_arguments_dont_match(args_without_self, expected_types)
            _raise_type_error_if_passed_and_expected_types_dont_match(args_without_self, expected_types)
            return func(*args, **kwargs)
        return wrapper
    return check_types

def _raise_error_if_number_of_passed_and_expected_arguments_dont_match(passed_args, expected_types):
    if len(passed_args) != len(expected_types):
        msg = "Number of arguments passed in decorator " \
              f"{len(expected_types)} doesn't match with number of " \
              f"arguments in method, i.e., {len(passed_args)}"
        raise DifferentNumberOfArgumentsError(msg)
    
def _raise_type_error_if_passed_and_expected_types_dont_match(passed_args, expected_types):
    for (arg, expected_type) in zip(passed_args, expected_types):
        if not isinstance(arg, expected_type):
            raise TypeError(f"Argument '{arg}' is of type {type(arg)}. "
                            f"'{expected_type}' expected instead")

def create_videos(video_parameters: List[Dict]) -> List[YoutubeVideo]:
    """Factory function that creates a list of YoutubeVideos from a list of
    dictionaries representing video parameters
    """
    youtube_videos = []
    for params in video_parameters:
        youtube_video = YoutubeVideo(channel_name=params["channel_name"],
                                     url=params["url"])
        youtube_videos.append(youtube_video)
    return youtube_videos

def nest_list(list: list, nested_list_length: int) -> List[List]:
    new_list = []
    nested_list = []
    for item in list:
        nested_list.append(item)
        if len(nested_list) == nested_list_length:
            new_list.append(nested_list)
            nested_list = []
    if len(nested_list) != 0:
        new_list.append(nested_list)
    return new_list