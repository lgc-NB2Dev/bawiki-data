import asyncio
import json
from asyncio import Semaphore

import aiofiles
from bs4 import BeautifulSoup

from ..base.const import MANGA_JSON_PATH, Manga
from ..base.utils import async_read_file, game_kee_req, tags_to_str


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
        prefix = (
            name[: name.rfind("】") + 1]
            if (name := i["name"]).startswith("【")
            else "【ぶるーあーかいぶっ！】"
        )
        article_ids.extend(
            [(cid, prefix) for x in i["child"] if not (cid := x["content_id"]) == 0]
        )

        org_j: list[Manga] = (
            json.loads(await async_read_file(str(MANGA_JSON_PATH)))
            if MANGA_JSON_PATH.exists()
            else []
        )

    excepts = [x["cid"] for x in org_j] + [170611, 172246]
    print(f"manga: excepts articles: {len(excepts)}")
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
    async with aiofiles.open(str(MANGA_JSON_PATH), "w", encoding="u8") as f:
        await f.write(obj)

    print("manga: complete")
