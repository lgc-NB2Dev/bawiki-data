#!/usr/bin/env python

SHELL_FOLDER=$(dirname "$0")

pip install pathlib aiofiles aiohttp cn-sort
python "${SHELL_FOLDER}/update_alias_list.py"
