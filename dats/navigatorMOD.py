#####################################################
# imports
#####################################################

import urllib
import requests

#####################################################
# module variables
#####################################################

NavigatorCOMP   = parent.Navigator
navAndText      = NavigatorCOMP.op('container_ui/container_nav_and_text')
view 		    = NavigatorCOMP.op('container_ui/container_view')
linkManifest    = NavigatorCOMP.op('table_manifestBuffer')

lister          = navAndText.op('container_nav/lister')
webBrowser  	= navAndText.op('webBrowser')

loadingView     = view.op('container_loading')
settingsView    = view.op('container_settings')
dispBuffer      = view.op('container_display_buffer')

transTimer      = loadingView.op('timer1')

#####################################################
## Func Finder
#####################################################
def qs_funcs(func_key):
    func_map = {
        'remoteTox' : loadNewTox,
        'openNetwork' : openFloatingNetwork
        }
    return func_map.get(func_key)


#####################################################
# functions
#####################################################

def selectionHandler(info):
    currentRow      = info.get('row')
    
    # invalid row click
    if currentRow == -1:
        pass

    else:

        if info is None:
            pass

        else:
            lastRowSelected = NavigatorCOMP.fetch('lastRowSelected', 0)
            webPage 	    = info.get('rowData').get('rowObject').get('webPage')
            remoteTox 	    = info.get('rowData').get('rowObject').get('tox')
            col             = info.get('col')

            NavigatorCOMP.store('selectedWebPage', webPage)
            NavigatorCOMP.store('selectedRemoteTox', remoteTox)

            if col == 0:
                # same row clicked
                if lastRowSelected == currentRow:
                    pass

                else:
                    NavigatorCOMP.store('lastRowSelected', currentRow)
                    NavigatorCOMP.store('selectedWebPage', webPage)
                    NavigatorCOMP.store('selectedRemoteTox', remoteTox)
                    loadNewSelection()        

                pass

            # view URL in browser
            elif col == 1:
                ui.viewFile(webPage)

            # # open floating network
            # elif col == 2:
            #     networkView.par.display = (1 if not networkView.par.display.eval() else 0)

    pass

def checkLoad(url):
    qsResult = querryStringParse(url)
    key_list = [key for key in qsResult.keys()]

    if len(key_list) < 1:
        pass

    else:
        print(key_list)
        try:
            func = qs_funcs(key_list[0])
            func(qsResult)
        except Exception as e:
            debug(e)

    pass

def openFloatingNetwork(parsedQs):
    print("Open Floating Window")

    floating_pane = ui.panes.createFloating(name="Example")
    current_example = parent.Navigator.op('container_ui/container_view/container_display_buffer').findChildren(depth=1)[0]
    floating_pane.owner = current_example
    floating_pane.home()

    func = "parent().mod.navigatorMOD.webBrowserGoBack()"
    run(func, delayFrames=5)
    pass

def webBrowserGoBack():
    print("go back")
    webBrowser.par.Goback.pulse()

def loadNewTox(parsedQs):
    remoteTox = parsedQs.get('remoteTox')
    print(remoteTox)
    NavigatorCOMP.store('selectedRemoteTox', remoteTox[0])
    loadNewSelection()
    print('load remote')
    pass

def loadNewSelection():
    loadingView.par['display'] = True
    displayLoadingScreen()

def displayLoadingScreen():
    transTimer.par.start.pulse()

def updateBrowser():
    url = NavigatorCOMP.fetch('selectedWebPage')
    webBrowser.par['Address'] = url

def loadRemoteTox():
    remoteTox = NavigatorCOMP.fetch('selectedRemoteTox')

    try:

        asset 	    = urllib.request.urlopen(remoteTox)
        tox 	    = asset.read()
        loadedTox   = dispBuffer.loadByteArray(tox)
        loadedTox.par['display'] = True
        loadedTox.nodeX = 0
        loadedTox.nodeY = 0
        loadedTox.par.hmode = 1
        loadedTox.par.vmode = 1
        updateBrowser()

    except Exception as e:
        print(e)

def clearView():
    for each in dispBuffer.findChildren(depth=1):
        each.destroy()

def setTimerPlay(playVal):
    transTimer.par['play'] = playVal
    print("called")

def toggleSettings():
    settingsView.par.display = (0 if settingsView.par.display else 1)

def querryStringParse(url):
    parseResult = urllib.parse.urlparse(url).query
    qsResult = urllib.parse.parse_qs(parseResult)
    return qsResult

#####################################################
## Timer Functions
#####################################################

def timerSegmentEnter(**kwargs):
    timerOp = kwargs.get('timerOp')
    segment = kwargs.get('segment')
    interrupt = kwargs.get('interrupt')

    if segment > 0:
        timerOp.par.play = False
        clearView()
        run(loadRemoteTox(), delayFrames = 1)
        timerOp.par.play = True

def onTimerDone(**kwargs):
    loadingView.par['display'] = False
    pass


