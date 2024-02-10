import json
import time
from typing import List, cast

import aiofiles

from ..base.const import GACHA_JSON_PATH
from ..base.utils import schale_get, schale_get_stu_data

BASE_DICT = {
    "3": {"chance": 2.5, "char": []},
    "2": {"chance": 18.5, "char": []},
    "1": {"chance": 79.0, "char": []},
}


async def main():
    stu_li = cast(dict, await schale_get_stu_data(raw=True))
    stu_dict = {x["Id"]: x for x in stu_li}

    # region base
    star3 = []
    star2 = []
    star1 = []

    for i in stu_li:
        s_id = i["Id"]
        s_name = i["Name"]
        star_grade = i["StarGrade"]
        limited = i["IsLimited"]
        if not limited:
            if star_grade == 3:
                star3.append(s_id)
            elif star_grade == 2:
                star2.append(s_id)
            elif star_grade == 1:
                star1.append(s_id)

        print(
            f'gacha: {star_grade}星{"[限定]" if limited else " 常驻 "}：({s_id}) {s_name}',
        )

    star3.sort()
    star2.sort()
    star1.sort()

    BASE_DICT["3"]["char"] = star3
    BASE_DICT["2"]["char"] = star2
    BASE_DICT["1"]["char"] = star1
    # endregion

    # region current_pools
    region_name_map = {
        "Jp": "日服",
        "Global": "国际服",
        "Cn": "国服",
    }

    pools = []

    common_data = cast(dict, await schale_get("data/config.min.json"))
    regions: List[dict] = common_data["Regions"]

    for region in regions:
        region_name = region_name_map[region["Name"]]
        gachas = region["CurrentGacha"]
        for gacha in gachas:
            if not (gacha["start"] <= time.time() < gacha["end"]):
                continue

            characters = gacha["characters"]
            three_star: List[dict] = [
                stu_dict[x] for x in characters if stu_dict[x]["StarGrade"] == 3
            ]
            three_star_ids = [x["Id"] for x in three_star]
            others: List[dict] = [
                stu_dict[x] for x in characters if x not in three_star_ids
            ]

            for up in three_star:
                name = "、".join((up["Name"], *(x["Name"] for x in others)))
                ids = [up["Id"], *(x["Id"] for x in others)]
                pools.append({"name": f"【{region_name}】{name}", "pool": ids})

    print(f"gacha: 当期卡池：{json.dumps(pools, ensure_ascii=False, indent=2)}")
    # endregion

    async with aiofiles.open(str(GACHA_JSON_PATH), encoding="u8") as f:
        j = json.loads(await f.read())
    j["base"] = BASE_DICT
    j["current_pools"] = pools

    dump_j = json.dumps(j, indent=2, ensure_ascii=False)

    async with aiofiles.open(str(GACHA_JSON_PATH), "w", encoding="u8") as f:
        await f.write(dump_j)

    print("gacha: complete")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
