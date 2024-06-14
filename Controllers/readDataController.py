import json
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(process)d - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def read_json(path: str):
    with open(path, mode="r", encoding="utf-8-sig") as file:
        result = json.load(file)
    return result

