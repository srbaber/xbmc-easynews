import constants
import properties
import xbmc

maxHistory = properties.get_property('history', '10')
LAST_KEYWORDS = 'lastKeywords'


#
# handler responsible for clean up of download delete
#
class EasynewsCleanupHandler():
    name = 'EasynewsCleanupHandler'
    remove_operation = 'Remove'
    clear_operation = 'Clear'
    remove_history = properties.get_localized_string(30340, 'Remove')
    clear_history = properties.get_localized_string(30341, 'Clear History')

    def __init__(self):
        pass

    def apply(self, addonhandle, activity):
        if constants.APPLY_LOG:
            xbmc.log('%s.apply %s %s' % (self.name, addonhandle, activity.tostring()), 1)
        if activity.operation == self.remove_operation:
            remove_history(activity.state['searchPhrase'])
            xbmc.executebuiltin('Container.Refresh')
        elif activity.operation == self.clear_operation:
            clear_history()
            xbmc.executebuiltin('Container.Refresh')


def clear_history():
    for i in range(int(maxHistory)):
        set_search(i, '')


def remove_history(searchPhrase):
    j = 0
    for i in range(int(maxHistory)):
        value = get_search(i)
        if value != searchPhrase:
            set_search(j, value)
            j = j + 1

    for i in range(j + 1, int(maxHistory), 1):
        set_search(i, '')


def get_search(index):
    return properties.get_property(LAST_KEYWORDS + '_%d' % index, '')


def set_search(index, searchPhrase):
    properties.set_property(LAST_KEYWORDS + "_%d" % index, searchPhrase)
