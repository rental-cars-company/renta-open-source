import re
from typing import Any

from PIL.Image import Image

from . import scaner
from .date_parser import parse_date
from .exeptions import ReadingDocumentError

UZ_DRIVER_LICENSE_RE = re.compile(
    r"1\.?\s+(?P<surname>[A-Z]+)\s*\n"
    r"2\.?\s+(?P<name>[A-Z]+)\s*\n"
    r"(?P<PATRONYM>[A-Z\s']+)\s*\n"
    r"3\.?\s+[A-Z]+\s+[A-Z]+\s+(?P<date_of_birth>\d\d\s?\d\d\s?\d\d\s?\d\d)\s*\n"
    r"4a\s+(?P<acquire_date>\d\d\s?\d\d\s?\d\d\s?\d\d)"
    r"\s+4b\s+(?P<validity_period>\d\d\s?\d\d\s?\d\d\s?\d\d)\s*\n"
    r"4[a-c]\s+.*\n4[a-c]\s+.*\n5\s+.*\n"
    r".*\n.*\n9\s?(?P<b_category>[6|B])"
)
UZ_DRIVER_LICENSE_RE_GROUPS = (
    "surname",
    "name",
    "date_of_birth",
    "acquire_date",
    "validity_period",
    "b_category",
)
UZ_DRIVER_LICENSE_RE_DATE_GROUPS = (
    "date_of_birth",
    "acquire_date",
    "validity_period",
)


def parse_main_driverlicense_data(text: str) -> dict[str, Any]:
    match = UZ_DRIVER_LICENSE_RE.search(text)
    data = {}

    if match is None:
        raise ReadingDocumentError()

    for group_name in UZ_DRIVER_LICENSE_RE_GROUPS:
        data[group_name] = match.group(group_name)  # type: ignore

    for date_gr_name in UZ_DRIVER_LICENSE_RE_DATE_GROUPS:
        data[date_gr_name] = parse_date(data[date_gr_name])

    if "b_category" in data.keys():
        del data["b_category"]
        data["has_b_category"] = True

    return data


def get_driverlicense_data(image: Image, language="uzb"):
    img = scaner.cv_image_from_pil(image)
    greyscale = scaner.cv_get_greyscale(img)
    bboxes = scaner.cv_find_bboxes(greyscale)
    img_H, img_W = img.shape[:2]

    data = {}

    for x, y, w, h in bboxes:
        if h > img_H * 0.4 and w > img_W * 0.4:
            h = greyscale.shape[0]
            cropped = greyscale[y:h, x : x + w]
            text = scaner.get_text_from_image(cropped, language)
            parsed_data = parse_main_driverlicense_data(text)
            data = {**data, **parsed_data}

    return data
