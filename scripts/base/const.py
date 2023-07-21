from pathlib import Path
from typing import TypedDict

SCHALE_URL = "https://lonqie.github.io/SchaleDB/"
GAMEKEE_URL = "https://ba.gamekee.com/"

SCRIPT_PATH = Path(__file__).parent.parent
ROOT_PATH = SCRIPT_PATH.parent
DATA_PATH = ROOT_PATH / "data"
IMG_PATH = ROOT_PATH / "img"
TMP_PATH = SCRIPT_PATH / "tmp"

EMOJI_DATA_PATH = IMG_PATH / "emoji"

ALIAS_JSON_PATH = DATA_PATH / "stu_alias.json"
# ALIAS_BAK_PATH = DATA_PATH / "stu_alias.json.bak"
SUFFIX_ALIAS_JSON_PATH = DATA_PATH / "suffix_alias.json"
WIKI_JSON_PATH = DATA_PATH / "wiki.json"
EMOJI_JSON_PATH = DATA_PATH / "emoji.json"
MANGA_JSON_PATH = DATA_PATH / "manga.json"
GACHA_JSON_PATH = DATA_PATH / "gacha.json"


class Manga(TypedDict):
    cid: int
    title: str
    detail: str
    pics: list[str]
