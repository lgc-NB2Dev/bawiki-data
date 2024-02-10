import asyncio
import json
import os
from typing import cast

from ..base.const import WIKI_JSON_PATH
from ..base.utils import replace_brackets, schale_get_stu_data, sort_json_keys


async def main():
    cn_stu, en_stu = cast(
        tuple[dict, dict],
        await asyncio.gather(
            *(schale_get_stu_data("cn"), schale_get_stu_data("en")),
        ),
    )

    mapping = sort_json_keys(
        {
            replace_brackets(y["Name"]): en_stu[x]["Name"].lower()
            for x, y in cn_stu.items()
        },
    )

    # print(json.dumps(mapping, ensure_ascii=False))

    wiki_json = json.loads(WIKI_JSON_PATH.read_text(encoding="u8"))
    student_json = wiki_json["student"]

    wiki_students = {"all": student_json.get("all", "img/student/_all.png")}
    for k, v in mapping.items():
        path = f"img/student/{v}.png"

        if not os.path.exists(path):  # noqa: PTH110
            original_path = student_json.get(k)

            if original_path and ("_extra" in original_path):
                print(f'update_stu_li: {k} 角评为 "_extra"，忽略')
                wiki_students[k] = original_path
                continue

            print(f"update_stu_li: !!! WARNING !!! {k} 角评不存在! <{path}>")
            k = f"_{k}"

        wiki_students[k] = path

    unknown_stu = {k: v for k, v in student_json.items() if k not in wiki_students}
    for k, v in unknown_stu.items():
        print(f"update_stu_li: 未知学生 {k} 角评 <{v}>")
        wiki_students[k] = v

    wiki_json["student"] = wiki_students

    WIKI_JSON_PATH.write_text(
        json.dumps(wiki_json, ensure_ascii=False, indent=2),
        encoding="u8",
    )
    print("update_stu_li: complete")


if __name__ == "__main__":
    asyncio.run(main())
