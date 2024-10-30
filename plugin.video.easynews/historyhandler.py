import action
import constants
import properties
import xbmc
import xbmcgui
import xbmcplugin
from easynewscleanuphandler import get_search, max_history, get_watched, EasynewsCleanupHandler
from easynewssearchhandler import EasynewsSearchHandler, go_to_main_menu


class HistoryHandler:
    name = 'HistoryHandler'
    show_history_operation = 'ShowHistory'
    show_watched_operation = 'ShowWatched'

    def apply(self, addon_handle, activity):
        if constants.APPLY_LOG:
            xbmc.log('%s.apply %s %s' % (self.name, addon_handle, activity.tostring()), 1)

        if activity.operation == self.show_history_operation:
            show_history(addon_handle)
        elif activity.operation == self.show_watched_operation:
            watched_enabled = properties.get_property('watched_enabled', 'false') == 'true'
            if watched_enabled:
                show_watched(addon_handle)
            else:
                xbmcgui.Dialog().ok('Easynews Configuration',
                                    'Please enable Track Watched in the settings')
                go_to_main_menu(addon_handle)


def add_clear_history(addon_handle):
    history_action = action.of(EasynewsCleanupHandler.name, EasynewsCleanupHandler.clear_history_operation,
                               EasynewsCleanupHandler.clear_history)
    xbmcplugin.addDirectoryItem(addon_handle, history_action.url(), history_action.directory_item(), isFolder=False)


def add_clear_watched(addon_handle):
    history_action = action.of(EasynewsCleanupHandler.name, EasynewsCleanupHandler.clear_watched_operation,
                               EasynewsCleanupHandler.clear_watched)
    xbmcplugin.addDirectoryItem(addon_handle, history_action.url(), history_action.directory_item(), isFolder=False)


def add_history_context_menu(activity):
    edit = action.of(EasynewsCleanupHandler.name, EasynewsCleanupHandler.edit_history_operation,
                     EasynewsCleanupHandler.edit_history, activity.thumbnail, activity.state)
    remove = action.of(EasynewsCleanupHandler.name, EasynewsCleanupHandler.remove_history_operation,
                       EasynewsCleanupHandler.remove_history, activity.thumbnail, activity.state)
    cm = [(EasynewsCleanupHandler.edit_history, 'RunPlugin(%s)' % edit.url()),
          (EasynewsCleanupHandler.remove_history, 'RunPlugin(%s)' % remove.url())]

    item = activity.playable_item()
    item.addContextMenuItems(cm)
    return item


def add_watched_context_menu(activity):
    remove = action.of(EasynewsCleanupHandler.name, EasynewsCleanupHandler.remove_watched_operation,
                       EasynewsCleanupHandler.remove_watched, activity.thumbnail, activity.state)
    cm = [(EasynewsCleanupHandler.remove_watched, 'RunPlugin(%s)' % remove.url())]

    item = activity.playable_item()
    item.addContextMenuItems(cm)
    return item


def add_history(addon_handle, search_phrase):
    history_action = action.of(EasynewsSearchHandler.name, EasynewsSearchHandler.search_and_order_operation,
                               search_phrase,
                               state={'search_phrase': search_phrase})
    list_item = add_history_context_menu(history_action)
    xbmcplugin.addDirectoryItem(addon_handle, history_action.url(), list_item, isFolder=True)


def add_watched_activity(addon_handle, watched_activity):
    list_item = add_watched_context_menu(watched_activity)
    xbmcplugin.addDirectoryItem(addon_handle, watched_activity.url(), list_item, isFolder=False)


def show_history(addon_handle):
    for i in range(int(max_history)):
        search_phrase = get_search(i)
        if search_phrase == '':
            break
        else:
            add_history(addon_handle, search_phrase)

    add_clear_history(addon_handle)
    xbmcplugin.endOfDirectory(addon_handle)


def show_watched(addon_handle):
    watched_list = get_watched()
    for watched_activity in watched_list:
        add_watched_activity(addon_handle, watched_activity)

    add_clear_watched(addon_handle)
    xbmcplugin.endOfDirectory(addon_handle)
