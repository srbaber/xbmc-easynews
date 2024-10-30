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

    search_by_date = 'Recent Posts'
    search_keyword = 'Keyword Search'
    search_history = 'Search History'
    watched_history = 'Watched History'
    search_group = 'Group Search'
    downloads = 'Downloads'
    zip_manager = 'Zip Manager'
    saved_searches = 'Saved Searches'

    def __init__(self):
        pass

    def apply(self, addon_handle, activity):
        if constants.APPLY_LOG:
            xbmc.log('%s.apply %s %s' % (self.name, addon_handle, activity.tostring()), 1)

        add_menu_item(addon_handle, EasynewsSearchHandler.name, EasynewsSearchHandler.search_recent_operation,
                      self.search_by_date)

        add_menu_item(addon_handle, EasynewsGroupsHandler.name, EasynewsGroupsHandler.search_groups_operation,
                      self.search_group)

        add_menu_item(addon_handle, EasynewsKeywordHandler.name, EasynewsKeywordHandler.search_operation,
                      self.search_keyword)

        add_menu_item(addon_handle, HistoryHandler.name, HistoryHandler.show_history_operation, self.search_history)

        add_menu_item(addon_handle, FileHandler.name, FileHandler.playback, self.downloads)

        add_menu_item(addon_handle, EasynewsZipManagerHandler.name, EasynewsZipManagerHandler.list_queues_operation,
                      self.zip_manager)

        add_menu_item(addon_handle, EasynewsSavedSearchHandler.name,
                      EasynewsSavedSearchHandler.show_saved_searches_operation,
                      self.saved_searches)

        add_menu_item(addon_handle, HistoryHandler.name, HistoryHandler.show_watched_operation, self.watched_history)

        xbmcplugin.endOfDirectory(addon_handle)


def add_menu_item(addon_handle, name, operation, menu_option):
    activity = action.of(name, operation, menu_option)
    xbmcplugin.addDirectoryItem(addon_handle, activity.url(), activity.directory_item(), isFolder=True)
