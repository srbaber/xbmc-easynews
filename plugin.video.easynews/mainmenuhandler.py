import action
import constants
import xbmc
import xbmcplugin
from easynewsgroupshandler import EasynewsGroupsHandler
from easynewskeywordhandler import EasynewsKeywordHandler
from easynewssavedsearchhandler import EasynewsSavedSearchHandler
from easynewssearchhandler import EasynewsSearchHandler
from easynewszipmanagerhandler import EasynewsZipManagerHandler
from filehandler import FileHandler
from historyhandler import HistoryHandler


#
# handler responsible for building the main menu
#
class MainMenuHandler:
    name = 'MainMenuHandler'

    searchByDate = 'Recent Posts'
    searchKeyword = 'Keyword Search'
    searchHistory = 'Search History'
    searchGroup = 'Group Search'
    downloads = 'Downloads'
    zipManager = 'Zip Manager'
    savedSearches = 'Saved Searches'

    def __init__(self):
        pass

    def apply(self, addon_handle, activity):
        if constants.APPLY_LOG:
            xbmc.log('%s.apply %s %s' % (self.name, addon_handle, activity.tostring()), 1)

        add_menu_item(addon_handle, EasynewsSearchHandler.name, EasynewsSearchHandler.search_recent_operation,
                      self.searchByDate)

        add_menu_item(addon_handle, EasynewsGroupsHandler.name, EasynewsGroupsHandler.search_groups_operation,
                      self.searchGroup)

        add_menu_item(addon_handle, EasynewsKeywordHandler.name, EasynewsKeywordHandler.search_operation,
                      self.searchKeyword)

        add_menu_item(addon_handle, HistoryHandler.name, HistoryHandler.show_history_operation, self.searchHistory)

        add_menu_item(addon_handle, FileHandler.name, FileHandler.playback, self.downloads)

        add_menu_item(addon_handle, EasynewsZipManagerHandler.name, EasynewsZipManagerHandler.list_queues_operation,
                      self.zipManager)

        add_menu_item(addon_handle, EasynewsSavedSearchHandler.name,
                      EasynewsSavedSearchHandler.show_saved_searches_operation,
                      self.savedSearches)

        xbmcplugin.endOfDirectory(addon_handle)


def add_menu_item(addon_handle, name, operation, menu_option):
    activity = action.of(name, operation, menu_option)
    xbmcplugin.addDirectoryItem(addon_handle, activity.url(), activity.directory_item(), isFolder=True)
