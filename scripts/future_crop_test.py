import json
from pathlib import Path

from PIL import Image

ROOT_PATH = Path(__file__).parent.parent
WIKI_PATH = ROOT_PATH / "data" / "wiki.json"
TMP_PATH = ROOT_PATH / "scripts" / "tmp"

if not TMP_PATH.exists():
    TMP_PATH.mkdir(parents=True)


def main():
    for i in TMP_PATH.iterdir():
        if i.is_file():
            i.unlink()

    with open(str(WIKI_PATH), encoding="u8") as f:
        wiki_json = json.loads(f.read())

    future: dict = wiki_json["global_future"]
    pic_path: str = future["img"]
    future_parts: list = future["parts"]

    img: Image.Image = Image.open(str(ROOT_PATH / pic_path))
    for p in future_parts:
        filename = (" _ ".join(p["date"]) + ".png").replace("/", "-")
        start, end = p["part"]
        part_img = img.crop((0, start, img.width, end))
        part_img.save(str(TMP_PATH / filename))


if __name__ == "__main__":
    main()
