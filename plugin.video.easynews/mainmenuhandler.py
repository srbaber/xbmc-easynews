import action
import constants
import xbmc
import xbmcplugin
from easynewsgroupshandler import EasynewsGroupsHandler
from easynewskeywordhandler import EasynewsKeywordHandler
from easynewssearchhandler import EasynewsSearchHandler
from savedSearchHandler import SavedSearchHandler
from easynewssizehandler import EasynewsSizeHandler
from easynewszipmanagerhandler import EasynewsZipManagerHandler
from filehandler import FileHandler
from historyhandler import HistoryHandler


#
# handler responsible for building the main menu
#
class MainMenuHandler():
    name = 'MainMenuHandler'

    searchByDate = 'Search By Date'
    searchBySize = 'Search By Size'
    searchKeyword = 'Keyword Search'
    savedSearches = 'Saved Searches'
    searchHistory = 'Search History'
    searchGroup = 'Group Search'
    downloads = 'Downloads'
    zipmanager = 'Zip Manager'

    def __init__(self):
        pass

    def apply(self, addonhandle, activity):
        if constants.APPLY_LOG:
            xbmc.log('%s.apply %s' % (self.name, addonhandle), 1)

        activity = action.of(EasynewsKeywordHandler.name, EasynewsKeywordHandler.searchKeyword, self.searchKeyword)
        xbmcplugin.addDirectoryItem(addonhandle, activity.url(), activity.directoryitem(), isFolder=True)

        activity = action.of(SavedSearchHandler.name, SavedSearchHandler.showSavedSearches, self.savedSearches)
        xbmcplugin.addDirectoryItem(addonhandle, activity.url(), activity.directoryitem(), isFolder=True)

        activity = action.of(EasynewsGroupsHandler.name, EasynewsGroupsHandler.searchGroups, self.searchGroup)
        xbmcplugin.addDirectoryItem(addonhandle, activity.url(), activity.directoryitem(), isFolder=True)

        activity = action.of(EasynewsSearchHandler.name, EasynewsSearchHandler.searchByDate, self.searchByDate)
        xbmcplugin.addDirectoryItem(addonhandle, activity.url(), activity.directoryitem(), isFolder=True)

        activity = action.of(EasynewsSizeHandler.name, EasynewsSizeHandler.searchBySize, self.searchBySize)
        xbmcplugin.addDirectoryItem(addonhandle, activity.url(), activity.directoryitem(), isFolder=True)

        activity = action.of(HistoryHandler.name, HistoryHandler.showHistory, self.searchHistory)
        xbmcplugin.addDirectoryItem(addonhandle, activity.url(), activity.directoryitem(), isFolder=True)

        activity = action.of(FileHandler.name, FileHandler.playback, self.downloads)
        xbmcplugin.addDirectoryItem(addonhandle, activity.url(), activity.directoryitem(), isFolder=True)

        activity = action.of(EasynewsZipManagerHandler.name, EasynewsZipManagerHandler.listQueues, self.zipmanager)
        xbmcplugin.addDirectoryItem(addonhandle, activity.url(), activity.directoryitem(), isFolder=True)

        xbmcplugin.endOfDirectory(addonhandle)