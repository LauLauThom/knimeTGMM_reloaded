# knimeTGMM_reloaded

Knime workflow to automate use of TGMM software for cell segmentation and lineage tracking.

Results can be viewed either in Knime or displayed better using MaMut plugin on FIJI.

The original TGMM repository contains the necessary software to run this workflow and an example dataset under `data>data`. You can find it at: https://git.rcc.uchicago.edu/open-source/TGMM .

The IDRdownloader python script in this repository can allow you to download additional datasets from the Image Data Resource database (https://idr.openmicroscopy.org/).

It is currently set to download an appropriate dataset from the Keller lab (source of the TGMM software) (https://idr.openmicroscopy.org/webclient/img_detail/4007801/?dataset=3351).

## Expected datasets

We recommend to use 3D datasets of at least 10 frames. Errors were observed using shorter datasets.

Timeframes have to be saved in separate `.tif` files, the filename of which should include the number of the frame.

During configuration, you will be asked to provide the location of the files with the timepoint replaced by "?" and no extension (example: `frame0001.tif` -> frame????).

## Processing steps

This workflow includes the different functions:

- Segmentation of 3D images: Takes 3D tif images as input, outputs data in `.bin` files.
- Display of segmentation: Takes `.bin` files, outputs `.tif` files and allows visuaization in Knime by superposition on the original images.
- Tracking of cells: Takes `.bin` files, outputs tracking data in `.xml` files.
- Display of tracking: Takes `.xml` files, allows visualization of centroids superposed on the original images, with consistent lineage labels.

## Requirements

This workflow is only compatible with TGMM for Windows. TGMM requires a CUDA compatible GPU to function. It was tested to work on Knime 4.4.0.

The Knime extensions for Image Processing and External Tool compatiblity will be installed automatically by Knime upon opening the workflow.

## MaMut import

To import results in MaMut, all images need to be integrated into a hyperstack with the correct number of slices and frames in FIJI.

Then, the Big Data Viewer plugin can be used to export the stack to hdf5 + xml.

The `Import TGMM results into MaMut` submenu of MaMut takes the path to the `GMEMtracking3D_\XML_finalResult_lht` directory (created by TGMM in your results folder) and the XML created by Big Data Viewer.

It produces a new XML file, which is used by MaMut in the `Open MaMut annotation` submenu and directly provides access to the different viewers provided by MaMut.
