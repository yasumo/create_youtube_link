import urllib.request
import bs4
import sys
import time
import os
from pathlib import Path
import random

indent1 = "  "
indent2 = f"{indent1}{indent1}"
indent3 = f"{indent1}{indent1}{indent1}"


def save(output_txt_file_path: Path, output: str):
    with open(output_txt_file_path.as_posix(), "w", encoding="utf-8") as output_file:
        output_file.write(output)


def get_title(url):
    html = urllib.request.urlopen(url)

    soup = bs4.BeautifulSoup(html, "html.parser")

    title_tag = soup.title

    title = title_tag.string

    # 末尾の” - YouTube”を消す
    title = title[0:-10]
    return title


def formatter(title, url):
    return f'{indent2}{{\n{indent3}"title" : "{title}",\n{indent3}"url" : "{url}",\n{indent3}"time" : [\n{indent3}]\n{indent2}}}'


def format_urls(url_list_file_path: Path):
    if not url_list_file_path.exists():
        raise Exception("ファイルがありません")

    with open(url_list_file_path.as_posix(), 'r', encoding="utf-8") as url_list_file:
        lines = url_list_file.readlines()  # 1行毎にファイル終端まで全て読む(改行文字も含まれる)
        for line in lines:
            url = line.strip()
            if len(url) > 0:
                # アクセスしすぎはダメなので待つ
                time.sleep(2 + random.random())
                title = get_title(url)
                print(title)
                yield formatter(title, url)


def main():
    args = sys.argv
    input_file_path_str = args[1]
    if input_file_path_str is None:
        raise Exception("第一引数にjsonファイル指定してください")
    input_file_path = Path(input_file_path_str)

    prefix = f'{{\n{indent1}"data" : [\n'
    suffix = f'\n{indent1}]\n}}'
    template = ",\n".join(format_urls(input_file_path))
    output = f'{prefix}{template}{suffix}'

    output_file_path = Path(f"output{os.sep}{input_file_path.stem}_template.json")
    output_file_path.parent.mkdir(exist_ok=True, parents=True)
    print(output)
    save(output_file_path, output)


if __name__ == '__main__':
    main()
