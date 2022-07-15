import fitz
import os


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


def checkInputPDF(PDF_Filename):
    global file_handle
    file_handle = fitz.open(PDF_Filename)
    haveHeader = False
    startLogDepth = ''
    for pageI in file_handle:
        pIdx = pageI.number
        page = file_handle[pIdx]
        t = page.get_text()
        if pIdx == 0:
            if 'UWID: ' in t.splitlines():
                haveHeader = True
            for i in t.splitlines():
                if 'Logging From'.lower() in i.lower():
                    m = [x for x in i.split() if x.isnumeric()]
                    startLogDepth = m[0]
    return [haveHeader, startLogDepth]


def createPDF_TIF(browseFolderName, startDepth, filesList, haveHeader):
    output_file = f"{file_handle.metadata['title']}_Output.pdf"
    startLogDepth = int(startDepth)
    cumDept = startLogDepth
    depthPerPage = []
    depths = []
    PageIndexFactor = 2 if haveHeader else 0
    for idx, pageI in enumerate(file_handle):
        if idx >= PageIndexFactor:
            pIdx = pageI.number
            page = file_handle[pIdx]
            t = page.get_text()
            chunk = t.splitlines()[0:3]
            check = [i.isnumeric() for i in chunk]
            haveText = 2 if False in check else 3
            addVal = 117 if haveText == 2 else 116
            fromDepth = cumDept
            toDepth = fromDepth+117
            data = {
                'pageNo': pIdx,
                'from': fromDepth,
                'to': toDepth,
                'addVal': addVal
            }
            # if fromDepth < ((len(filesList)/2)*20)+startLogDepth:
            depthPerPage.append(data)
            cumDept += addVal

    imgsDepths = []
    for i in depthPerPage:
        cumDepth = i['from']
        for x in range(6):
            tDep = cumDepth
            bDep = (cumDepth+20)-((cumDepth % 20) % 10)
            if bDep-tDep < 20:
                cumDepth -= (10-(bDep-tDep))
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
            for idx, file_name in enumerate(filesList):
                oTs = file_name.split('_')[4]
                if v == int(oTs):
                    imgList.append(file_name)
        pageData['imgs'] = imgList
        imgList = []

    for idx, pageData in enumerate(depthPerPage):
        pIdx = pageData['pageNo']
        page = file_handle[pIdx]
        top = 0
        btm = 0
        for idx, file_name in enumerate(pageData['imgs']):
            final_file_name = removeLeadingZero(file_name)
            tif_file = f'{browseFolderName}\\{final_file_name}'
            top = (pageData['depths'][idx]-pageData['from'])*4.31
            btm += (pageData['depths'][idx+1]-pageData['depths'][idx])*4.31
            image_rectangle = fitz.Rect(top, 139.98, btm, 245.42)
            page.insert_image(image_rectangle, filename=tif_file,
                              rotate=90, keep_proportion=False)

    file_handle.save(output_file)

    os.startfile(output_file)
