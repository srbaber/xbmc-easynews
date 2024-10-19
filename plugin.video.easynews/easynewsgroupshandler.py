import html
import re

import action
import easynewssearchhandler
import properties
import xbmc
import xbmcplugin
from downloadhandler import DownloadHandler
from easynewsgrouphandler import EasynewsGroupHandler

MAIN_URL = 'https://members.easynews.com/index.html'


#
# handler responsible for performing the groups search for easynews
#
class EasynewsGroupsHandler(easynewssearchhandler.EasynewsSearchHandler):
    name = 'EasynewsGroupsHandler'
    search_groups_operation = 'SearchGroups'

    search_groups = properties.get_localized_string(30311, 'Search Groups')

    def build_params(self, activity):
        if self.search_groups_operation not in activity.state:
            groups = properties.get_property('groups', '')
            kb = xbmc.Keyboard(groups, self.search_groups, False)
            kb.doModal()
            if kb.isConfirmed():
                # get text from keyboard
                search_phrase = kb.getText()
            else:
                search_phrase = self.search_abort_operation
        else:
            search_phrase = activity.state[self.search_groups_operation]

        params = super().build_params(activity)

        params['search'] = search_phrase
        params['nocache'] = '1635253521'
        params['sortOpt'] = '0'
        return params

    def build_url(self, activity):
        return MAIN_URL

    def add_context_menu(self, activity):
        download = action.of(DownloadHandler.name, DownloadHandler.download_operation, DownloadHandler.download_file,
                             activity.thumbnail, activity.state)
        cm = [(DownloadHandler.download_file, 'RunPlugin(%s)' % download.url())]

        item = activity.playable_item()
        item.addContextMenuItems(cm)
        return item

    def add_group(self, addon_handle, group, count):
        title = '%s (%s posts)' % (group, count)
        group_action = action.of(EasynewsGroupHandler.name, EasynewsGroupHandler.search_group_operation, title,
                                 state={'group': group})
        list_item = self.add_context_menu(group_action)
        xbmcplugin.addDirectoryItem(addon_handle, group_action.url(), list_item, isFolder=True)

    def parse(self, addon_handle, data):
        # xbmc.log("Parse Data : %s" % data, 1)
        results = re.compile('<table class="grouplist"(.+?)</table>',
                             re.DOTALL).findall(data)
        if len(results) == 0:
            return

        items = re.compile('<tr class=(.+?)</tr>',
                           re.DOTALL).findall(results[0])

        if items:
            for item in items:
                count = re.compile('<td class="count">(.+?)</td>',
                                   re.DOTALL).findall(item)
                count = count[0]

                group = re.compile('value="(.+?)"',
                                   re.DOTALL).findall(item)
                group = html.unescape(group[0])

                self.add_group(addon_handle, group, count)
