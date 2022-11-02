import json
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent
JSON_PATH = ROOT_PATH / "data" / "emoji.json"
EMOJI_PATH = ROOT_PATH / "img" / "emoji"


def main():
    emo_li = [f'img/emoji/{x.name}' for x in EMOJI_PATH.iterdir() if x.is_file()]
    with open(str(JSON_PATH), 'w', encoding='u8') as f:
        json.dump(emo_li, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
