import html
import re

import action
import properties
import xbmc
import xbmcplugin
from easynewssearchhandler import EasynewsSearchHandler

MAIN_URL = 'https://members.easynews.com/index.html'


#
#
#
class GroupItem:
    def __init__(self, group, count):
        self.group = group
        self.count = count


#
# handler responsible for performing the groups search for easynews
#
def add_group(addon_handle, group_item):
    title = '%s (%s posts)' % (group_item.group, group_item.count)
    group_action = action.of(EasynewsSearchHandler.name, EasynewsSearchHandler.search_group_operation, title,
                             state={'group': group_item.group})
    xbmcplugin.addDirectoryItem(addon_handle, group_action.url(), group_action.directory_item(), isFolder=True)


class EasynewsGroupsHandler(EasynewsSearchHandler):
    name = 'EasynewsGroupsHandler'
    search_groups_operation = 'SearchGroups'

    search_groups = properties.get_localized_string(30311, 'Search Groups')

    def build_params(self, activity):
        if self.search_groups_operation in activity.state:
            search_phrase = activity.state[self.search_groups_operation]
        else:
            groups = properties.get_property('groups', '')
            kb = xbmc.Keyboard(groups, self.search_groups, False)
            kb.doModal()
            if kb.isConfirmed():
                # get text from keyboard
                search_phrase = kb.getText()
            else:
                search_phrase = self.search_abort_operation

        params = super().build_params(activity)
        params['search'] = search_phrase
        params['nocache'] = '1635253521'
        params['sortOpt'] = '0'
        return params

    def build_url(self, activity):
        return MAIN_URL

    def parse(self, addon_handle, data):
        # xbmc.log("Parse Data : %s" % data, 1)
        results = re.compile('<table class="grouplist"(.+?)</table>', re.DOTALL).findall(data)
        if len(results) == 0:
            return

        items = re.compile('<tr class=(.+?)</tr>', re.DOTALL).findall(results[0])
        group_items = []
        if items:
            for item in items:
                count = re.compile('<td class="count">(.+?)</td>',
                                   re.DOTALL).findall(item)
                count = count[0]
                group = re.compile('value="(.+?)"', re.DOTALL).findall(item)
                group = html.unescape(group[0])
                group_items.append(GroupItem(group, count))

        # sort by number of articles descending
        group_items.sort(key=lambda x: x.count, reverse=True)

        for group_item in group_items:
            add_group(addon_handle, group_item)
