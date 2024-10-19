import constants
import properties
import xbmc

maxHistory = properties.get_property('history', '10')
LAST_KEYWORDS = 'lastKeywords'


#
# handler responsible for clean up of download delete
#
class EasynewsCleanupHandler:
    name = 'EasynewsCleanupHandler'
    remove_operation = 'Remove'
    clear_operation = 'Clear'
    edit_history_operation = 'EditHistory'
    remove_history = properties.get_localized_string(30340, 'Remove')
    clear_history = properties.get_localized_string(30341, 'Clear History')
    edit_history = properties.get_localized_string(30342, 'Edit')

    def __init__(self):
        pass

    def apply(self, addon_handle, activity):
        if constants.APPLY_LOG:
            xbmc.log('%s.apply %s %s' % (self.name, addon_handle, activity.tostring()), 1)

        if activity.operation == self.remove_operation:
            remove_history(activity.state['search_phrase'])
            xbmc.executebuiltin('Container.Refresh')
        elif activity.operation == self.clear_operation:
            clear_history()
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
    for i in range(int(maxHistory)):
        set_search(i, '')


def remove_history(search_phrase):
    j = 0
    for i in range(int(maxHistory)):
        value = get_search(i)
        if value != search_phrase:
            set_search(j, value)
            j = j + 1

    for i in range(j + 1, int(maxHistory), 1):
        set_search(i, '')


def get_search(index):
    return properties.get_property(LAST_KEYWORDS + '_%d' % index, '')


def set_search(index, search_phrase):
    properties.set_property(LAST_KEYWORDS + "_%d" % index, search_phrase)


def replace_search(old_phrase, search_phrase):
    for i in range(int(maxHistory)):
        value = get_search(i)
        if value == old_phrase:
            set_search(i, search_phrase)
