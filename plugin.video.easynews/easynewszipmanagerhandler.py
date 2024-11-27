import html
import re

import action
import constants
import getrequest
import properties
import xbmc
import xbmcplugin
from downloadhandler import DownloadHandler
from easynewssearchhandler import EasynewsSearchHandler, cleanup_title, go_to_main_menu

MAIN_URL = 'https://members.easynews.com/2.0/tools/zip-manager'


#
# handler responsible for building the zip manager menu
#
class EasynewsZipManagerHandler(EasynewsSearchHandler):
    name = 'EasynewsZipManagerHandler'

    list_queue_operation = 'ListQueue'
    list_queues_operation = 'ListQueues'
    delete_operation = 'Delete'
    clear_operation = 'Clear'
    delete_file = properties.get_localized_string(30320, 'Remove From Queue')
    clear_all = properties.get_localized_string(30321, 'Clear Queue')

    def build_url(self, activity):
        return MAIN_URL

    def build_params(self, activity):
        params = {'editzip': activity.state['queue']}

        return params

    def add_context_menu(self, activity):
        items = []
        remove = action.of(self.name, self.delete_operation, self.delete_file, activity.thumbnail, activity.state)
        items.append((self.delete_file, 'RunPlugin(%s)' % remove.url()))

        download = action.of(DownloadHandler.name, DownloadHandler.download_operation, DownloadHandler.download_file,
                             activity.thumbnail, activity.state)
        items.append((DownloadHandler.download_file, 'RunPlugin(%s)' % download.url()))

        item = activity.playable_item()
        item.addContextMenuItems(items)
        return item

    def add_queue_item(self, addon_handle, title, thumbnail, gurl, state):
        video_action = action.of(self.name, self.playbackOperation, title, thumbnail, state)
        list_item = self.add_context_menu(video_action)
        xbmcplugin.addDirectoryItem(addon_handle, gurl, list_item, isFolder=False)

    def parse_queue(self, addon_handle, data, queue):
        items = re.compile('<tr class="rRow(.+?)</tr>', re.DOTALL).findall(data)
        if items:
            for item in items:
                title = re.compile('target="fileTarget" >(.+?)</a>', re.DOTALL).findall(item)
                title = html.unescape(title[0])
                title = cleanup_title(title)

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

                self.add_queue_item(addon_handle, title, thumbnail, gurl, state)

    def search(self, activity):
        return getrequest.get(self.build_url(activity), self.build_params(activity))

    def clear_queue(self, activity):
        form_data = {'clearzip': activity.state['queue']}
        getrequest.get(self.build_url(activity), form_data)

    def delete(self, activity):
        form_data = {'editque': activity.state['queue'],
                     activity.state['sig']: activity.state['val'],
                     'DEL': 'Remove Checked Files'}

        # xbmc.log('%s.delete %s' % (self.name, form_data), 1)
        getrequest.post(self.build_url(activity), form_data)

    def apply(self, addon_handle, activity):
        if constants.APPLY_LOG:
            xbmc.log('%s.apply %s %s' % (self.name, addon_handle, activity.tostring()), 1)

        if check_for_invalid_user_id(addon_handle):
            go_to_main_menu(addon_handle)
            return

        if activity.operation == self.list_queue_operation:
            response = self.search(activity)
            self.parse_queue(addon_handle, response, activity.state['queue'])
            clear_queues_menu(addon_handle, activity.state['queue'])
        elif activity.operation == self.delete_operation:
            self.delete(activity)
            xbmc.executebuiltin('Container.Refresh')
        elif activity.operation == self.clear_operation:
            self.clear_queue(activity)
            xbmc.executebuiltin('Container.Refresh')
        else:
            list_queues_menu(addon_handle)

        xbmcplugin.endOfDirectory(addon_handle)


def clear_queues_menu(addon_handle, queue_name):
    clear_action = action.of(EasynewsZipManagerHandler.name, EasynewsZipManagerHandler.clear_operation,
                             EasynewsZipManagerHandler.clear_all,
                             state={'queue': queue_name})
    xbmcplugin.addDirectoryItem(addon_handle, clear_action.url(), clear_action.directory_item(), isFolder=False)


def add_zip_queue(addon_handle, title, queue_name):
    queue_action = action.of(EasynewsZipManagerHandler.name, EasynewsZipManagerHandler.list_queue_operation, title,
                             state={'queue': queue_name})
    xbmcplugin.addDirectoryItem(addon_handle, queue_action.url(), queue_action.directory_item(), isFolder=True)


def list_queues_menu(addon_handle):
    add_zip_queue(addon_handle, 'Unqueued Files', 'Z')
    for queue_number in range(1, 11):
        title = 'Queue %02d' % queue_number
        queue_name = 'Q%02d' % queue_number
        add_zip_queue(addon_handle, title, queue_name)
