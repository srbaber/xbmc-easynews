import html
import re

import action
import easynewssearchhandler
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
    searchGroups = 'SearchGroups'

    def __init__(self):
        pass

    def build_params(self, action):
        params = super().build_params(action)

        params['search'] = params['ns']
        params['nocache'] = '1635253521'
        params['sortOpt'] = '0'

        return params

    def build_url(self):
        return MAIN_URL

    def contextmenu(self, activity):
        download = action.of(DownloadHandler.name, DownloadHandler.download, DownloadHandler.download,
                             activity.thumbnail, activity.state)
        cm = [(DownloadHandler.download, 'RunPlugin(%s)' % download.url())]

        item = activity.playableitem()
        item.addContextMenuItems(cm)
        return item

    def add_group(self, addonhandle, group, count):
        title = '%s (%s posts)' % (group, count)
        groupAction = action.of(EasynewsGroupHandler.name, EasynewsGroupHandler.searchGroup, title,
                                state={'group': group})
        contextmenu = self.contextmenu(groupAction)
        xbmcplugin.addDirectoryItem(addonhandle, groupAction.url(), contextmenu, isFolder=True)

    def parse(self, addonhandle, data):
        xbmc.log("Parse Data : %s" % data, 1)
        results = re.compile('<table class="grouplist"(.+?)</table>',
                             re.DOTALL).findall(data)[0]
        items = re.compile('<tr class=(.+?)</tr>',
                           re.DOTALL).findall(results)

        if items:
            for item in items:
                count = re.compile('<td class="count">(.+?)</td>',
                                   re.DOTALL).findall(item)
                count = count[0]

                group = re.compile('value="(.+?)"',
                                   re.DOTALL).findall(item)
                group = html.unescape(group[0])

                self.add_group(addonhandle, group, count)
