from PIL import Image
import os
import shutil

def crop_all(path, columns, rows):
    dirlist = [item for item in os.listdir(path) if item.endswith(('.jpeg', '.jpg', '.png'))]
    for item in dirlist:
        crop_image(path, item, columns = columns, rows = rows)

def crop_image(path: str, filename: str, columns: int, rows: int, move_directory: str = None):
    """Function which crops an image and saves it in a directory. If move_directory is specified, the
    original picture will be moved there.

    Args:
    
        path (str): Path where the original picture is located and the cropped one will be saved
        filename (str): Filename of the original picture
        columns (int): number of columns that the picture will be split into
        rows (int): number of rows that the picture will be split into
        move_directory (str, optional): Directory were the original pictures will be moved. Defaults to None.
    """

    name = filename.split('.')[0]
    extension = filename.split('.')[1]

    im = Image.open(os.path.join(path, filename))

    width, height = im.size

    for col in range(columns):
        for row in range(rows, 0, -1):

            left = width / columns * col
            bottom = height / rows * (row - 1)
            right = width / columns * (col + 1)
            top = height / rows * row

            spl = im.crop((left, bottom, right, top))

            col_ext = f"-{col+1}" if columns > 1 else ''
            row_ext = f"-{row}" if rows > 1 else ''
            new_filename = f"{name}{col_ext}{row_ext}.{extension}"
            save_loc = os.path.join(path, new_filename)
            spl.save(save_loc)

    if move_directory:
        os.makedirs(f"{move_directory}", exist_ok=True)
        shutil.move(f"{path}/{filename}", f"{move_directory}/{filename}")

if __name__=='__main__':
    filename = '626063 2.jpg'
    path = os.path.expanduser('~/Downloads')
    columns = 2
    rows = 1
    crop_image(path, filename, columns, rows)