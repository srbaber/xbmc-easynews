import html
import re

import action
import constants
import easynewssearchhandler
import getrequest
import properties
import xbmc
import xbmcplugin
from downloadhandler import DownloadHandler

MAIN_URL = 'https://members.easynews.com/2.0/tools/zip-manager'

#
# handler responsible for build the zip manager menu
#
class EasynewsZipManagerHandler(easynewssearchhandler.EasynewsSearchHandler):
    name = 'EasynewsZipManagerHandler'

    list_queue_operation = 'ListQueue'
    list_queues_operation = 'ListQueues'
    delete_operation = 'Delete'
    clear_operation = 'Clear'
    deletefile = properties.get_localized_string(30320, 'Remove From Queue')
    clearall = properties.get_localized_string(30321, 'Clear Queue')

    def build_url(self):
        return MAIN_URL

    def build_params(self, action):
        params = {}
        params['editzip'] = action.state['queue']

        return params

    def contextmenu(self, activity):
        items = []
        remove = action.of(self.name, self.delete_operation, self.deletefile, activity.thumbnail, activity.state)
        items.append ((self.deletefile, 'RunPlugin(%s)' % remove.url()))

        download = action.of(DownloadHandler.name, DownloadHandler.download_operation, DownloadHandler.download_file,
                             activity.thumbnail, activity.state)
        items.append((DownloadHandler.download_file, 'RunPlugin(%s)' % download.url()))

        item = activity.playableitem()
        item.addContextMenuItems(items)
        return item

    def add_queue_item(self, addonhandle, title, thumbnail, gurl, state):
        videoAction = action.of(self.name, self.playbackOperation, title, thumbnail, state)
        contextmenu = self.contextmenu(videoAction)
        xbmcplugin.addDirectoryItem(addonhandle, gurl, contextmenu, isFolder=False)

    def parse_queue(self, addonhandle, data, queue):
        items = re.compile('<tr class="rRow(.+?)</tr>', re.DOTALL).findall(data)
        if items:
            for item in items:
                title = re.compile('target="fileTarget" >(.+?)</a>', re.DOTALL).findall(item)
                title = html.unescape(title[0])
                title = self.cleanup_title(title)

                gurl = re.compile('<a href="(.+?)" target="fileTarget" >', re.DOTALL).findall(item)
                gurl = html.unescape(gurl[0])

                thumbnail = self.build_thumbnail_url(gurl)

                gurl = getrequest.url_auth(gurl)

                sig = re.compile('name="(.+?)" value=', re.DOTALL).findall(item)
                sig = html.unescape(sig[0])

                val = re.compile('value="(.+?)"', re.DOTALL).findall(item)
                val = html.unescape(val[0])

                state = {
                    'url': gurl,
                    'sig': sig,
                    'val': val,
                    'queue': queue
                }

                self.add_queue_item(addonhandle, title, thumbnail, gurl, state)

    def clear_queues_menu(self, addonhandle, queuename):
        clearAction = action.of(EasynewsZipManagerHandler.name, EasynewsZipManagerHandler.clear_operation,
                                EasynewsZipManagerHandler.clearall,
                                state={'queue': queuename})
        xbmcplugin.addDirectoryItem(addonhandle, clearAction.url(), clearAction.directoryitem(), isFolder=False)

    def add_zip_queue(self, addonhandle, title, queuename):
        queueAction = action.of(EasynewsZipManagerHandler.name, EasynewsZipManagerHandler.list_queue_operation, title,
                                state={'queue': queuename})
        xbmcplugin.addDirectoryItem(addonhandle, queueAction.url(), queueAction.directoryitem(), isFolder=True)

    def list_queues_menu(self, addonhandle):
        self.add_zip_queue(addonhandle, 'Unqueued Files', 'Z')
        for queuenumber in range(1, 11):
            title = 'Queue %02d' % queuenumber
            queuename = 'Q%02d' % queuenumber
            self.add_zip_queue(addonhandle, title, queuename)

    def search(self, action):
        return getrequest.get(self, self.build_url(), self.build_params(action))

    def clear_queue(self, action):
        formdata = {}
        formdata['clearzip'] = action.state['queue']

        getrequest.get(self, self.build_url(), formdata)

    def delete(self, action):
        formdata = {}
        formdata['editque'] = action.state['queue']
        formdata[action.state['sig']] = action.state['val']
        formdata['DEL'] = 'Remove Checked Files'

        xbmc.log('%s.delete %s' % (self.name, formdata), 1)

        getrequest.post(self, self.build_url(), formdata)

    def apply(self, addonhandle, activity):
        if constants.APPLY_LOG:
            xbmc.log('%s.apply %s %s' % (self.name, addonhandle, activity.tostring()), 1)

        if activity.operation == self.list_queue_operation:
            response = self.search(activity)
            self.parse_queue(addonhandle, response, activity.state['queue'])
            self.clear_queues_menu(addonhandle, activity.state['queue'])
        elif activity.operation == self.delete_operation:
            self.delete(activity)
            xbmc.executebuiltin('Container.Refresh')
        elif activity.operation == self.clear_operation:
            self.clear_queue(activity)
            xbmc.executebuiltin('Container.Refresh')
        else:
            self.list_queues_menu(addonhandle)

        xbmcplugin.endOfDirectory(addonhandle)


def sort_by_title(videoAction):
    return videoAction['title']
