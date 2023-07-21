import json
import re

import aiofiles

from ..base.const import EMOJI_DATA_PATH, EMOJI_JSON_PATH


async def main():
    emo_li = [f"img/emoji/{x.name}" for x in EMOJI_DATA_PATH.iterdir() if x.is_file()]
    emo_li.sort(key=lambda x: re.search("[0-9]+", x).group(0) or 0)
    async with aiofiles.open(str(EMOJI_JSON_PATH), "w", encoding="u8") as f:
        await f.write(json.dumps(emo_li, ensure_ascii=False, indent=2))
    print("emoji: complete")
