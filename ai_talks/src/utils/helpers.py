import base64
import os
import random
from pathlib import Path
from typing import List


def render_svg(svg: Path) -> str:
    """Renders the given svg string."""
    with open(svg) as file:
        b64 = base64.b64encode(file.read().encode("utf-8")).decode("utf-8")
        return f"<img src='data:image/svg+xml;base64,{b64}'/>"


def get_files_in_dir(path: Path) -> List[str]:
    files = []
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            files.append(file)
    return files


def get_random_img(img_names: list[str]) -> str:
    return random.choice(img_names)
