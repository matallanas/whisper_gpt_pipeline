import click, re
import pandas as pd
from dataset import TranscriptDataset
from downloader import WhisperPP, YoutubeDownloader
from interpreter import WhisperInterpreter


_global_options = [
    click.option(
        "--model-size",
        "-m",
        default="base",
        help="Size of the model to use to transcribe",
    ),
    click.option("--language", "-l", help="Language of the video"),
    click.option(
        "--transcribe",
        "mode",
        flag_value="transcribe",
        default=True,
        help="Transcribe audio files to its language.",
    ),
    click.option(
        "--translate",
        "mode",
        flag_value="translate",
        help="Traslate audio files to its language.",
    ),
    click.option(
        "--write",
        "-w",
        is_flag=True,
        show_default=True,
        default=False,
        help="Write result in a json.",
    ),
]


def global_options(func):
    for option in reversed(_global_options):
        func = option(func)
    return func


@click.group()
def cli():
    pass


@cli.command()
@click.argument("url")
@click.option(
    "--download-path", "-d", default="tmp/", help="Path to download and store files"
)
@global_options
def download_url(
    url: str, download_path: str, model_size: str, language: str, mode: str, write: bool
):
    """
    Download a Youtube video and convert to mp3
    """
    data = []
    whisper_options = dict(
        model_size=model_size, mode=mode, language=language, write=write
    )
    whisperPP = WhisperPP(data, **whisper_options)
    downloader = YoutubeDownloader(download_path)
    downloader.download(url, whisperPP)
    return data


@cli.command()
@click.argument("file_path", type=click.Path(exists=True))
@global_options
def interpret(file_path, model_size, language, mode, write):
    """
    Transcribe or a tranlate a local file
    """
    interpreter = WhisperInterpreter(model_size)
    options = dict(language=language, write=write)
    process = getattr(interpreter, mode)
    result = process(file_path, **options)
    print(result)


@cli.command()
@click.option(
    "--name",
    "-n",
    default="",
    help="Name of the Hugging Face Dataset, if empyt a local dataset is created.",
)
@click.option(
    "--input", "-i", help="Location of the data, could be youtube url or a local path."
)
@click.option(
    "--download-path", "-d", default="tmp/", help="Path to download and store files"
)
@click.option(
    "--upload",
    "-u",
    is_flag=True,
    show_default=True,
    default=False,
    help="Upload dataset to the hub",
)
@global_options
def dataset(name, input, download_path, upload, model_size, language, mode, write):
    """
    Add the transcript of Youtube videos to a Hugging Face dataset
    """

    ds = TranscriptDataset(name)
    overwrite = False
    params = dict(model_size=model_size, language=language, write=write, number_videos=500)
    ds.generate_dataset(input, download_path, overwrite, params)
    if upload or (overwrite and name != ""):
       ds.upload()


if __name__ == "__main__":
    cli()
