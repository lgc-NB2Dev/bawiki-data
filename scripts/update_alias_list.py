import asyncio
import json
from pathlib import Path

import aiofiles
from aiohttp import ClientSession

SCHALE_URL = "https://lonqie.github.io/SchaleDB/"
ROOT_PATH = Path(__file__).parent.parent
ALIAS_PATH = ROOT_PATH / "data" / "stu_alias.json"
ALIAS_BAK_PATH = ROOT_PATH / "data" / "stu_alias.json.bak"


async def schale_get(suffix, raw=False):
    async with ClientSession() as c:
        async with c.get(f"{SCHALE_URL}{suffix}") as r:
            return (await r.read()) if raw else (await r.json())


async def schale_get_stu_data(locale):
    r = await schale_get(f"data/{locale}/students.min.json")
    return {x["Id"]: x for x in r}


async def read_file(path, mode="r", encoding="utf-8", **kwargs):
    async with aiofiles.open(str(path), mode, encoding=encoding, **kwargs) as f:
        return await f.read()


async def main():
    cn_stu, jp_stu, en_stu, alias_li = await asyncio.gather(
        *[
            schale_get_stu_data("cn"),
            schale_get_stu_data("jp"),
            schale_get_stu_data("en"),
            read_file(ALIAS_PATH),
        ]
    )

    async with aiofiles.open(str(ALIAS_BAK_PATH), "w", encoding="utf-8") as f:
        await f.write(alias_li)

    alias_li = json.loads(alias_li)

    for s_id, s in cn_stu.items():
        org_li = alias_li.get(cn_name := s["Name"]) or []
        replace_li = []

        jp = jp_stu[s_id]
        en = en_stu[s_id]

        jp_n = jp["Name"]
        if jp_n != cn_name:
            if jp_n in alias_li:
                org_li = alias_li[jp_n]
                del alias_li[jp_n]

            if jp_n not in org_li:
                replace_li.append(jp_n)

        if (en_n := en["Name"]) not in org_li:
            replace_li.append(en_n)

        replace_li.extend(org_li)
        replace_li.sort()
        alias_li[cn_name] = replace_li

    async with aiofiles.open(str(ALIAS_PATH), "w", encoding="utf-8") as f:
        await f.write(
            json.dumps(alias_li, ensure_ascii=False, indent=2)
            .replace("（", "(")
            .replace("）", ")")
            .lower()
        )


if __name__ == "__main__":
    asyncio.run(main())
