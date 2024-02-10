import json
import re

import anyio

from ..base.const import EMOJI_DATA_PATH, EMOJI_JSON_PATH


async def main():
    emo_li = [f"img/emoji/{x.name}" for x in EMOJI_DATA_PATH.iterdir() if x.is_file()]
    emo_li.sort(key=lambda x: r.group(0) if (r := re.search("[0-9]+", x)) else 0)
    await anyio.Path(EMOJI_JSON_PATH).write_text(
        json.dumps(emo_li, ensure_ascii=False, indent=2),
        encoding="u8",
    )
    print("emoji: complete")
