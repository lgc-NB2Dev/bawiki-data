from asyncio import run
import json

from ..base.utils import game_kee_get_stu_li, schale_get_stu_data


async def main():
    gamekee_stu_list = list(await game_kee_get_stu_li())
    schale_stu = await schale_get_stu_data("cn")
    schale_stu_list = (
        [x["Name"] for x in schale_stu.values()] if isinstance(schale_stu, dict) else []
    )
    # print(gamekee_stu_list)
    gamekee_diff = [stu for stu in schale_stu_list if stu not in gamekee_stu_list]
    schale_diff = [stu for stu in gamekee_stu_list if stu not in schale_stu_list]
    print("Gamekee Diff (not in Schale) >", schale_diff)
    print("Schale Diff (not in Gamekee) >", gamekee_diff)
    # prepare_dict = dict.fromkeys(gamekee_diff, "")
    # print(json.dumps(prepare_dict, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    run(main())
