import json

import aiofiles

from ..base.const import GACHA_JSON_PATH
from ..base.utils import schale_get_stu_data

BASE_DICT = {
    "3": {"chance": 2.5, "char": []},
    "2": {"chance": 18.5, "char": []},
    "1": {"chance": 79.0, "char": []},
}


async def main():
    stu_li = await schale_get_stu_data(raw=True)

    star3 = []
    star2 = []
    star1 = []

    for i in stu_li:
        s_id = i["Id"]
        s_name = i["Name"]
        star_grade = i["StarGrade"]
        limited = i["IsLimited"]
        if not limited:
            match star_grade:
                case 3:
                    star3.append(s_id)
                case 2:
                    star2.append(s_id)
                case 1:
                    star1.append(s_id)

        print(f'gacha: {star_grade}星{"[限定]" if limited else " 常驻 "}：({s_id}) {s_name}')

    star3.sort()
    star2.sort()
    star1.sort()

    BASE_DICT["3"]["char"] = star3
    BASE_DICT["2"]["char"] = star2
    BASE_DICT["1"]["char"] = star1

    async with aiofiles.open(str(GACHA_JSON_PATH), encoding="u8") as f:
        j = json.loads(await f.read())
    j["base"] = BASE_DICT

    dump_j = json.dumps(j, indent=2, ensure_ascii=False)

    async with aiofiles.open(str(GACHA_JSON_PATH), "w", encoding="u8") as f:
        await f.write(dump_j)

    print("gacha: complete")
