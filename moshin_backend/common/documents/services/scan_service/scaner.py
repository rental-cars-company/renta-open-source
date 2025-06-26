from typing import Sequence

import cv2
import numpy as np
import pytesseract
from django.conf import settings
from PIL.Image import Image


def init_tesseract(_path: str | None = "E:\\tesseract\\model\\tesseract"):
    if _path is None:
        _path = settings.TESSERACT_CMD_PATH

    try:
        pytesseract.pytesseract.tesseract_cmd = _path
        pytesseract.get_tesseract_version()

    except pytesseract.pytesseract.TesseractNotFoundError:
        print(
            f"""
            |---------------------------------------------------------------------------|
            | Ошибка запуска Tesseract по пути: {_path}            |
            | Установить путь до Tesseract нужно в переменную среды TESSERACT_CMD_PATH  |
            |---------------------------------------------------------------------------|
            """
        )


def cv_image_from_pil(pil_image: Image) -> cv2.typing.MatLike:
    npdata: np.ndarray = np.array(pil_image, dtype=np.uint8)
    image = cv2.cvtColor(npdata, code=cv2.COLOR_RGB2BGR)
    resized_img = cv2.resize(image, (800, 500), interpolation=cv2.INTER_CUBIC)
    return resized_img


def cv_charpen_image(image: cv2.typing.MatLike) -> cv2.typing.MatLike:
    # Enhance contrast
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # Light blur
    blurred = cv2.GaussianBlur(enhanced, (3, 3), 0)

    # Adaptive threshold (handles bright areas better)
    thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    return thresh


def cv_get_greyscale(image: cv2.typing.MatLike) -> cv2.typing.MatLike:
    _kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 7))

    img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, _kernel)
    img = cv2.fastNlMeansDenoising(img, None, 20, 7, 21)
    return img


def cv_get_text_mask(
    greyscaled_image: cv2.typing.MatLike,
) -> cv2.typing.MatLike:
    _recatngle_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 7))
    _square_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (32, 32))

    #  Sobel–Feldman
    grad = cv2.Sobel(greyscaled_image, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=7)
    grad = np.absolute(grad)
    (minVal, maxVal) = (np.min(grad), np.max(grad))
    grad = (grad - minVal) / (maxVal - minVal)
    grad = (grad * 255).astype("uint8")

    grad = cv2.morphologyEx(grad, cv2.MORPH_CLOSE, _recatngle_kernel)
    thresh = cv2.threshold(grad, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, _square_kernel)
    thresh = cv2.erode(thresh, None, iterations=1)  # type: ignore

    # cv2.imshow('s', thresh)
    # cv2.waitKey(0)

    return thresh


def cv_find_bboxes(image_greyscale: cv2.typing.MatLike) -> Sequence:
    processed = cv_get_text_mask(image_greyscale)

    cnts, _ = cv2.findContours(
        processed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    rectangles = []
    for contour in cnts:
        rect: cv2.typing.Rect = cv2.boundingRect(contour)
        rect = [rect[0] - 4, rect[1] - 4, rect[2] + 8, rect[3] + 8]
        rectangles.append(rect)

    return rectangles


def get_text_from_image(image: cv2.typing.MatLike, language):

    try:
        custom_oem_psm_config = r"--oem 3 --psm 6"
        text = pytesseract.image_to_string(
            image=image, lang=language, config=custom_oem_psm_config
        )
        return text
    except:
        return ""
