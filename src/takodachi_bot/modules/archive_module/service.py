import subprocess

if __name__ == "__main__":
    import os
    import sys

    sys.path.append(
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
    )
from takodachi_bot.configs import (
    ARCHIVE_YOUTUBE_STREAM_BAT_PATCH as ARCHIVE_YOUTUBE_STREAM,
    ARCHIVE_VIDEO_BAT_PATCH as ARCHIVE_VIDEO,
    ARCHIVE_AND_PLAY_TWITCH_STREAM_BAT_PATCH as ARCHIVE_PLAY_TWITCH_STREAM,
    ARCHIVE_TWITCH_STREAM_BAT_PATCH as ARCHIVE_TWITCH_STREAM,
)


def start_archive(path, url):
    cmd = ["start", "", path]
    if isinstance(url, str):
        cmd.append(url)
    subprocess.Popen(cmd, shell=True)


def archive_youtube_stream(url):
    start_archive(ARCHIVE_YOUTUBE_STREAM, url)


def archive_video(url):
    start_archive(ARCHIVE_VIDEO, url)


def archive_and_play_twitch_stream(url):
    start_archive(ARCHIVE_PLAY_TWITCH_STREAM, url)


def archive_twitch_stream(url):
    start_archive(ARCHIVE_TWITCH_STREAM, url)
