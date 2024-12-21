import html
import re

import action
import constants
import getrequest
import xbmc
import xbmcplugin
from easynewssearchhandler import EasynewsSearchHandler, go_to_main_menu, check_for_invalid_user_id, get_page_number

SAVED_SEARCH_URL = 'https://members.easynews.com/savedSrch.html'
MAIN_URL = "https://members.easynews.com/1.0/global5"


class EasynewsSavedSearchHandler(EasynewsSearchHandler):
    name = 'SavedSearchHandler'
    show_saved_searches_operation = 'showSavedSearches'

    def build_params(self, activity):
        params = {}
        return params

    def build_url(self, activity):
        url = activity.state['searchUrl']
        url = html.unescape(url)

        # makes sure we set the result output as RSS feed for easy parsing
        url = re.sub('sS=.&', 'sS=5&', url)
        url = re.sub('pno=[0-9]*&', 'pno=' + str(get_page_number(activity)) + '&', url)
        return url

    def add_saved_search(self, addon_handle, search_phrase, search_url):
        search_action = action.of(EasynewsSavedSearchHandler.name, EasynewsSearchHandler.search_and_order_operation,
                                  search_phrase, state={'searchUrl': search_url, 'page_number': '1'})
        xbmcplugin.addDirectoryItem(addon_handle, search_action.url(), search_action.directory_item(), isFolder=True)

    def parse_saved_searches(self, addon_handle, response):
        data = re.sub('</td>', '</td>\n', response.text)
        searches = re.compile('<input type="text" name="l[0-9]*" value="(.+?)"', re.DOTALL).findall(data)
        urls = re.compile('<a target="gSearch" href="/1.0/global5/(.+?)"', re.DOTALL).findall(data)

        for i in range(len(searches)):
            search = searches[i]
            url = MAIN_URL + urls[i]
            self.add_saved_search(addon_handle, search, url)

    def show_saved_searches(self, addon_handle):
        response = getrequest.get(SAVED_SEARCH_URL, {})
        self.parse_saved_searches(addon_handle, response)
        xbmcplugin.endOfDirectory(addon_handle)

    def apply(self, addon_handle, activity):
        if constants.APPLY_LOG:
            xbmc.log('%s.apply %s %s' % (self.name, addon_handle, activity.tostring()), 1)

        if check_for_invalid_user_id():
            go_to_main_menu(addon_handle)
            return

        if activity.operation == self.show_saved_searches_operation:
            self.show_saved_searches(addon_handle)
        else:
            super().apply(addon_handle, activity)
