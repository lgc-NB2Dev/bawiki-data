import json
from typing import Any

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

    if is_json:
        if raw:
            raise TypeError("Raw 与 Json 不可同时为 True")
        data = json.loads(data)

    print(f"req {url}: {data[:50]}")
    return data


async def schale_get(suffix: str, raw: bool = False):
    return await async_req(f"{SCHALE_URL}{suffix}", raw=raw)


async def schale_get_stu_data(
    locale: str = "cn",
    key: str = "Id",
    raw: bool = False,
) -> dict[str, dict] | list[dict]:
    r = await schale_get(f"data/{locale}/students.min.json")
    return r if raw else {x[key]: x for x in r}


async def game_kee_req(suffix: str, *args, **kwargs) -> dict[str, Any] | list[Any]:
    ret = await async_req(
        f"{GAMEKEE_URL}{suffix}",
        *args,
        headers={"game-id": "0", "game-alias": "ba"},
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
