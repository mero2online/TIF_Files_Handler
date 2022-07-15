from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import os

from HelperFunc import getTimeNowText, readLocalFile, resource_path, writeLocalFile
from TIF_Func import addLabelsForTIF, listAllFiles, resizeAllTIF
from TIF_PDF_Func import checkInputPDF, createPDF_TIF
from settings import appVersionNo

try:
    import pyi_splash  # type: ignore
    pyi_splash.close()
except:
    pass


def getCSVData():
    text = readLocalFile(f'TIF_Files_Handler_Config.csv')

    result = []

    for line in text.splitlines():
        result.append(line.split(",")[1])

    return result


def browseFolder():
    global browseFolderName
    browseFolderName = filedialog.askdirectory()
    if browseFolderName:
        if browsWindowName == 'showAddLabel':
            addLabelBtn.config(state=NORMAL)
        elif browsWindowName == 'showResizeImage':
            resizeImageBtn.config(state=NORMAL)
        elif browsWindowName == 'showCreatePDF':
            global filesList
            filesList = listAllFiles(browseFolderName)
            if len(filesList) == 0:
                messagebox.showerror(
                    'Folder error', 'This folder not contains any TIF files,\nPlease select another folder')
            else:
                saveStatusVar.set(
                    f'Folder contains: {len(filesList)} TIF files')
                browsePDFBtn.config(state=NORMAL)


def browsePDF():
    global PDF_Filename
    PDF_Filename = filedialog.askopenfilename(
        title='Select a file...',
        filetypes=(('PDF files', '*.pdf'),
                   ('All files', '*.*')))
    startDepth.set('')
    if PDF_Filename:
        global haveHeader
        haveHeader, startLogDepth = checkInputPDF(PDF_Filename)
        if haveHeader:
            if startLogDepth:
                startDepth.set(startLogDepth)
                CreatePDFBtn.config(state=NORMAL)
        startDepthEntry.config(state=NORMAL)
        CreatePDFBtn.config(state=NORMAL)
        folderName.set(PDF_Filename)


def saveConfig():
    parameters = ['Well Name', 'From', 'To']
    values = [wellName.get(), fromDep.get(), toDep.get()]

    arr = []
    for idx, x in enumerate(parameters):
        arr.append(f'{x},{values[idx]}')

    txt = '\n'.join(arr)
    writeLocalFile(f'TIF_Files_Handler_Config.csv', txt)
    saveStatusVar.set('New config saved successfully')


def getFilesNames(fromDepth, toDepth):
    depthRange = int((toDepth-fromDepth)/10)
    result = []
    for idx in range(depthRange):
        fromD = fromDepth+((idx)*10)
        toD = fromD+10
        result.append(f'{wellName.get()}_{fromD}_{toD}_cutting_0.8X_WL_1.tif')

    return result


def createFiles():
    fromDepth = int(fromDep.get())
    toDepth = int(toDep.get())
    filesNames = getFilesNames(fromDepth, toDepth)
    timeNow = getTimeNowText()
    dirName = f'{fromDepth}-{toDepth}-{timeNow}'
    folderName.set(f'Folder [{dirName}] created successfully')
    os.mkdir(dirName)
    for i in filesNames:
        writeLocalFile(f'{dirName}\{i}', '')
    saveConfig()


def addLabelsForImages():
    addLabelsForTIF(browseFolderName)


def resizeAllImages():
    resizeAllTIF(browseFolderName)


def createPDFPhoto():
    createPDF_TIF(browseFolderName, startDepth.get(), filesList, haveHeader)


def clearSaveStatusVar(*e):
    saveStatusVar.set('')
    folderName.set('')


def destroyCreateFiles():
    clearSaveStatusVar()
    try:
        toDestroy = myLabel+myEntry+[createFilesBtn]
        for e in toDestroy:
            e.destroy()
    except NameError:
        pass


def destroyAddLabel():
    clearSaveStatusVar()
    try:
        toDestroy = [browseFolderBtn, addLabelBtn]
        for e in toDestroy:
            e.destroy()
    except NameError:
        pass


