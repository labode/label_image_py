# Image labeling tool
Finds label clusters in binary image and writes a label text to the corresponding position on an overlay image of labels and microscopy data

## Requirements
Required packages are listed in requirements.txt and can be installed using pip as follows:\
`pip3 install -r requirements.txt`

## Input
- Binary label image
- Overlay image to be labeled
- Output filename
- Scale factor (if not supplied, 1 (i.e. no scaling) will be used)
- Label text (if not supplied, 'ID' will be used)

## Output
- Image with text labels (e.g. 'ID 3' for binary label 3, and a label text of 'ID')

## Usage
### Example
`python3 label_image.py overlay_image.tif label_image.tif Output_image.tif 2 ID`
### Note
The scaling will not change the output image size, but will make the program analyze the label data on a downscaled image. This will reduce computation time, but if the scaling factor is too large, labels might get lost. 
