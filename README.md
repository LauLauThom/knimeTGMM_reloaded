# knimeTGMM_reloaded

Knime workflow to automate the use of Tracking by Gaussian Mixture Model (TGMM) for 3D cell segmentation and cell-lineage tracking in 3D+time image-sequences.  
TGMM was designed to work with dataset of cells with fluorescently labelled nuclei (ex: H2B-mCherry in developping drosophila embryos). 

Results can be viewed either in Knime or displayed better using MaMut plugin in FIJI.

The IDRdownloader python script in this repository can allow you to download additional datasets from the Image Data Resource database (https://idr.openmicroscopy.org/).  
It is currently set to download an appropriate dataset from the Keller lab (source of the TGMM software) (https://idr.openmicroscopy.org/webclient/img_detail/4007801/?dataset=3351).

## Requirements  
TGMM requires a GPU with CUDA support.  
This KNIME workflow is only compatible with TGMM for Windows, and was tested with Knime 4.4.0.  
The Knime extensions (Image Processing and External Tools) needed by the workflow will be installed automatically by Knime upon opening the workflow.


The original TGMM repository contains the necessary software to run this workflow (TGMM 1.0) and an example dataset under `data>data`.  
You can find it at: https://sourceforge.net/projects/tgmm/files/.  
TGMM 1.0 is also available at https://git.rcc.uchicago.edu/open-source/TGMM but this version was returning CUDA errors with out configuration.  
TGMM 2.0 is also available but not compiled. 
There is also some documentation in the doc directory of this repo https://bitbucket.org/fernandoamat/tgmm-paper/src/master/.  


## Expected datasets

We recommend to use 3D datasets of at least 10 frames. Errors were observed using shorter datasets.  
Z-stack for each timepoints have to be saved in separate `.tif` files.  
Additionally, the filename should contain the timepoint, and filenames shoud be identical (except the timepoint) between the images. 
The reason is that the image location is provided to the workflow (ad to TGMM), as a wildcard pattern for the filepath, with ??? in-place of the timepoints, and no extension.  
Example to match the following images: 
```
myPath/frame0001.tif
myPath/frame0002.tif
``` 
One should use the pattern
`myPath/frame????` with 4 `?` since all frames have a timepoint encoded as a 4-digit value.  

## Processing steps

This workflow includes the different functions:

- Hierarchical segmentation of 3D images: Takes 3D tif images as input, outputs data in `.bin` files.
- Display of segmentation: Takes `.bin` files, outputs `.tif` files and allows visuaization in Knime by superposition on the original images.
- Tracking of cells: Takes `.bin` files, outputs tracking data in `.xml` files.
- Display of tracking: Takes `.xml` files, allows visualization of centroids superposed on the original images, with consistent lineage labels.


## MaMut import

To import results in MaMut, all images need to be integrated into a hyperstack with the correct number of slices and frames in FIJI.

Then, the Big Data Viewer plugin can be used to export the stack to hdf5 + xml.

The `Import TGMM results into MaMut` submenu of MaMut takes the path to the `GMEMtracking3D_\XML_finalResult_lht` directory (created by TGMM in your results folder) and the XML created by Big Data Viewer.

It produces a new XML file, which is used by MaMut in the `Open MaMut annotation` submenu and directly provides access to the different viewers provided by MaMut.
