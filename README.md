# knimeTGMM_reloaded

Knime workflow to automate use of TGMM software for cell segmentation and lineage tracking.

Results can be viewed either in Knime or displayed better using MaMut plugin on FIJI.

### MaMut import

To import results in MaMut, all images need to be integrated into a hyperstack with the correct number of slices and frames in FIJI.

Then, the Big Data Viewer plugin can be used to export the stack to hdf5 + xml.

The `Import TGMM results into MaMut` submenu of MaMut takes the path to the `GMEMtracking3D_\XML_finalResult_lht` directory (created by TGMM in your results folder) and the XML created by Big Data Viewer.

It produces a new XML file, which is used by MaMut in the `Open MaMut annotation` submenu and directly provides access to the different viewers provided by MaMut.
