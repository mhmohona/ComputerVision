# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from base64 import b64encode
import math
from pathlib import Path
from typing import List, Tuple, Union 

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


def im2base64(im_path: Union[Path, str]) -> bytes:
    """Get image bytes.

    Args:
        im_path (string): Path to the image

    Returns:
        im_bytes
    """

    with open(im_path, "rb") as image:
        # Extract image bytes
        im_content = image.read()
        # Convert bytes into a string
        im_bytes = b64encode(im_content)

    return im_bytes


def ims2strlist(im_path_list: list) -> list:
    """Get byte-str list of the images in the given path.

    Args:
        im_path_list (list of strings): List of image paths

    Returns:
        im_string_list: List containing based64-encoded images
            decoded into strings
    """

    im_string_list = []
    for im_path in im_path_list:
        im_string_list.append(im2base64(im_path).decode("utf-8"))

    return im_string_list


def im_width(input: Union[str, np.array]) -> int:
    """Returns the width of an image.
    Args:
        input: Image path or image as numpy array.
    Return:
        Image width.
    """
    return im_width_height(input)[0]


def im_height(input: Union[str, np.array]) -> int:
    """Returns the height of an image.
    Args:
        input: Image path or image as numpy array.
    Return:
        Image height.
    """
    return im_width_height(input)[1]


def im_width_height(input: Union[str, np.array]) -> Tuple[int, int]:
    """Returns the width and height of an image.
    Args:
        input: Image path or image as numpy array.
    Return:
        Tuple of ints (width,height).
    """
    if isinstance(input, str) or isinstance(input, Path):
        width, height = Image.open(
            input
        ).size  # this is fast since it does not load the full image
    else:
        width, height = (input.shape[1], input.shape[0])
    return width, height


def show_ims(
    im_paths: Union[str, List[str]],
    labels: Union[str, List[str]]=None,
    size: int=3,
    rows: int=1,
):
    """Show image files
    Args:
        im_paths (str or List[str]): Image filepaths
        labels (str or List[str]): Image labels. If None, show image file name.
        size (int): MatplotLib plot size.
        rows (int): rows of the images
    """
    if isinstance(im_paths, (str, Path)):
        if labels is not None and isinstance(labels, str):
            labels = [labels]
        ims = [mpimg.imread(im_paths)]
        im_paths = [im_paths]
    else:
        ims = [mpimg.imread(im_path) for im_path in im_paths]
    
    cols = math.ceil(len(ims)/rows)
    _, axes = plt.subplots(rows, cols, figsize=(size*cols, size*rows))
    axes = np.array(axes).reshape(-1)

    for i, (im_path, im) in enumerate(zip(im_paths, ims)):
        if labels is None:
            axes[i].set_title(Path(im_path).stem)
        else:
            axes[i].set_title(labels[i])
        axes[i].set_axis_off()
        axes[i].imshow(im)
