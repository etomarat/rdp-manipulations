import numpy as np
import cv2  # type: ignore
from rdp_manipulations.logger import logger

from typing import Optional

ImageLocatorType = Optional[dict[str, float]]
ImageLocatorCenterType = Optional[tuple[float, float]]


def image_diff(image_path1: str, image_path2: str) -> float:
    image1 = cv2.imread(image_path1)
    image2 = cv2.imread(image_path2)
    try:
        errorL2 = cv2.norm(image1, image2, cv2.NORM_L2)
        height, width, *_ = image1.shape
        similarity = 1 - errorL2 / (height * width)
        logger.debug(
            f'Image {image_path1} and {image_path2} similarity: {similarity}')
        return similarity
    except Exception:
        return 0


def is_image_identic(to_locate_path: str, where_locate_path: str, threshold: float = 0.8) -> bool:
    logger.debug(f'called is_image_identic with threshold {threshold}')
    return image_diff(to_locate_path, where_locate_path) >= threshold


def image_locate(to_locate_path: str, where_locate_path: str, threshold: float = 0.8) -> ImageLocatorType:
    logger.debug(f'called image_locate with threshold {threshold}')
    to_locate = cv2.imread(to_locate_path)
    where_locate = cv2.imread(where_locate_path)
    matxh_result = cv2.matchTemplate(where_locate, to_locate, cv2.TM_CCOEFF_NORMED)

    # Magic ->
    match_indices = np.arange(matxh_result.size)[
        (matxh_result.astype(float) > threshold).flatten()]
    result = np.unravel_index(match_indices, matxh_result.shape)
    # Magic -<

    try:
        y, x, = map(lambda c: int(c) if c.size else False, result)
        height, width, *_ = to_locate.shape
    except TypeError:
        return image_locate(to_locate_path, where_locate_path, threshold=threshold + 0.01)

    if not (x or y):
        return None

    return {
        'x': x,
        'y': y,
        'width': width,
        'height': height
    }


def image_locate_center(to_locate_path: str, where_locate_path: str, threshold: float = 0.8) -> ImageLocatorCenterType:
    location = image_locate(to_locate_path, where_locate_path, threshold)

    if location is None:
        return None

    x = location['x'] + location['width'] / 2
    y = location['y'] + location['height'] / 2

    return (x, y)


def is_image_contain(to_locate_path: str, where_locate_path: str, threshold: float = 0.8) -> bool:
    return image_locate(to_locate_path, where_locate_path, threshold) is not None