def destroyResizeImage():
    clearSaveStatusVar()
    try:
        toDestroy = [browseFolderBtn, resizeImageBtn]
        for e in toDestroy:
            e.destroy()
    except NameError:
        pass


def destroyCreatePDF():
    clearSaveStatusVar()
    try:
        toDestroy = [browseFolderBtn, browsePDFBtn, CreatePDFBtn,
                     startDepthLabel, startDepthEntry]
        for e in toDestroy:
            e.destroy()
    except NameError:
        pass


def showCreateFiles():
    showCreateFilesBtn.config(state='disabled')
    showAddLabelBtn.config(state='normal')
    showResizeImageBtn.config(state='normal')
    showCreatePDFBtn.config(state='normal')
    clearSaveStatusVar()

    result = getCSVData() if os.path.exists(
        'TIF_Files_Handler_Config.csv') else ['', '', '']

    global wellName, fromDep, toDep  # Vars
    global myLabel, myEntry
    global folderName, createFilesBtn, saveStatus, currentFilePath

    myLabelName = ['Well Name', 'From Depth', 'To Depth']

    myVars = []
    myLabel = []
    myEntry = []
    for i in range(len(myLabelName)):
        label = Label(
            root, text=myLabelName[i], background='#15133C', foreground='#EC994B')
        xPlace = 100
        yPlace = (i*40)+55
        label.place(x=xPlace, y=yPlace, width=150, height=35)
        myLabel.append(label)

        var = StringVar(root, value=result[i])
        myVars.append(var)

        entry = Entry(root, textvariable=myVars[i],
                      background='#fff', borderwidth=2, relief="ridge", font=('Arial', 12, 'bold'))
        myEntry.append(entry)

        xPlace = 260
        entry.place(x=xPlace, y=yPlace, width=150, height=35)

        var.trace('w', clearSaveStatusVar)

    wellName, fromDep, toDep = myVars

    createFilesBtn = Button(root, text="Create Files", background='#15133C', foreground='#EC994B', borderwidth=2, relief="groove", padx=5, pady=5,
                            command=createFiles)
    createFilesBtn.place(x=197, y=175, width=120, height=35)
    resizeWindow(515, 290)
    destroyAddLabel()
    destroyResizeImage()
    destroyCreatePDF()


def showAddLabel():
    showAddLabelBtn.config(state='disabled')
    showCreateFilesBtn.config(state='normal')
    showResizeImageBtn.config(state='normal')
    showCreatePDFBtn.config(state='normal')

    resizeWindow(515, 205)
    destroyCreateFiles()
    destroyResizeImage()
    destroyCreatePDF()

    addBrowseButton('showAddLabel')

    global addLabelBtn
    addLabelBtn = Button(root, text="Label All Images", background='#15133C', foreground='#EC994B', borderwidth=2, relief="groove", padx=5, pady=5,
                         command=addLabelsForImages)
    addLabelBtn.place(x=197, y=95, width=120, height=35)
    addLabelBtn.config(state=DISABLED)


def showResizeImage():
    showResizeImageBtn.config(state='disabled')
    showCreateFilesBtn.config(state='normal')
    showAddLabelBtn.config(state='normal')
    showCreatePDFBtn.config(state='normal')

    resizeWindow(515, 205)
    destroyCreateFiles()
    destroyAddLabel()
    destroyCreatePDF()

    addBrowseButton('showResizeImage')

    global resizeImageBtn
    resizeImageBtn = Button(root, text="Resize All Images", background='#15133C', foreground='#EC994B', borderwidth=2, relief="groove", padx=5, pady=5,
                            command=resizeAllImages)
    resizeImageBtn.place(x=197, y=95, width=120, height=35)
    resizeImageBtn.config(state=DISABLED)


