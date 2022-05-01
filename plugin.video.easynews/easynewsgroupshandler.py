import re, html

import xbmc, xbmcplugin

import action
import easynewssearchhandler

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

    def add_group(self, addonhandle, group, count):
        title = '%s (%s posts)' % (group , count)
        groupAction = action.of(EasynewsGroupHandler.name, EasynewsGroupHandler.searchGroup, title, state={'group':group})
        xbmcplugin.addDirectoryItem(addonhandle, groupAction.url(), groupAction.videoitem(), isFolder=True)

    def parse(self, addonhandle, data):
        xbmc.log("Parse Data : %s" % data, 1)
        results=re.compile('<table class="grouplist"(.+?)</table>',
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

