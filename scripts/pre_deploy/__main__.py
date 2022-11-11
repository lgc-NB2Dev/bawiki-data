import asyncio
import importlib
from pathlib import Path


async def run():
    tasks = [
        importlib.import_module(x, "scripts.pre_deploy").main()
        for x in [
            f".{y.stem}"
            for y in Path(__file__).parent.iterdir()
            if y.is_file() and (not y.name.startswith("_"))
        ]
    ]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(run())
