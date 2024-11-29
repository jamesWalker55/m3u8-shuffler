import json
import random
from pathlib import Path


def write_json(path, obj):
    with open(path, "w", encoding="utf8") as f:
        json.dump(obj, f)


def read_m3u8(path):
    # foobar's m3u8 uses UTF8 BOM, in Python it's 'utf-8-sig'
    with open(path, "r", encoding="utf-8-sig") as f:
        lines = f.readlines()

    lines = [x.rstrip("\r\n") for x in lines]

    # some may start with "#EXTM3U"
    # those are not supported
    assert lines[0] == "#", f"unsupported m3u8 extension: {lines[0]!r}"

    lines.pop(0)

    return lines


def write_m3u8(path, playlist: list[str]):
    with open(path, "w", encoding="utf8") as f:
        f.write("#\n")
        for x in playlist:
            f.write(x)
            f.write("\n")


def main():
    path = Path(R"D:\Soundtracks\Downloaded Playlist 2024-11-29.m3u8")
    playlist = read_m3u8(path)

    # assign a range-limited random float to each playlist item
    def generate_random_key(i: int):
        # random number, range is about -2.5..+2.5
        # https://academo.org/demos/gaussian-distribution/
        rand = random.gauss(0, 1.5)
        return i + rand * 500

    # sort the playlist randomly, but not completely randomly
    playlist = [(generate_random_key(i), i, x) for i, x in enumerate(playlist)]
    playlist.sort()

    write_m3u8(path.with_stem(path.stem + " Shuffled"), [x for k, i, x in playlist])
    # for debugging: show original index of item
    write_m3u8(
        path.with_stem(path.stem + " Shuffled IDX"),
        [f"{i} {x}" for k, i, x in playlist],
    )
