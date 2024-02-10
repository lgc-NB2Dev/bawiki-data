import asyncio
import json
import logging

import anyio
from cn_sort import sort_text_list

from ..base.const import ALIAS_JSON_PATH, SUFFIX_ALIAS_JSON_PATH
from ..base.utils import (
    replace_brackets,
    schale_get_stu_data,
    sort_json_keys,
)


async def main():
    logging.disable(999)

    cn_stu, jp_stu, en_stu, alias_li, suff_li = await asyncio.gather(
        *[
            schale_get_stu_data("cn"),
            schale_get_stu_data("jp"),
            schale_get_stu_data("en"),
            await anyio.Path(ALIAS_JSON_PATH).read_text(encoding="u8"),
            await anyio.Path(SUFFIX_ALIAS_JSON_PATH).read_text(encoding="u8"),
        ],
    )

    # async with aiofiles.open(str(ALIAS_BAK_PATH), "w", encoding="utf-8") as f:
    #     await f.write(alias_li)

    alias_li = json.loads(alias_li)
    suff_li = json.loads(suff_li)

    replaced_alias_li = alias_li

    for s_id, cn in cn_stu.items():
        cn_name = replace_brackets(cn["Name"])
        org_li = set(alias_li.get(cn_name) or set())

        jp = jp_stu[s_id]
        en = en_stu[s_id]

        jp_name = replace_brackets(jp["Name"])
        en_name = en["Name"].lower()
        alias_names = {jp_name, en_name}

        if not cn_name.startswith(cn["FamilyName"]):
            alias_names.update(
                {
                    f"{cn['FamilyName']}{cn_name}",
                    f"{jp['FamilyName']}{jp_name}",
                    f"{en['FamilyName']} {en['Name']}".lower(),
                },
            )

        if jp_name != cn_name and jp_name in alias_li:
            org_li = set(alias_li[jp_name])
            del alias_li[jp_name]

        org_li.update(alias_names)

        if "(" in cn_name:
            split = cn_name.split("(")
            cn_org_name = split[0]
            suffix = split[1][:-1]
            if ((suffix_alias := suff_li.get(suffix)) is not None) and (
                org_id := [k for k, v in cn_stu.items() if v["Name"] == cn_org_name]
            ):
                org_id = org_id[0]

                org_alias = {cn_org_name, *(alias_li.get(cn_org_name) or [])}
                org_fullname = {
                    f"{cn['FamilyName']}{cn['PersonalName']}",
                    f"{jp['FamilyName']}{jp['PersonalName']}",
                    f"{en['FamilyName']} {en['PersonalName']}".lower(),
                }
                org_alias.difference_update(org_fullname)

                suffix_alias = [suffix, *suffix_alias]

                for sa in suffix_alias:
                    for al in org_alias:
                        org_li.add(f"{sa}{al}")

        org_li = list(sort_text_list(list(org_li)))
        replaced_alias_li[cn_name] = org_li
        print(f"stu_alias: {cn_name}: {'; '.join(org_li)}")
        # await asyncio.sleep(0)

    cn_names = [replace_brackets(x["Name"]) for x in cn_stu.values()]
    for k, _ in replaced_alias_li.items().keys():
        if k not in cn_names:
            print(f"stu_alias: !!! WARNING !!! 别名列表中的未知学生 {k}")

    await anyio.Path(ALIAS_JSON_PATH).write_text(
        replace_brackets(
            json.dumps(
                sort_json_keys(replaced_alias_li),
                ensure_ascii=False,
                indent=2,
            ),
        ).lower(),
        encoding="u8",
    )

    print("stu_alias: complete")
