import action
import constants
import xbmc
import xbmcplugin
from easynewscleanuphandler import get_search, set_search, maxHistory, EasynewsCleanupHandler
from easynewshistoryhandler import EasynewsHistoryHandler


class HistoryHandler():
    name = 'HistoryHandler'
    show_history_operation = 'ShowHistory'

    def contextmenu(self, activity):
        remove = action.of(EasynewsCleanupHandler.name, EasynewsCleanupHandler.remove_operation,
                           EasynewsCleanupHandler.remove_history, activity.thumbnail, activity.state)
        cm = [(EasynewsCleanupHandler.remove_history, 'RunPlugin(%s)' % remove.url())]

        item = activity.playableitem()
        item.addContextMenuItems(cm)
        return item

    def add_history(self, addonhandle, searchPhrase):
        historyAction = action.of(EasynewsHistoryHandler.name, EasynewsHistoryHandler.search_operation, searchPhrase,
                                  state={'searchPhrase': searchPhrase})
        contextmenu = self.contextmenu(historyAction)
        xbmcplugin.addDirectoryItem(addonhandle, historyAction.url(), contextmenu, isFolder=True)

    def add_clear_history(self, addonhandle):
        historyAction = action.of(EasynewsCleanupHandler.name, EasynewsCleanupHandler.clear_operation, EasynewsCleanupHandler.clear_history)
        xbmcplugin.addDirectoryItem(addonhandle, historyAction.url(), historyAction.directoryitem(), isFolder=False)

    def show_history(self, addonhandle):
        for i in range(int(maxHistory)):
            searchPhrase = get_search(i)
            if searchPhrase != '':
                self.add_history(addonhandle, searchPhrase)

        self.add_clear_history(addonhandle)
        xbmcplugin.endOfDirectory(addonhandle)

    def apply(self, addonhandle, activity):
        if constants.APPLY_LOG:
            xbmc.log('%s.apply %s %s' % (self.name, addonhandle, activity.tostring()), 1)

        if activity.operation == self.show_history_operation:
            self.show_history(addonhandle)


def last_search():
    return get_search(0)


def add_search(searchPhrase):
    last_index = int(maxHistory) - 1

    for i in range(int(maxHistory)):
        last_search = get_search(i)
        if searchPhrase == last_search:
            last_index = i + 1
            break

    for i in range(last_index - 1, 0, -1):
        value = get_search(i - 1)
        set_search(i, value)

    set_search(0, searchPhrase)
