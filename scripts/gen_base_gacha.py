import json
from pathlib import Path

import requests

BASE_DICT = {
    "3": {"chance": 2.5, "char": []},
    "2": {"chance": 18.5, "char": []},
    "1": {"chance": 79.0, "char": []},
}

PATH = Path(__file__).parent


def main():
    stu_li = requests.get(
        "https://lonqie.github.io/SchaleDB/data/cn/students.json"
    ).json()

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

        print(f'{star_grade}星{"[限定]" if limited else " 常驻 "}：({s_id}) {s_name}')

    star3.sort()
    star2.sort()
    star1.sort()

    BASE_DICT["3"]["char"] = star3
    BASE_DICT["2"]["char"] = star2
    BASE_DICT["1"]["char"] = star1

    with open(str(PATH.parent / "data" / "gacha.json"), encoding="u8") as f:
        j = json.load(f)
    j["base"] = BASE_DICT

    dump_j = json.dumps(j, indent=2, ensure_ascii=False)
    print(dump_j)

    with open(str(PATH.parent / "data" / "gacha.json"), "w", encoding="u8") as f:
        f.write(dump_j)


if __name__ == "__main__":
    main()
