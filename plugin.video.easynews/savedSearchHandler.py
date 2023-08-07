import action
import constants
import getrequest
import re
import xbmc
import xbmcplugin
from easynewshistoryhandler import EasynewsHistoryHandler

SAVED_SEARCH_URL = 'https://members.easynews.com/savedSrch.html'


class SavedSearchHandler():
    name = 'SavedSearchHandler'
    showSavedSearches = 'showSavedSearches'

    def contextmenu(self, activity):
        item = activity.playableitem()
        return item

    def add_history(self, addonhandle, searchPhrase):
        historyAction = action.of(EasynewsHistoryHandler.name, EasynewsHistoryHandler.searchKeyword, searchPhrase,
                                  state={'searchPhrase': searchPhrase})
        contextmenu = self.contextmenu(historyAction)
        xbmcplugin.addDirectoryItem(addonhandle, historyAction.url(), contextmenu, isFolder=True)

    def build_url(self):
        return SAVED_SEARCH_URL

    def search(self, action):
        return getrequest.get(self, self.build_url(), {})

    def parse(self, data):
        searches = []

        items = re.compile('<input type="text"(.+?)value="(.+?)"(.+?)>', re.DOTALL).findall(data)
        if items:
            for item in items:
                if item is not None and len(item) > 2:
                    searches.append(item[1])
        
        return searches


    def show_saved_searches(self, addonhandle, activity):

        response = self.search(activity)
        searches = self.parse(response)

        for term in searches:
            if term != '':
                self.add_history(addonhandle, term)

        xbmcplugin.endOfDirectory(addonhandle)

    def apply(self, addonhandle, activity):
        if constants.APPLY_LOG:
            xbmc.log('%s.apply %s %s' % (self.name, addonhandle, activity.tostring()), 1)

        if activity.operation == self.showSavedSearches:
            self.show_saved_searches(addonhandle, activity)
