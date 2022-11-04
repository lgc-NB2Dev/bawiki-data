#!/usr/bin/env python

SHELL_FOLDER=$(dirname "$0")

pip install pathlib aiofiles aiohttp cn-sort requests beautifulsoup4 lxml
python "${SHELL_FOLDER}/update_alias_list.py"
python "${SHELL_FOLDER}/gen_base_gacha.py"
python "${SHELL_FOLDER}/update_emoji_list.py"
python "${SHELL_FOLDER}/update_comic.py"
