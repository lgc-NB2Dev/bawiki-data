import asyncio
import json
from asyncio import Semaphore
from pathlib import Path
from typing import Any, TypedDict

from aiohttp import ClientSession
from bs4 import BeautifulSoup, PageElement

MANGA_JSON = Path(__file__).parent.parent / "data" / "manga.json"


class Manga(TypedDict):
    cid: int
    title: str
    detail: str
    pics: list[str]


async def async_req(
    url: str,
    *args,
    method: str = "GET",
    is_json: bool = True,
    raw: bool = False,
    **kwargs,
) -> str | bytes | dict[str, Any] | list:
    async with ClientSession() as s:
        async with s.request(method, url, *args, **kwargs) as r:
            ret = (await r.read()) if raw else (await r.text())
    if is_json and (not raw):
        ret = json.loads(ret)
    return ret


async def game_kee_req(suffix: str, *args, **kwargs) -> dict[str, Any] | list[Any]:
    ret = await async_req(
        f"https://ba.gamekee.com/{suffix}",
        *args,
        headers={"game-id": "0", "game-alias": "ba"},
        proxy=None,
        **kwargs,
    )
    if ret["code"] != 0:
        raise ConnectionError(ret["msg"])
    return ret["data"]


def tags_to_str(tag: PageElement) -> str:
    if c := getattr(tag, "contents", None):
        return "".join([s for x in c if (s := tags_to_str(x))])

    else:
        if s := tag.text.strip().replace("\u200b", ""):
            return s
        elif tag.name == "img" or tag.name == "br":
            return "\n"
        else:
            return ""


async def _get_article(article_id: int, title_prefix: str) -> Manga:
    while True:
        try:
            article: dict = await game_kee_req(f"v1/content/detail/{article_id}")
            soup = BeautifulSoup(article["content"], "lxml")
            detail = tags_to_str(soup).strip()
            if "汉化：" in detail:
                detail = detail.replace("汉化：", "\n汉化：").replace("\n）", "）")
            manga = Manga(
                cid=article_id,
                title=f'{title_prefix}{article["title"]}',
                detail=detail,
                pics=[
                    f"https:{src}"
                    for x in soup.find_all("img")
                    if (not (src := x["src"]).endswith(".gif")) and "gamekee" in src
                ],
            )
        except Exception as e:
            print(f"manga: article {article_id} err: {e!r}, retry")
            continue

        print(f"manga: article {article_id} ok")
        return manga


async def get_article(article_id: int, title_prefix: str, s: Semaphore) -> Manga:
    async with s:
        return await _get_article(article_id, title_prefix)


async def main():
    # print(await _get_article(155021))
    # return

    entries: dict = await game_kee_req("v1/wiki/entry")
    manga_entry = [x for x in entries["entry_list"] if x["id"] == 51508][0]
    article_ids: list[tuple[int, str]] = []
    for i in manga_entry["child"]:
        prefix = name if "四格" in (name := i["name"]) else "【ぶるーあーかいぶっ！】"
        article_ids.extend([(x["content_id"], prefix) for x in i["child"]])

    with MANGA_JSON.open(encoding="u8") as f:
        org_j: list[Manga] = json.loads(f.read() or "[]")

    excepts = [x["cid"] for x in org_j] + [170611]
    print(f"manga: excepts: {excepts}")
    for i in article_ids.copy():
        if i[0] in excepts:
            article_ids.remove(i)

    print(f"manga: total articles: {len(article_ids)}")

    s = Semaphore(8)
    mangas = await asyncio.gather(
        *[get_article(x, prefix, s) for x, prefix in article_ids]
    )
    mangas += org_j
    mangas.sort(key=lambda x: x["cid"])

    obj = json.dumps(mangas, ensure_ascii=False, indent=2)
    with MANGA_JSON.open("w", encoding="u8") as f:
        f.write(obj)

    print("manga: complete")


if __name__ == "__main__":
    asyncio.run(main())
