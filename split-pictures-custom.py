from PIL import Image
import numpy as np
import os
import shutil

def crop_all(path, col_withds, row_heights, move_directory=None):
    dirlist = [item for item in os.listdir(path) if item.endswith(('.jpeg', '.jpg', '.png'))]

    for item in dirlist:
        crop_image(path, item, col_widths=col_widths, row_heights=row_heights)

# Main function
def crop_image(path: str, filename: str, col_widths: tuple, row_heights: tuple, move_directory: str = None):
    """Function which crops an image and saves it in a directory. If move_directory is specified, the
    original picture will be moved there.

    Args:
    
        path (str): Path where the original picture is located and the cropped one will be saved
        filename (str): Filename of the original picture
        col_widths (tuple): tuple containing the widths of the columns
        row_heights (tuple): tuple containing the heights of the rows
        move_directory (str, optional): Directory were the original pictures will be moved. Defaults to None.
    """

    name = filename.split('.')[0]
    extension = filename.split('.')[1]

    im = Image.open(os.path.join(path, filename))

    width, height = im.size

    col_end = np.atleast_2d(np.cumsum(col_widths)).transpose()
    width_scaling = width / col_end.max()

    col_start = np.roll(col_end, 1)
    col_start[0, 0] = 0

    row_end = np.atleast_2d(np.cumsum(row_heights)).transpose()
    height_scaling = height / row_end.max()

    row_start = np.roll(row_end, 1)
    row_start[0, 0] = 0

    scaling = min(width_scaling, height_scaling)
    cols = np.concatenate((col_start, col_end), axis=1) * scaling
    rows = np.concatenate((row_start, row_end), axis=1) * scaling


    for i in range(len(rows)):
        row = rows[i]
        for j in range(len(cols)):
            col = cols[j]

            left = col[0]
            bottom = row[0]
            right = col[1]
            top = row[1]

            spl = im.crop((left, bottom, right, top))

            row_ext = f"-{i+1}" if len(rows) > 1 else ''
            col_ext = f"-{j+1}" if len(cols) > 1 else ''
            new_filename = f"{name}{col_ext}{row_ext}.{extension}"
            save_loc = os.path.join(path, new_filename)
            spl.save(save_loc)

        if move_directory:
            os.makedirs(f"{move_directory}", exist_ok=True)
            shutil.move(f"{path}{filename}", f"{move_directory}{filename}")

if __name__=='__main__':
    # Specify column and row sizes
    col_widths = (2560, 130, 2560)
    row_heights = (1440)

    # Specify file paths
    filename  = "christmas-london.jpg"
    path = os.path.expanduser('~/Downloads/')
    crop_image(path, filename, col_widths, row_heights)