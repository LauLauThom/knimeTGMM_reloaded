# knimeTGMM_reloaded

Knime workflow to automate use of TGMM software for cell segmentation and lineage tracking.

Results can be viewed either in Knime or displayed better using MaMut plugin on FIJI.

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

### MaMut import

To import results in MaMut, all images need to be integrated into a hyperstack with the correct number of slices and frames in FIJI.

Then, the Big Data Viewer plugin can be used to export the stack to hdf5 + xml.

The `Import TGMM results into MaMut` submenu of MaMut takes the path to the `GMEMtracking3D_\XML_finalResult_lht` directory (created by TGMM in your results folder) and the XML created by Big Data Viewer.

It produces a new XML file, which is used by MaMut in the `Open MaMut annotation` submenu and directly provides access to the different viewers provided by MaMut.
