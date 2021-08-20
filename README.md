# knimeTGMM_reloaded

Knime workflow to automate the use of Tracking by Gaussian Mixture Model (TGMM) for 3D cell segmentation and cell-lineage tracking in 3D+time image-sequences.  
TGMM was designed to work with dataset of cells with fluorescently labelled nuclei (ex: H2B-mCherry in developping drosophila embryos). 

Results can be viewed either in Knime or displayed better using MaMut plugin in FIJI.

The IDRdownloader python script in this repository can allow you to download additional datasets from the Image Data Resource database (https://idr.openmicroscopy.org/).  
It is currently set to download an appropriate dataset from the Keller lab (source of the TGMM software) (https://idr.openmicroscopy.org/webclient/img_detail/4007801/?dataset=3351).

# Requirements  
TGMM requires a GPU with CUDA support.  
This KNIME workflow is only compatible with TGMM for Windows, and was tested with Knime 4.4.0.  
The Knime extensions (Image Processing and External Tools) needed by the workflow will be installed automatically by Knime upon opening the workflow.

The original TGMM repository contains the necessary software to run this workflow (TGMM 1.0) as well as some documentation/user-guide and an example dataset under `data>data`.  
You can find it at: https://sourceforge.net/projects/tgmm/files/.  
TGMM 1.0 is also available at https://git.rcc.uchicago.edu/open-source/TGMM but this version was returning CUDA errors with out configuration.  
TGMM 2.0 is also available but not compiled. 
There is also some documentation in the doc directory of this repo https://bitbucket.org/fernandoamat/tgmm-paper/src/master/.  


# Expected datasets

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

# Processing steps

This workflow includes the different functions:

### __Hierarchical segmentation of 3D images into supervoxels__  
This is performed by the node "Pyramidal Segmentation Hierarchy".  

This first step includes:
 - reducing noise in images using median filter (use CUDA)
 - identification of foreground regions using the "background threshold" parameter
 - watershed
 - Persistence Based Clustering (PCB), creating the hierarchy of segmentation levels

The node is internally calling `ProcessStackBatchMultiCore.exe <TGMMconfig.txt> <firstTimepoint> <lastTimepoint>`.   
The config file is automatically generated from the parameters provided in the GUI of the node (refer to the mouse-over description of the GUI elements and/or to the TGMM user-guide for a more detailed description of the parameters).    
This command actually parallelizes `ProcessStack.exe <TGMMconfig.txt> <image>` called with individual Z-stacks of timepoints (the `<image>`), and using as many CPU cores as available (ie timepoints are processed in parallel).   

The output is a hierarchical segmentations for each timepoint, saved as `.bin` files in the image directory.      
These bin files can be used to derive different segmentations, by choosing a cut-off (Tau), ie to a Tau value corresponds one segmentation level.     
By selecting a Tau, the hierarchical segmentation is "cut" to a given level, yielding a first set of supervoxel (next workflow).  

Note: ProcessStack can also be called to generate such bin file for single timepoints Z-stacks by calling  
`ProcessStack.exe <image> <radiusMedianFilter> <minTau> <backgroundThr> <conn3D>`

### __Visualization of the segmentation for a given Tau__  
This is calling `ProcessStack.exe <binFile> <Tau> <minSuperVoxelSize>`.  
This allows to visualize the resulting segmentation for a given Tau and minimum nuclei size (also called supervoxel size).  
It takes the `.bin` files generated at the previous step, and outputs segmentation mask as `.tif` files in the image directory.     
The masks are then loaded in Knime and can be viewed overlaid on the original images.   
From the original publication "The higher the value of Tau, the coarser the segmentation, as more image regions are merged."  

### __Tracking of cells__  
This is calling `TGMM.exe <TGMMconfig.txt> <firstTime> <lastTime>`.  
It performs the following steps:
- from the `.bin` files containing the hierarchical segmentation, derive a segmentation corresponding to the selected Tau
- remove supervoxels below `minNucleiSize` 
- apply Otsu thresholding followed by filtering with `maxNucleiSize` 
- Fit gaussians on the supervoxels/nuclei (the Gaussian Mixture Model)
- Establish cell tracks and lineage based on the gaussian fit

The output is a set of XML file (one per timepoint).  
The XML contains the coordinates of the gaussian fitted on the nuclei, as well as track/lineage information.  
The XML files can be loaded in Fiji using MaMut to view the nuclei rendered from the gaussian fits and their tracks.  

### __Display of localized nuclei__  
Takes `.xml` files, allows visualization of centroids overlaid on the original images.  
The color of the centroid labeling is determined by the index of the cell lineage (ie cells from the same lineage have the same labeling color).  


## MaMut import

To import results in MaMut, all images need to be integrated into a hyperstack with the correct number of slices and frames in FIJI.

Then, the Big Data Viewer plugin can be used to export the stack to hdf5 + xml.

The `Import TGMM results into MaMut` submenu of MaMut takes the path to the `GMEMtracking3D_\XML_finalResult_lht` directory (created by TGMM in your results folder) and the XML created by Big Data Viewer.

It produces a new XML file, which is used by MaMut in the `Open MaMut annotation` submenu and directly provides access to the different viewers provided by MaMut.
