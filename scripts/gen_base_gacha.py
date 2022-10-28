import json
from pathlib import Path
import requests

BASE_DICT = [
    {
        "server": 0,
        "3": {"chance": 2.5, "char": []},
        "2": {"chance": 18.5, "char": []},
        "1": {"chance": 79.0, "char": []},
    },
    {
        "server": 1,
        "3": {"chance": 2.5, "char": []},
        "2": {"chance": 18.5, "char": []},
        "1": {"chance": 79.0, "char": []},
    },
]
PATH = Path(__file__).parent


def main():
    with open(str(PATH / "gacha_2star.txt"), encoding="u8") as f:
        star2_names = f.read().split("\n")
    with open(str(PATH / "gacha_1star.txt"), encoding="u8") as f:
        star1_names = f.read().split("\n")

    stu_li = requests.get(
        "https://lonqie.github.io/SchaleDB/data/en/students.json"
    ).json()
    res_g = []
    res_j = []
    star2 = []
    star1 = []
    for i in stu_li:
        s_id = i["Id"]
        match i["StarGrade"]:
            case 3:
                if not i["IsLimited"]:
                    j_re, g_re = i["IsReleased"]
                    if j_re:
                        res_j.append(s_id)
                    if g_re:
                        res_g.append(s_id)
            case 2:
                if i["Name"].lower() in star2_names:
                    star2.append(s_id)
            case 1:
                if i["Name"].lower() in star1_names:
                    star1.append(s_id)

    res_g.sort()
    res_j.sort()
    star2.sort()
    star1.sort()

    BASE_DICT[0]["3"]["char"] = res_j
    BASE_DICT[1]["3"]["char"] = res_g
    BASE_DICT[0]["2"]["char"] = star2
    BASE_DICT[1]["2"]["char"] = star2
    BASE_DICT[0]["1"]["char"] = star1
    BASE_DICT[1]["1"]["char"] = star1

    print(BASE_DICT)

    with open(str(PATH.parent / "data" / "gacha.json"), encoding="u8") as f:
        j = json.load(f)
    j["base"] = BASE_DICT

    with open(str(PATH.parent / "data" / "gacha.json"), "w", encoding="u8") as f:
        f.write(json.dumps(j, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
