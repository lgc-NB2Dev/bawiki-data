import json
from pathlib import Path

from PIL import Image

ROOT_PATH = Path(__file__).parent.parent
WIKI_PATH = ROOT_PATH / "data" / "wiki.json"
PIC_PATH = ROOT_PATH / 'img' / 'global_future.png'
TMP_PATH = ROOT_PATH / 'scripts' / 'tmp'

if not TMP_PATH.exists():
    TMP_PATH.mkdir(parents=True)


def main():
    with open(str(WIKI_PATH), encoding='u8') as f:
        wiki_json = json.loads(f.read())

    future_parts: list = wiki_json['global_future']['parts']

    img: Image.Image = Image.open(str(PIC_PATH))
    for p in future_parts:
        filename = (' _ '.join(p['date']) + '.png').replace('/', '-')
        start, end = p['part']
        part_img = img.crop((0, start, img.width, end))
        part_img.save(str(TMP_PATH / filename))


if __name__ == '__main__':
    main()
