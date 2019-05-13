from typing import Dict, Optional, cast

from util.safe_json import safe_loads, OnError
from util.files import read_file

CONFIG_PATH = 'config.json'

config_type = {
    'url': str,
    'https_enabled': bool,
}

def config() -> Dict[str, str]:
    s = read_file(CONFIG_PATH)
    return cast(
        Dict[str, str],
        safe_loads(s, config_type, OnError.RAISE_EXCEPTION),
    )

