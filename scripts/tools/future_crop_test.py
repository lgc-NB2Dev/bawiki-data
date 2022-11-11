import json

from PIL import Image

from ..base.const import ROOT_PATH, TMP_PATH, WIKI_JSON_PATH

if not TMP_PATH.exists():
    TMP_PATH.mkdir(parents=True)


def main():
    for i in TMP_PATH.iterdir():
        if i.is_file():
            i.unlink()

    with open(str(WIKI_JSON_PATH), encoding="u8") as f:
        wiki_json = json.loads(f.read())

    future: dict = wiki_json["global_future"]
    pic_path: str = future["img"]
    future_parts: list = future["parts"]
    banner_s, banner_e = future["banner"]

    img: Image.Image = Image.open(str(ROOT_PATH / pic_path))

    part_img = img.crop((0, banner_s, img.width, banner_e))
    part_img.save(str(TMP_PATH / "banner.png"))

    for p in future_parts:
        filename = (" _ ".join(p["date"]) + ".png").replace("/", "-")
        start, end = p["part"]
        part_img = img.crop((0, start, img.width, end))
        part_img.save(str(TMP_PATH / filename))


if __name__ == "__main__":
    main()
