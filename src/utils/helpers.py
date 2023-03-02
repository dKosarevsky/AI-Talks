from typing import Any, Dict, List, Optional


def get_dict_key(dictionary: Dict, value: Any) -> Optional[Any]:
    for key, val in dictionary.items():
        if val == value:
            return key
