import fitz
import os
import shutil
from PIL import Image

from HelperFunc import resource_path


def addLeadingZero(file_name):
    oTs = file_name.split('_')
    oTs[3] = oTs[3].zfill(4)
    oTs[4] = oTs[4].zfill(4)
    final_file_name = '_'.join(oTs)
    return final_file_name


def removeLeadingZero(file_name):
    oTs = file_name.split('_')
    oTs[3] = oTs[3].lstrip('0')
    oTs[4] = oTs[4].lstrip('0')
    final_file_name = '_'.join(oTs)
    return final_file_name


def calculateStartDepth(t, d):
    chunk = t.splitlines()[0:3]
    check = [i.isnumeric() for i in chunk]
    depths = chunk[0:2] if False in check else chunk[0:3]
    firstDepth = int(depths[0])
    rectPerPage = []
    firstTickWidth = d[2]['rect'][1]
    for i, x in enumerate(d[2:14]):
        if x['rect'][1] != firstTickWidth:
            rectPerPage.append(
                x['rect'][0]
            )
    firstH = rectPerPage[0]/4.319362324859913
    start_depth = round(firstDepth - firstH)
    print(start_depth)
    return f'{start_depth}'


def checkInputPDF(PDF_Filename):
    global file_handle, picRectY0, picRectY1
    picRectY0 = 139.98
    picRectY1 = 245.42

    file_handle = fitz.open(PDF_Filename)
    haveHeader = False
    startLogDepth = ''
    fileList = list(file_handle)
    for pageI in fileList[0:3]:
        pIdx = pageI.number
        page = file_handle[pIdx]
        t = page.get_text()
        d = page.get_drawings()
        if pIdx == 0:
            if 'UWID: ' in t.splitlines():
                haveHeader = True
        if haveHeader:
            # if pIdx == 0:
            #     for i in t.splitlines():
            #         if 'Logging From'.lower() in i.lower():
            #             m = [x for x in i.split() if x.isnumeric()]
            #             startLogDepth = m[0]
            if pIdx == 2:
                startLogDepth = calculateStartDepth(t, d)
        else:
            return [haveHeader, startLogDepth]
            # if pIdx == 0:
            #     startLogDepth = calculateStartDepth(t, d)

        SecondPageRect = []
        if haveHeader and pIdx == 1:
            for i, x in enumerate(d):
                if x['closePath']:
                    SecondPageRect.append(x['rect'])
            picRect = SecondPageRect[9]
            picRectY0 = picRect[1]
            picRectY1 = picRect[3]
            print(picRect[1], picRect[3])

            # end = False
            # for i, x in enumerate(d):
            #     if x['rect'].y0 == picRectY0:
            #         k.append([
            #             pIdx+1,
            #             0 if x['rect'].x0 < 0 else x['rect'].x0,
            #             x['rect'].x1,
            #             x['rect'].y0,
            #             x['rect'].y1,
            #         ])
            #         end = False if x['rect'].x0 > 502 else True
            #         print(x['rect'].x0)
            # if end:
            #     k.append([pIdx+1, 503.940002441406])
    file_handle.close()
    return [haveHeader, startLogDepth]


def getRectPerPage(d):
    rectPerPage = []
    for i, x in enumerate(d[2:14]):
        if x['rect'][0] not in rectPerPage:
            if i == 0 and x['rect'][0] != 0:
                rectPerPage.append(0)
                rectPerPage.append(x['rect'][0])
            elif i == 11 and x['rect'][0] < 502 and len(rectPerPage) > 10:
                if x['rect'][0] > 0:
                    rectPerPage.append(x['rect'][0])
                    rectPerPage.append(503.940002441406)
                else:
                    rectPerPage.append(503.940002441406)
            else:
                if x['rect'][0] >= 0:
                    rectPerPage.append(x['rect'][0])
    return rectPerPage


def getTopBtm(pIdx):
    page = file_handled[pIdx]
    d = page.get_drawings()

    rectPerPage = getRectPerPage(d)

    if len(rectPerPage) == 13:
        indexes = [1, 3, 5, 7, 9, 11]
        for index in sorted(indexes, reverse=True):
            del rectPerPage[index]

    elif len(rectPerPage) == 14:
        indexes = [1, 2, 4, 6, 8, 10, 12]
        for index in sorted(indexes, reverse=True):
            del rectPerPage[index]

    elif pIdx == len(file_handled)-1:
        indexes = [1, 3, 5, 7, 9, 11]
        filtered = list(range(len(rectPerPage)))
        indexes = [i for i in indexes if i in filtered]
        for index in sorted(indexes, reverse=True):
            del rectPerPage[index]
    return rectPerPage


