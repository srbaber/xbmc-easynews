import action
import constants
import xbmc
import xbmcplugin
from easynewscleanuphandler import get_search, set_search, maxHistory, EasynewsCleanupHandler
from easynewshistoryhandler import EasynewsHistoryHandler
from easynewssearchhandler import EasynewsSearchHandler


class HistoryHandler:
    name = 'HistoryHandler'
    show_history_operation = 'ShowHistory'

    def apply(self, addon_handle, activity):
        if constants.APPLY_LOG:
            xbmc.log('%s.apply %s %s' % (self.name, addon_handle, activity.tostring()), 1)

        if activity.operation == self.show_history_operation:
            show_history(addon_handle)


def last_search():
    return get_search(0)


def add_search(search_phrase):
    last_index = int(maxHistory) - 1

    for i in range(int(maxHistory)):
        last_search_phrase = get_search(i)
        if search_phrase == last_search_phrase:
            last_index = i + 1
            break

    for i in range(last_index - 1, 0, -1):
        value = get_search(i - 1)
        set_search(i, value)

    set_search(0, search_phrase)


def add_clear_history(addon_handle):
    history_action = action.of(EasynewsCleanupHandler.name, EasynewsCleanupHandler.clear_operation,
                               EasynewsCleanupHandler.clear_history)
    xbmcplugin.addDirectoryItem(addon_handle, history_action.url(), history_action.directory_item(), isFolder=False)


def add_context_menu(activity):
    edit = action.of(EasynewsCleanupHandler.name, EasynewsCleanupHandler.edit_history_operation,
                     EasynewsCleanupHandler.edit_history, activity.thumbnail, activity.state)
    remove = action.of(EasynewsCleanupHandler.name, EasynewsCleanupHandler.remove_operation,
                       EasynewsCleanupHandler.remove_history, activity.thumbnail, activity.state)
    cm = [(EasynewsCleanupHandler.edit_history, 'RunPlugin(%s)' % edit.url()),
          (EasynewsCleanupHandler.remove_history, 'RunPlugin(%s)' % remove.url())]

    item = activity.playable_item()
    item.addContextMenuItems(cm)
    return item


def add_history(addon_handle, search_phrase):
    history_action = action.of(EasynewsHistoryHandler.name, EasynewsSearchHandler.search_and_order_operation,
                               search_phrase,
                               state={'search_phrase': search_phrase})
    list_item = add_context_menu(history_action)
    xbmcplugin.addDirectoryItem(addon_handle, history_action.url(), list_item, isFolder=True)


def show_history(addon_handle):
    for i in range(int(maxHistory)):
        search_phrase = get_search(i)
        if search_phrase != '':
            add_history(addon_handle, search_phrase)

    add_clear_history(addon_handle)
    xbmcplugin.endOfDirectory(addon_handle)
