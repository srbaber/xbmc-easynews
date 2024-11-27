import re

import action
import constants
import properties
import xbmc

max_history = properties.get_property('history', '10')
max_watched = properties.get_property('watched', '500')
LAST_KEYWORDS = 'lastKeywords'
LAST_WATCHED = 'lastWatched'


#
# handler responsible for clean up of download delete
#
class EasynewsCleanupHandler:
    name = 'EasynewsCleanupHandler'
    remove_history_operation = 'RemoveHistory'
    remove_watched_operation = 'RemoveWatched'
    clear_history_operation = 'ClearHistory'
    clear_watched_operation = 'ClearWatched'
    edit_history_operation = 'EditHistory'
    remove_history = properties.get_localized_string(30340, 'Remove')
    clear_history = properties.get_localized_string(30341, 'Clear History')
    remove_watched = properties.get_localized_string(30340, 'Remove')
    clear_watched = properties.get_localized_string(30343, 'Clear Watched')
    edit_history = properties.get_localized_string(30342, 'Edit')

    def __init__(self):
        pass

    def apply(self, addon_handle, activity):
        if constants.APPLY_LOG:
            xbmc.log('%s.apply %s %s' % (self.name, addon_handle, activity.tostring()), 1)

        if activity.operation == self.remove_history_operation:
            remove_history(activity.state['search_phrase'])
            xbmc.executebuiltin('Container.Refresh')
        if activity.operation == self.remove_watched_operation:
            remove_watched(activity)
            xbmc.executebuiltin('Container.Refresh')
        elif activity.operation == self.clear_history_operation:
            clear_history()
            xbmc.executebuiltin('Container.Refresh')
        elif activity.operation == self.clear_watched_operation:
            clear_watched()
            xbmc.executebuiltin('Container.Refresh')
        elif activity.operation == self.edit_history_operation:
            edit_history(activity)
            xbmc.executebuiltin('Container.Refresh')


def edit_history(activity):
    old_phrase = activity.state['search_phrase']

    kb = xbmc.Keyboard(old_phrase, EasynewsCleanupHandler.edit_history, False)
    kb.doModal()
    if kb.isConfirmed():
        # get text from keyboard
        new_phrase = kb.getText()
        replace_search(old_phrase, new_phrase)


def clear_history():
    for i in range(int(max_history)):
        set_search(i, '')


def clear_watched():
    watched_list = []
    save_watched(watched_list)


def remove_history(search_phrase):
    j = 0
    for i in range(int(max_history)):
        value = get_search(i)

        # skip the copy
        if value == search_phrase:
            continue

        # move the list up
        if j != i:
            set_search(j, value)
        j = j + 1

    # clear the rest of the list
    for i in range(j + 1, int(max_history), 1):
        set_search(i, '')


def remove_watched(watched_activity):
    watched_list = get_watched()
    for watched_item in watched_list:
        existing_url = get_url(watched_item)
        watched_url = get_url(watched_activity)

        # remove the item
        if existing_url == watched_url:
            watched_list.remove(watched_item)

    save_watched(watched_list)


def get_search(index):
    return properties.get_property(LAST_KEYWORDS + '_%d' % index, '')


def set_search(index, search_phrase):
    properties.set_property(LAST_KEYWORDS + "_%d" % index, search_phrase)


def get_watched():
    encoded_value = properties.get_property(LAST_WATCHED, '')
    if encoded_value == '':
        return None

    decoded_watch_list = []
    watched_list = action.loads(encoded_value)
    for watched_item in watched_list:
        decoded_watch_list.append(action.decode(watched_item))

    return decoded_watch_list


def save_watched(watched_activities):
    encoded_watch_list = []
    for watched_item in watched_activities:
        encoded_watch_list.append(action.encode(watched_item))

    properties.set_property(LAST_WATCHED, action.dumps(encoded_watch_list))


def replace_search(old_phrase, search_phrase):
    for i in range(int(max_history)):
        value = get_search(i)
        if value == old_phrase:
            set_search(i, search_phrase)


def add_search(search_phrase):
    last_index = int(max_history) - 1

    # find the item in the list
    for i in range(int(max_history)):
        last_search_phrase = get_search(i)
        if search_phrase == last_search_phrase:
            last_index = i + 1
            break

    # move the list down
    for i in range(last_index - 1, 0, -1):
        value = get_search(i - 1)
        set_search(i, value)

    # add at first position
    set_search(0, search_phrase)


def last_search():
    return get_search(0)


def get_url(watched_item):
    url = watched_item.state.get('url', '')
    url = re.sub('\?.*', '', url)
    return url


def add_watched(watched_activity):
    # make sure the function is enabled
    watched_enabled = properties.get_property('watched_enabled', 'false') == 'true'
    if not watched_enabled:
        return

    watched_list = get_watched()
    if watched_list is None:
        watched_list = []
    else:
        # if it exists remove it
        for watched_item in watched_list:
            existing_url = get_url(watched_item)
            watched_url = get_url(watched_activity)
            if existing_url == watched_url:
                watched_list.remove(watched_item)

    # add the item to the front of the list
    watched_list.insert(0, watched_activity)

    # prune the list
    if len(watched_list) > int(max_watched):
        watched_list = watched_list[:int(max_watched)]

    # save the list to the properties
    save_watched(watched_list)
