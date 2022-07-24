import threading


def initProgBar(one, two, three):
    global root, pb1, startProgBar
    root = one
    pb1 = two
    startProgBar = three
    startProgressBar()
    stopProgressBar()


def stepVa():
    pb1.step(10)
    root.update()


def startProgressBar():
    stepVa()
    global thr
    thr = threading.Timer(1, startProgressBar)
    thr.start()
    if startProgBar.get() == False:
        pb1.stop()
        thr.cancel()
    startProgBar.set(True)


def stopProgressBar():
    startProgBar.set(False)
    root.update()


def pbOnClosing():
    stopProgressBar()
    if startProgBar.get() == False:
        thr.cancel()
