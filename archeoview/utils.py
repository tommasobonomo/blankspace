import os
import rasterio as rio
import numpy as np

from typing import List, Tuple


def geotiff_to_numpy(image_path: str) -> Tuple[List[str], np.ndarray]:
    """Extracts values of GeoTiff file in numpy array

    Arguments:
        image_path -- A path to a directory that contains one `.tiff` file for every band of the image

    Returns:
        A tuple of the names of the bands and the image matrix with shape (height, width, bands)
    """

    name_bands: List[str] = []
    value_bands: List[np.ndarray] = []

    for filename in os.listdir(image_path):
        if filename.endswith(".tif"):
            # Assumes that band file is in format name.bandname.tif
            name_bands.append(filename.split(".")[1])
            with rio.open(os.path.join(image_path, filename)) as tiff_file:
                # Assumes that tiff_file has only one band
                value_bands.append(tiff_file.read(1))

    # TODO: #1 add interpolation of bands with higher resolution

    # We also assume that the bands have the same resolution
    image_matrix = np.array(value_bands)
    # We roll around the axes so that bands are last
    image_matrix = np.rollaxis(image_matrix, 0, 3)
    return name_bands, image_matrix


def minmax_scaling(image: np.ndarray, bands_first: bool = False) -> np.ndarray:
    """Performs min-max scaling of an input image, resulting with values in the range [0, 1]

    Arguments:
        image -- The input image, a np.ndarray with shape (height, width, bands), unless
        `bands_first = True`

    Keyword Arguments:
        bands_first -- If True, input image has shape (bands, height, width) (default: {False})

    Returns:
        The input image with the same format scaled in the range [0, 1]
    """
    if bands_first:
        image = np.rollaxis(image, 0, 3)

    _, _, n_bands = image.shape

    min_band = image.min()
    max_band = image.max()
    if max_band == min_band:
        image = 0
    else:
        image = (image - min_band) / (max_band - min_band)

    if bands_first:
        image = np.rollaxis(image, 2, 0)

    return image
