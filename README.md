# Image labeling tool
Finds label clusters in binary image and writes a label text to the corresponding position on an overlay image of labels and microscopy data

## Input
- Binary label image
- Overlay image to be labeled
- Output filename
- Label text (if not supplied 'ID' will be used)

## Output
- Image with text labels (e.g. 'ID 3' for binary label 3, and a label text of 'ID')

## Usage
### Example
`python3 main.py overlay_image.tif label_image.tif Output_image.tif ID` 