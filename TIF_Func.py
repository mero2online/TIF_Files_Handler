from PIL import Image, ImageFont, ImageDraw
import os

from HelperFunc import resource_path


def listAllFiles(browseFolderName):
    tifList = []
    src_files = os.listdir(browseFolderName)
    for file_name in src_files:
        pathOnly, file_extension = os.path.splitext(file_name)
        if os.path.isfile(f'{browseFolderName}\\{file_name}') and file_extension == '.tif':
            tifList.append(file_name)
    return tifList


def addLabelsForTIF(browseFolderName):
    dest_dir = 'Labeled_TIF'
    if os.path.exists(dest_dir) == False:
        os.mkdir(dest_dir)

    tifList = listAllFiles(browseFolderName)
    for file_name in tifList:
        my_image = Image.open(f'{browseFolderName}\\{file_name}')

        imgSize = my_image.size

        imgXw = imgSize[0]
        imgYh = imgSize[1]

        title_font = ImageFont.truetype(
            resource_path('arial.ttf'), int(imgXw/30))

        title_text = ["Zoom/Magnification: 0.8X", "_____", "2mm"]
        title_text_pos = [(imgXw*0.01, imgYh*0.93), (imgXw*0.89,
                                                     imgYh*0.88), (imgXw*0.9, imgYh*0.93)]

        image_editable = ImageDraw.Draw(my_image)

        for idx, v in enumerate(title_text):
            image_editable.text(title_text_pos[idx],
                                title_text[idx], fill="#000", font=title_font)

        my_image.save(f'{dest_dir}\\{file_name}')


def resizeAllTIF(browseFolderName):
    dest_dir = 'Resized_TIF'
    if os.path.exists(dest_dir) == False:
        os.mkdir(dest_dir)

    tifList = listAllFiles(browseFolderName)
    # h = len(tifList)*600
    # img = Image.new("RGB", (800, h), "white")
    for idx, file_name in enumerate(tifList):
        my_image = Image.open(f'{browseFolderName}\\{file_name}')
        my_image.thumbnail((800, 600), Image.ANTIALIAS)
        my_image.save(f'{dest_dir}\\{file_name}')
        # img.paste(my_image, (0, idx*600))
    # img.save(f'{dest_dir}\\0img.tif')
