# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 14:07:46 2021

@author: Pierre

Credit to Robert Haase (MPI CBG Dresden) for code   
"""

from idr import connection
import numpy
from skimage.io import imsave

conn = connection('idr.openmicroscopy.org')

# adapted from https://github.com/ome/omero-guide-ilastik/blob/e9df8014515a8dbbfd87623a24564044d05d2224/notebooks/pixel_classification.ipynb
def load_numpy_array(image, timestart, timestop, channels, slicestart, slicestop, step):
    pixels = image.getPrimaryPixels()
#    size_z = image.getSizeZ()
#    size_c = image.getSizeC()
#    size_t = image.getSizeT()
    size_y = image.getSizeY()
    size_x = image.getSizeX()
    z, t, c = 0, 0, 0  # first plane of the image

    zct_list = []
    for t in range(timestart, timestop):
        for z in range(slicestart, slicestop, step):  # get the Z-stack
            for c in range(channels):  # all channels
                zct_list.append((z, c, t))

    print(zct_list)
    values = []
    # Load all the planes as YX numpy array
    planes = pixels.getPlanes(zct_list)
    j = 0
    k = 0
    tmp_c = []
    tmp_z = []
    s = "z:%s t:%s c:%s y:%s x:%s" % (int((slicestop-slicestart)/step), timestop-timestart, channels, size_y, size_x)
    print(s)
    # axis tzyxc
    lenPlanes = int((slicestop-slicestart)/step) * (timestop-timestart) * channels
    print("Downloading image %s" % image.getName())
    for i, p in enumerate(planes):
        if k < int((slicestop-slicestart)/step):
            if j < channels:
                tmp_c.append(p)
                j = j + 1
            if j == channels:
                # use dstack to have c at the end
                tmp_z.append(numpy.dstack(tmp_c))
                tmp_c = []
                j = 0
                k = k + 1
        if k == int((slicestop-slicestart)/step):  # done with the stack
            values.append(numpy.stack(tmp_z))
            tmp_z = []
            k = 0
        print("Loaded plane {} out of {}".format(i, lenPlanes))

    return numpy.stack(values)

def retrieve_image(conn, dataset_id, image_id, timestart, timestop, channels, slicestart, slicestop, step=1):
    input_data = None

    images = conn.getObjects('Image', opts={'dataset': dataset_id, 'image':image_id})

    for image in images:
        if image.getId() == image_id:
            input_data = load_numpy_array(image, timestart, timestop, channels, slicestart, slicestop, step)
    return input_data

# see: https://idr.openmicroscopy.org/webclient/?show=image-9844380
dataset_id = 3351
image_id = 4007801

input_data = retrieve_image(conn, dataset_id, image_id, 140, 160, 1, 400, 441, 8)

print(input_data.shape)
imsave('test.tif', input_data)