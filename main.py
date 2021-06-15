import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont


# Resources:
# https://note.nkmk.me/en/python-numpy-image-processing/


def read_image(filename):
    image = np.array(Image.open(filename), np.int16)

    return image


# This is not pretty and definitely takes some time to complete... but me no smrt :(
def find_labels(img_array):
    # TODO: Using the ol image is bullshit! we need to make seg_art_gen@zxx.tif (NOT! _th) images
    #  and can then take the label directly from them! (rule is already in MF, only need to add it as prereq)

    labels = []

    size = img_array.shape

    x = 0
    while x < size[0]:
        percent = round(x / (size[0] / 100), 2)
        print(str(percent) + '% done')

        y = 0
        while y < size[1]:
            # If the pixel does not have a value of 0 (background), we have found a label and can add it to our map
            if image_array[x, y] != 0:
                entry = [x, y, image_array[x, y]]
                labels.append(entry)

            y += 1

        x += 1

    return labels


def find_clusters(label_map, img_array):
    clusters = []

    while len(label_map) > 0:
        # Create empty cluster
        cluster = []
        search = []
        # Take first pixel
        start_px = label_map[0]
        cluster.append(start_px)
        search.append(start_px)
        label_map.remove(start_px)

        while len(search) > 0:
            neighbors = find_neighbours(label_map, img_array, search[0])
            search.remove(search[0])
            for i in neighbors:
                if i not in cluster:
                    cluster.append(i)
                if i not in search:
                    search.append(i)
                label_map.remove(i)

        clusters.append(cluster)

    return clusters


def find_neighbours(label_map, img_array, position):
    # Definition neighbour: bordering pixel with the same label as the original pixel
    neighbours = []

    # for each pixel there are a max of eight bordering pixels
    x_values = [position[0]]
    y_values = [position[1]]

    size = img_array.shape

    if position[0] - 1 >= 0:
        x_values.append(position[0] - 1)
    if position[0] + 1 < size[0]:
        x_values.append(position[0] + 1)
    if position[1] - 1 >= 0:
        y_values.append(position[1] - 1)
    if position[1] + 1 < size[1]:
        y_values.append(position[1] + 1)

    # => Check if pixels at these positions are in the map with a matching label
    for x_value in x_values:
        for y_value in y_values:
            px = [x_value, y_value, position[2]]
            # No need to check our input pixel again
            if px == position:
                continue
            if px in label_map:
                neighbours.append(px)

    return neighbours


def find_centers(cluster_map):
    # Center = [x, y, label]
    cluster_centers = []
    for cluster in cluster_map:
        x_range = []
        y_range = []
        for pixel in cluster:
            x_range.append(pixel[0])
            y_range.append(pixel[1])

        x_min = min(x_range)
        x_max = max(x_range)
        y_min = min(y_range)
        y_max = max(y_range)

        # TODO: The position might not be on the label (e.g. u-shaped vessel)
        #  => Check if position is on label?
        #  => What if not? Search closest label pixel?
        # y => centered, x => 10% from left edge, as we write left to right
        # TODO: Works but does not make any sense...
        center = [int(round((x_max - x_min) / 2, 0) + x_min),
                  int(round((y_max - y_min) / 20, 0) + y_min), cluster[0][2]]
        cluster_centers.append(center)

    return cluster_centers


def write_image(center_map, input_file, output_file):
    # https://www.tutorialspoint.com/python_pillow/python_pillow_writing_text_on_image.htm
    # open image
    image = Image.open(input_file)
    # define settings
    draw = ImageDraw.Draw(image)
    # TODO: Fine tune font size and type?
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf', 7)
    # for each center write label
    for center in center_map:
        draw.text((center[1], center[0]), "ID " + str(center[2]), font=font, fill=(255, 255, 255))

    # write image
    image.save(output_file)


if __name__ == '__main__':
    # Arguments need to be supplied from command line to use this in a makefile
    input_image = sys.argv[1]  # 'overlay.tif'
    label_image = sys.argv[2]  # 'labels.tif'
    output_image = sys.argv[3]  # 'output.tif'

    error = False

    if not input_image or not label_image or not output_image:
        print("Missing parameters")
        # Explain the needed parameters to the user
        print("Please supply: input image, overlay image, output image")
        error = True

    if not error:
        print('Reading image')
        image_array = read_image(label_image)
        print('Looking for labels')
        label_positions = find_labels(image_array)
        # print(label_positions)
        print('Performing cluster analysis')
        cluster_pixels = find_clusters(label_positions, image_array)
        # print(cluster_pixels)
        print('Calculating cluster centers')
        centers = find_centers(cluster_pixels)
        print(centers)
        print('Labeling image')
        write_image(centers, input_image, output_image)
        print('Finished')
