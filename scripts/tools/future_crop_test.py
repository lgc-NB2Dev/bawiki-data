import json

from PIL import Image

from ..base.const import ROOT_PATH, TMP_PATH, WIKI_JSON_PATH

if not TMP_PATH.exists():
    TMP_PATH.mkdir(parents=True)


def crop_and_save(future: dict, prefix: str):
    print(f"cropping {prefix}")

    pic_path: str = future["img"]
    future_parts: list = future["parts"]
    banner_s, banner_e = future["banner"]

    img: Image.Image = Image.open(str(ROOT_PATH / pic_path))

    part_img = img.crop((0, banner_s, img.width, banner_e))
    part_img.save(str(TMP_PATH / f"{prefix} _ banner.png"))

    for p in future_parts:
        date_str = " _ ".join(p["date"]).replace("/", "-")
        filename = f"{prefix} _ {date_str}.png"
        start, end = p["part"]
        part_img = img.crop((0, start, img.width, end))
        part_img.save(str(TMP_PATH / filename))


def main():
    print("cleaning tmp path")
    for i in TMP_PATH.iterdir():
        if i.is_file():
            i.unlink()

    wiki_json = json.loads(WIKI_JSON_PATH.read_text(encoding="u8"))
    crop_and_save(wiki_json["global_future"], "global")
    crop_and_save(wiki_json["chinese_future"], "chinese")


if __name__ == "__main__":
    main()
