import html
import re

import action
import constants
import getrequest
import xbmc
import xbmcplugin
from easynewssearchhandler import EasynewsSearchHandler

SAVED_SEARCH_URL = 'https://members.easynews.com/savedSrch.html'


class EasynewsSavedSearchHandler(EasynewsSearchHandler):
    name = 'SavedSearchHandler'
    show_saved_searches_operation = 'showSavedSearches'

    def build_params(self, activity):
        params = {}
        return params

    def build_url(self, activity):
        url = activity.state['searchUrl']
        url = html.unescape(url)
        url = re.sub('sS=.', 'sS=5', url)
        return url

    def apply(self, addon_handle, activity):
        if constants.APPLY_LOG:
            xbmc.log('%s.apply %s %s' % (self.name, addon_handle, activity.tostring()), 1)

        if activity.operation == self.show_saved_searches_operation:
            show_saved_searches(addon_handle)
        else:
            super().apply(addon_handle, activity)


def add_saved_search(addon_handle, search_phrase, search_url):
    search_action = action.of(EasynewsSavedSearchHandler.name, EasynewsSearchHandler.search_and_order_operation,
                              search_phrase, state={'searchUrl': search_url})
    xbmcplugin.addDirectoryItem(addon_handle, search_action.url(), search_action.directory_item(), isFolder=True)


def parse_saved_searches(addon_handle, data):
    data = re.sub('</td>', '</td>\n', data)
    searches = re.compile('<input type="text" name="l[0-9]*" value="(.+?)"', re.DOTALL).findall(data)
    urls = re.compile('<a target="gSearch" href="/1.0/global5/(.+?)"', re.DOTALL).findall(data)

    if searches:
        for i in range(len(searches)):
            search = searches[i]
            url = "https://members.easynews.com/1.0/global5" + urls[i]
            if search is not None and url is not None and len(url) > 2:
                add_saved_search(addon_handle, search, url)
        return len(searches)
    return 0


def find_saved_searches():
    return getrequest.get(SAVED_SEARCH_URL, {})


def show_saved_searches(addon_handle):
    response = find_saved_searches()
    parse_saved_searches(addon_handle, response)
    xbmcplugin.endOfDirectory(addon_handle)
