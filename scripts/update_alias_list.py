import asyncio
import json
from pathlib import Path

import aiofiles
from aiohttp import ClientSession
from cn_sort import sort_text_list

SCHALE_URL = "https://lonqie.github.io/SchaleDB/"
ROOT_PATH = Path(__file__).parent.parent
ALIAS_PATH = ROOT_PATH / "data" / "stu_alias.json"
ALIAS_BAK_PATH = ROOT_PATH / "data" / "stu_alias.json.bak"
SUFFIX_ALIAS_PATH = ROOT_PATH / "data" / "suffix_alias.json"


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


def replace_brackets(s):
    return s.replace("（", "(").replace("）", ")")


async def main():
    cn_stu, jp_stu, en_stu, alias_li, suff_li = await asyncio.gather(
        *[
            schale_get_stu_data("cn"),
            schale_get_stu_data("jp"),
            schale_get_stu_data("en"),
            read_file(ALIAS_PATH),
            read_file(SUFFIX_ALIAS_PATH),
        ]
    )

    # async with aiofiles.open(str(ALIAS_BAK_PATH), "w", encoding="utf-8") as f:
    #     await f.write(alias_li)

    alias_li = json.loads(alias_li)
    suff_li = json.loads(suff_li)

    replaced_alias_li = alias_li

    for s_id, s in cn_stu.items():
        org_li = set(alias_li.get(cn_name := replace_brackets(s["Name"])) or set())

        jp = jp_stu[s_id]
        en = en_stu[s_id]

        jp_n = replace_brackets(jp["Name"])
        en_n = en["Name"].lower()

        if jp_n != cn_name:
            if jp_n in alias_li:
                org_li = set(alias_li[jp_n])
                del alias_li[jp_n]

        org_li.add(jp_n)
        org_li.add(en_n)

        if "(" in cn_name:
            split = cn_name.split("(")
            cn_org_name = split[0]
            suffix = split[1][:-1]
            if (suffix_alias := suff_li.get(suffix)) and (
                org_id := [k for k, v in cn_stu.items() if v["Name"] == cn_org_name]
            ):
                org_id = org_id[0]
                org_alias = [cn_org_name] + (alias_li.get(cn_org_name) or [])
                suffix_alias = [suffix] + suffix_alias
                for sa in suffix_alias:
                    for al in org_alias:
                        org_li.add(f"{sa}{al}")

        org_li = list(sort_text_list(list(org_li)))
        replaced_alias_li[cn_name] = org_li

    async with aiofiles.open(str(ALIAS_PATH), "w", encoding="utf-8") as f:
        await f.write(
            replace_brackets(
                json.dumps(replaced_alias_li, ensure_ascii=False, indent=2)
            ).lower()
        )


if __name__ == "__main__":
    asyncio.run(main())
