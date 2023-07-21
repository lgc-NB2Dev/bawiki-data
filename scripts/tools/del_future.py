import json

from ..base.const import WIKI_JSON_PATH


def main():
    pop_num = int(input("请输入要去掉的列表项数量："))
    offset_y = int(input("请输入全局y坐标偏移："))

    with open(str(WIKI_JSON_PATH), encoding="u8") as f:
        wiki_json = json.loads(f.read())

    future_parts: list = wiki_json["global_future"]["parts"]
    part1 = future_parts[0]

    for _ in range(pop_num):
        future_parts.pop(0)

    part2 = future_parts[0]
    reduce = part2["part"][0] - part1["part"][0]
    # print(reduce)

    wiki_json["global_future"]["banner"][1] += offset_y
    for p in future_parts:
        p["part"] = [x - reduce + offset_y for x in p["part"]]

    with open(str(WIKI_JSON_PATH), "w", encoding="u8") as f:
        f.write(json.dumps(wiki_json, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
