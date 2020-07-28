import os
from PIL import Image


# the grid of the maze
# each cell of the maze is one of the following:
# '#' is wall
# '.' is empty space


def rgb(tile_sign):
    if tile_sign == '#':
        return 118, 165, 204
    if tile_sign == '.':
        return 74, 103, 127
    if tile_sign == '-':
        return 224, 231, 255
    if tile_sign == 'P':
        return 204, 102, 0
    if tile_sign == 'D':
        return 128, 128, 128
    return 0, 0, 0


def create_preview(mappath, width, height, zoom=1):
    im = None
    img_data = []
    im = Image.new('RGB', (width * 50, height * 50))

    with open(mappath, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = list(line.strip('\n'))
            for j in range(zoom):
                colors = []
                for character in line:
                    for i in range(zoom):
                        colors.append(rgb(character))
                img_data = img_data + colors

    im.putdata(img_data)
    # im = im.resize((int(width * zoom), int(height * zoom)), Image.ANTIALIAS)

    head, ext = os.path.splitext(mappath)
    new_img_path = '{}{}'.format(head, '.png')
    im.save(new_img_path)


create_preview('../maps/obstacle_lane/empty.map', 16, 5, 50)
