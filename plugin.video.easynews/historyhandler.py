import xbmc, xbmcplugin

import action
from easynewshistoryhandler import EasynewsHistoryHandler
from easynewscleanuphandler import get_search, set_search, maxHistory, EasynewsCleanupHandler

class HistoryHandler():
    name = 'HistoryHandler'
    showHistory = 'ShowHistory'

    def add_history(self, addonhandle, searchPhrase):
        historyAction = action.of(EasynewsHistoryHandler.name, EasynewsHistoryHandler.searchKeyword, searchPhrase, state={'searchPhrase': searchPhrase})
        xbmcplugin.addDirectoryItem(addonhandle, historyAction.url(), historyAction.historyitem(), isFolder=True)

    def add_clear_history(self, addonhandle):
        handler = EasynewsCleanupHandler()
        historyAction = action.of(handler.name, handler.clearHistory, 'Clear History')
        xbmcplugin.addDirectoryItem(addonhandle, historyAction.url(), historyAction.directoryitem(), isFolder=False)

    def show_history(self, addonhandle):
        for i in range(int(maxHistory)):
            searchPhrase = get_search(i)
            if searchPhrase != '':
                self.add_history(addonhandle, searchPhrase)

        self.add_clear_history(addonhandle)
        xbmcplugin.endOfDirectory(addonhandle)

    def apply(self, addonhandle, activity):
        xbmc.log('%s.apply %s %s' % (self.name, addonhandle, activity.tostring()), 1)

        if activity.operation == self.showHistory:
            self.show_history(addonhandle)

def last_search():
    return get_search(0)

def add_search(searchPhrase):
    last_index = int(maxHistory) - 1

    for i in range(int(maxHistory)):
        last_search = get_search(i)
        if searchPhrase == last_search:
            last_index = i+1
            break

    for i in range(last_index-1, 0, -1):
        value = get_search(i-1)
        set_search(i, value)

    set_search(0, searchPhrase)


