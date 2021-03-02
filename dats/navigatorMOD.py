#####################################################
# imports
#####################################################

import urllib.request
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

