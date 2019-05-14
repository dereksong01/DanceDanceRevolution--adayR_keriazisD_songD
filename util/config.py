from typing import Dict, Optional, NamedTuple, cast

from util.safe_json import safe_loads, OnError
from util.files import read_file

CONFIG_PATH = 'config.json'

config_type = {
    'url': str,
    'https_enabled': bool,
}

class Config(NamedTuple):
    url: str
    https_enabled: bool

def config() -> Config:
    s = read_file(CONFIG_PATH)
    return cast(Config, safe_loads(s, Config, OnError.RAISE_EXCEPTION))