def createPDF_TIF(PDF_Filename, browseFolderName, startDepth, filesList, haveHeader):
    global file_handled
    copiedPDF_Filename = resource_path('input.pdf')
    shutil.copy(PDF_Filename, copiedPDF_Filename)
    file_handled = fitz.open(copiedPDF_Filename)
    output_file = f"{file_handled.metadata['title']}_Output.pdf"
    startLogDepth = int(startDepth)
    cumDept = startLogDepth
    depthPerPage = []
    depths = []
    PageIndexFactor = 2 if haveHeader else 0
    for idx, pageI in enumerate(file_handled):
        if idx >= PageIndexFactor:
            pIdx = pageI.number
            page = file_handled[pIdx]
            heights = getTopBtm(pIdx)
            addVal = (heights[len(heights)-1])/4.319362324859913
            fromDepth = round(cumDept)
            toDepth = round(cumDept+addVal)
            data = {
                'pageNo': pIdx,
                'from': fromDepth,
                'to': toDepth,
                'heights': heights
            }
            # if fromDepth < ((len(filesList)/2)*20)+startLogDepth:
            depthPerPage.append(data)
            cumDept += addVal

    imgsDepths = []
    for i in depthPerPage:
        hRange = len(i['heights'])-1
        cumDepth = i['from']
        for x in range(hRange):
            tDep = cumDepth
            bDep = (cumDepth+20)-((cumDepth % 20) % 10)
            if bDep-tDep < 15:
                cumDepth -= (10-(bDep-tDep))
            elif bDep-tDep > 15 and bDep-tDep < 20:
                cumDepth -= (20-(bDep-tDep))
            cumDepth += 20
            depths.append(tDep)
            if tDep != i['from']:
                imgsDepths.append(tDep)

        depths.append(i['to'])
        tDepImg = i['to'] if i['to'] % 10 == 0 else (i['to']-(i['to'] % 10)+10)
        imgsDepths.append(tDepImg)
        i['depths'] = depths
        i['imgs_depths'] = imgsDepths
        depths = []
        imgsDepths = []

    imgList = []
    for idx, pageData in enumerate(depthPerPage):
        for i, v in enumerate(pageData['imgs_depths']):
            file_name_img = ''
            for idx, file_name in enumerate(filesList):
                oTs = file_name.split('_')[4]
                if v == int(oTs):
                    file_name_img = file_name
            imgList.append(file_name_img)
        pageData['imgs'] = imgList
        imgList = []

    # import pandas as pd
    # df = pd.DataFrame(depthPerPage)
    # df.to_excel('depthPerPage.xlsx')
    # os.startfile('depthPerPage.xlsx')

    for idx, pageData in enumerate(depthPerPage):
        pIdx = pageData['pageNo']
        page = file_handled[pIdx]
        tempPath = resource_path('temp')
        if os.path.exists(tempPath):
            shutil.rmtree(tempPath)
        os.mkdir(tempPath)
        for idx, file_name in enumerate(pageData['imgs']):
            if file_name != '':
                top = pageData['heights'][idx]
                btm = pageData['heights'][idx+1]
                final_file_name = removeLeadingZero(file_name)
                tif_file = f'{browseFolderName}\\{final_file_name}'
                my_image = Image.open(tif_file)
                imgSize = my_image.size
                imgXw = imgSize[0]
                if imgXw > 800:
                    my_image.thumbnail((800, 600), Image.ANTIALIAS)
                pathOnly, file_extension = os.path.splitext(file_name)
                jpgPath = f'{tempPath}\\{pathOnly}.jpg'
                my_image.save(jpgPath)
                image_rectangle = fitz.Rect(top, picRectY0, btm, picRectY1)
                page.insert_image(image_rectangle, filename=jpgPath,
                                  rotate=90, keep_proportion=False)
        if os.path.exists(tempPath):
            shutil.rmtree(tempPath)

    file_handled.save(output_file)
    file_handled.close()
    os.remove(copiedPDF_Filename)

    os.startfile(output_file)
