import os

import fitz
import PIL.Image
from PIL.Image import Image

IMG_SAVE_MODE = "RGB"


def open_file(path: str) -> list[Image]:
    extension = os.path.splitext(path)[1]

    if extension == ".pdf":
        fitz_file = fitz.open(filename=path)
        pixmaps: list[fitz.Pixmap] = [
            page.get_pixmap() for page in fitz_file  # type: ignore
        ]
        images: list[Image] = [
            pm.pil_image().convert(mode=IMG_SAVE_MODE) for pm in pixmaps
        ]
        return images

    else:
        image = PIL.Image.open(path).convert(mode=IMG_SAVE_MODE)
        return [
            image,
        ]
