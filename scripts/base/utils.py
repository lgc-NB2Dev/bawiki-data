import json
from typing import Any, Dict, Union, cast

from aiohttp import ClientSession
from bs4 import Tag
from cn_sort import sort_text_list

from .const import GAMEKEE_URL, SCHALE_URL


async def async_req(
    url: str,
    *args,
    method: str = "GET",
    is_json: bool = True,
    raw: bool = False,
    **kwargs,
) -> Any:
    async with ClientSession() as c:
        async with c.request(method, url, *args, **kwargs) as r:
            data = (await r.read()) if raw else (await r.text())
            print(f"req {url}: {repr(data)[:50]}")

    if is_json:
        if raw:
            raise TypeError("Raw 与 Json 不可同时为 True")
        data = json.loads(data)

    return data


async def schale_get(suffix: str, raw: bool = False):
    return await async_req(f"{SCHALE_URL}{suffix}", raw=raw)


async def schale_get_stu_data(
    locale: str = "cn",
    key: str = "Id",
    raw: bool = False,
) -> Union[dict[str, dict], list[dict]]:
    r = await schale_get(f"data/{locale}/students.min.json")
    return r if raw else {x[key]: x for x in r}


async def game_kee_req(
    suffix: str,
    *args,
    **kwargs,
) -> Union[dict[str, Any], list[Any]]:
    ret = await async_req(
        f"{GAMEKEE_URL}{suffix}",
        *args,
        headers={"game-id": "829", "game-alias": "ba"},
        proxy=None,
        **kwargs,
    )
    if ret["code"] != 0:
        raise ConnectionError(ret["msg"])
    return ret["data"]


def replace_brackets(s: str):
    return s.replace("（", "(").replace("）", ")")


def tags_to_str(tag: Tag) -> str:
    if c := getattr(tag, "contents", None):
        return "".join([s for x in c if (s := tags_to_str(x))])
    if s := tag.text.strip().replace("\u200b", ""):
        return s
    if tag.name == "img" or tag.name == "br":
        return "\n"
    return ""


def sort_json_keys(will_sort: dict) -> dict:
    return {k: will_sort[k] for k in sort_text_list(will_sort.keys())}


async def game_kee_get_stu_li() -> Dict[str, dict]:
    ret = cast(dict, await game_kee_req("v1/wiki/entry"))

    entry_stu = next(
        (x for x in ret["entry_list"] if x["id"] == 23941),
        None,
    )
    if not entry_stu:
        return {}

    entry_stu_all = next(
        (x for x in entry_stu["child"] if x["id"] == 49443),
        None,
    )
    if not entry_stu_all:
        return {}

    return {x["name"]: x for x in entry_stu_all["child"]}
