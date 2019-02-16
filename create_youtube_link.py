from typing import Iterable
import json
from pathlib import Path
import sys
import os
from abc import ABCMeta, abstractmethod


class YoutubeLinkData(metaclass=ABCMeta):
    def __init__(self, title, url, start_hour, start_min, start_sec):
        self.title = title
        self.url = url
        self.start_hour = start_hour
        self.start_min = start_min
        self.start_sec = start_sec

    @abstractmethod
    def __str__(self):
        pass


class YoutubeLinkData4Wiki(YoutubeLinkData):
    def __str__(self):
        t = self.title
        sh = self.start_hour
        sm = self.start_min
        ss = self.start_sec
        u = self.url
        return f"[[{t}({sh:02}:{sm:02}:{ss:02})>>{u}&t={sh}h{sm}m{ss}s]]"


def save(output_txt_file_path: Path, output: Iterable):
    with open(output_txt_file_path.as_posix(), "w", encoding="utf-8") as output_file:
        output_file.write("created by https://github.com/yasumo/create_youtube_link")
        output_file.write("\n")
        output_file.write("\n")
        output_file.write("\n".join(output))


def create_youtube_link(json_file_path: Path, clazz):
    if not json_file_path.exists():
        raise Exception("ファイルが無いです")
    with open(json_file_path.as_posix(), 'r', encoding="utf-8") as json_file:
        json_data = json.load(json_file)
    for data in json_data["data"]:
        title = data["title"]
        url = data["url"]
        for time in data["time"]:
            start_hour, start_min, start_sec = time
            youtube_link_data = clazz(title, url, start_hour, start_min, start_sec)
            yield str(youtube_link_data)


def main():
    args = sys.argv
    json_file_path_str = args[1]
    if json_file_path_str is None:
        raise Exception("第一引数にjsonファイル指定してください")

    json_file_path = Path(json_file_path_str)

    # wiki用のリンク作成
    youtube_links_for_wiki = create_youtube_link(json_file_path, YoutubeLinkData4Wiki)
    file_stem = json_file_path.stem
    output_txt_for_wiki_file_path = Path(f"{json_file_path.parent}{os.sep}{file_stem}4wiki.txt")
    save(output_txt_for_wiki_file_path, youtube_links_for_wiki)


if __name__ == '__main__':
    main()
