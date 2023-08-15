import action
import constants
import getrequest
import re
import xbmc
import xbmcplugin
from easynewssearchhandler import EasynewsSearchHandler

SAVED_SEARCH_URL = 'https://members.easynews.com/savedSrch.html'


class EasynewsSavedSearchHandler(EasynewsSearchHandler):
    name = 'SavedSearchHandler'
    show_saved_searches_operation = 'showSavedSearches'

    def add_saved_search(self, addonhandle, search_phrase, search_url):
        search_action = action.of(EasynewsSavedSearchHandler.name, EasynewsSearchHandler.search_by_date_operation,
                                 search_phrase, state={'searchUrl': search_url})
        xbmcplugin.addDirectoryItem(addonhandle, search_action.url(), search_action.directoryitem(), isFolder=True)

    def build_params(self, action):
        params = {}
        url = action.state['searchUrl']
        url = re.sub('^.*\?', '', url)
        url_params = url.split('&amp;')
        for param in url_params:
            key_values=param.split('=')
            params[key_values[0]] = key_values[1]

        params['sS'] = 5
        return params

    def build_url(self, action):
        url = action.state['searchUrl']
        url = re.sub('\?.*$', '', url)
        return url

    def find_saved_searches(self):
        return getrequest.get(self, SAVED_SEARCH_URL, {})

    def parse_saved_searches(self, addonhandle, data):
        searches = re.compile('<input type="text" name="l[0-9]*" value="(.+?)".*>', re.DOTALL).findall(data)
        urls = re.compile('2.0</a></td><td align="center"><a target="gSearch" href="(.+?)">Global5</a>', re.DOTALL).findall(data)
        if searches:
            for i in range(len(searches)):
                search = searches[i]
                url = urls[i]
                if search is not None and len(url) > 2 and url is not None:
                    self.add_saved_search(addonhandle, search, url)

    def show_saved_searches(self, addonhandle):
        response = self.find_saved_searches()
        self.parse_saved_searches(addonhandle, response)
        xbmcplugin.endOfDirectory(addonhandle)

    def apply(self, addonhandle, activity):
        if constants.APPLY_LOG:
            xbmc.log('%s.apply %s %s' % (self.name, addonhandle, activity.tostring()), 1)

        if activity.operation == self.show_saved_searches_operation:
            self.show_saved_searches(addonhandle)
        else:
            super().apply(addonhandle, activity)