def showCreatePDF():
    showCreatePDFBtn.config(state='disabled')
    showResizeImageBtn.config(state='normal')
    showCreateFilesBtn.config(state='normal')
    showAddLabelBtn.config(state='normal')

    resizeWindow(515, 290)
    destroyCreateFiles()
    destroyAddLabel()
    destroyResizeImage()

    addBrowseButton('showCreatePDF')

    global browsePDFBtn, CreatePDFBtn, startDepthLabel, startDepthEntry, startDepth
    browsePDFBtn = Button(root, text="Browse PDF", background='#15133C', foreground='#EC994B', borderwidth=2, relief="groove", padx=5, pady=5,
                          command=browsePDF)

    startDepth = StringVar()
    startDepthLabel = Label(root, text='Start Depth',
                            background='#15133C', foreground='#EC994B')
    startDepthEntry = Entry(root, textvariable=startDepth,
                            background='#fff', borderwidth=2, relief="ridge", font=('Arial', 12, 'bold'))

    CreatePDFBtn = Button(root, text="Create PDF", background='#15133C', foreground='#EC994B', borderwidth=2, relief="groove", padx=5, pady=5,
                          command=createPDFPhoto)

    browsePDFBtn.place(x=197, y=95, width=120, height=35)
    startDepthLabel.place(x=100, y=135, width=150, height=35)
    startDepthEntry.place(x=260, y=135, width=150, height=35)
    CreatePDFBtn.place(x=197, y=175, width=120, height=35)

    browsePDFBtn.config(state=DISABLED)
    CreatePDFBtn.config(state=DISABLED)
    startDepthEntry.config(state=DISABLED)


def addBrowseButton(windowName):
    global browseFolderBtn, browsWindowName
    browsWindowName = windowName
    browseFolderBtn = Button(root, text="Browse Folder", background='#15133C', foreground='#EC994B', borderwidth=2, relief="groove", padx=5, pady=5,
                             command=browseFolder)
    browseFolderBtn.place(x=197, y=55, width=120, height=35)


def resizeWindow(rootWidth, rootHeight):
    root.geometry(f'{rootWidth}x{rootHeight}')
    placeMadeByAndVersionNo(rootWidth, rootHeight)


def placeMadeByAndVersionNo(rootWidth, rootHeight):
    if rootHeight > 80:
        saveStatus.place(x=65, y=rootHeight-70, width=390, height=20)
        currentFilePath.place(x=65, y=rootHeight-45, width=390, height=20)
    madeWithLoveBy.place(x=0, y=rootHeight-20, width=190, height=20)
    versionNo.place(x=rootWidth-60, y=rootHeight-20, width=60, height=20)

########""" GUI """########


root = Tk()
global saveStatusVar
saveStatusVar = StringVar(root, '')

showCreateFilesBtn = Button(root, text="Create Empty Files", background='#15133C', foreground='#EC994B', borderwidth=2, relief="groove", padx=5, pady=5,
                            command=showCreateFiles)

showAddLabelBtn = Button(root, text="Add label", background='#15133C', foreground='#EC994B', borderwidth=2, relief="groove", padx=5, pady=5,
                         command=showAddLabel)

showResizeImageBtn = Button(root, text="Resize Image", background='#15133C', foreground='#EC994B', borderwidth=2, relief="groove", padx=5, pady=5,
                            command=showResizeImage)

showCreatePDFBtn = Button(root, text="Create PDF", background='#15133C', foreground='#EC994B', borderwidth=2, relief="groove", padx=5, pady=5,
                          command=showCreatePDF)

showCreateFilesBtn.place(x=10, y=10, width=120, height=35)
showAddLabelBtn.place(x=135, y=10, width=120, height=35)
showResizeImageBtn.place(x=260, y=10, width=120, height=35)
showCreatePDFBtn.place(x=385, y=10, width=120, height=35)

saveStatus = Label(root, textvariable=saveStatusVar,
                   background='#15133C', foreground='#EC994B')

folderName = StringVar()
currentFilePath = Label(
    root, textvariable=folderName, background='#15133C', foreground='#EC994B')

madeWithLoveBy = Label(
    root, text='Made with ❤ by Mohamed Omar', background='#15133C', foreground='#EC994B',
    font=('monospace', 9, 'bold'))

versionNo = Label(
    root, text=f'v.{appVersionNo}', background='#15133C', foreground='#EC994B',
    font=('monospace', 9, 'bold'))

root.title(f'TIF_Files_Handler {appVersionNo}')
resizeWindow(515, 80)
root.configure(bg='#000')

root.resizable(False, False)
# Setting icon of master window
root.iconbitmap(resource_path('tif.ico'))
# Start program
root.mainloop()
