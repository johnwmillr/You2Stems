"""
tube2stems
John W. Miller
2020
"""

# TODO: Add this: https://github.com/ytdl-org/youtube-dl/issues/23638

import sys
import argparse

from tube2stems import SongToStems


def main(args=None):
    desc = "Download YouTube audio, split the track into instrumental stems."
    parser = argparse.ArgumentParser(
        description=desc,
        prog="youstem",
        allow_abbrev=False)
        
    parser.add_argument(
        "url",
        help="The YouTube URL to download audio from.",
        type=str.lower)

    parser.add_argument(
        "--num-stems",
        "-n",
        help="The number of stems to split the audio into.",
        type=int,
        choices=[2, 4, 5],
        default=2)

    parser.add_argument(
        "--codec",
        "-c",
        help="Specify the preferred audio codec.",
        type=str.lower,
        choices=["mp3", "wav"],
        default="mp3")

    parser.add_argument(
        "--file",
        "-f",
        help="Specify the save name for the audio file.",
        type=str,
        default=None)

    parser.add_argument(
        "--verbose",
        "-v",
        help="Toggles verbosity.",
        type=bool,
        default=True,
        choices=[True, False])
    args = parser.parse_args()
    print(args)

    # Download audio, split into stems
    song2stems = SongToStems(
        num_stems=args.num_stems,
        verbose=args.verbose)

    song2stems.download_and_split(
        url=args.url,
        filename=args.file)


if __name__ == "__main__":
    main()