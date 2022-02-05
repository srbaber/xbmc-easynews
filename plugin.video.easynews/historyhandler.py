import xbmc, xbmcplugin

import properties
import action
import properties
from easynewshistoryhandler import EasynewsHistoryHandler

lastKeywords = 'lastKeywords'
maxHistory = properties.get_property('history', '10')

class HistoryHandler():
    name = 'HistoryHandler'
    showHistory = 'ShowHistory'
    clearHistory = 'ClearHistory'

    def add_history(self, addonhandle, searchPhrase):
        historyAction = action.of(EasynewsHistoryHandler.name, EasynewsHistoryHandler.searchKeyword, searchPhrase, state={'searchPhrase': searchPhrase})
        xbmcplugin.addDirectoryItem(addonhandle, historyAction.url(), historyAction.directoryitem(), isFolder=True)

    def add_clear_history(self, addonhandle):
        historyAction = action.of(self.name, self.clearHistory, 'Clear History')
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
        elif activity.operation == self.clearHistory:
            clear_history()
            xbmc.executebuiltin('Container.Refresh')

def get_search(index):
    return properties.get_property(lastKeywords + '_%d' % index, '')

def set_search(index, searchPhrase):
    properties.set_property(lastKeywords + "_%d" % index, searchPhrase)

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

def clear_history():
    for i in range(int(maxHistory)):
        set_search(i, '')