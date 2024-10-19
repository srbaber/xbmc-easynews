import os

import action
import constants
import properties
import xbmc
import re
import xbmcplugin


#
# handler responsible for listing downloaded content
#
class FileHandler:
    name = 'FileHandler'
    playback = 'Video'
    delete_operation = 'Delete'
    clear_operation = 'Clear'
    delete_file = properties.get_localized_string(30330, 'Delete Download')
    clear_all = properties.get_localized_string(30331, 'Clear Downloads')

    def add_clear_downloads(self, addon_handle):
        history_action = action.of(self.name, self.clear_operation, self.clear_all)
        xbmcplugin.addDirectoryItem(addon_handle, history_action.url(), history_action.directory_item(), isFolder=False)

    def add_context_menu(self, activity):
        delete = action.of(self.name, self.delete_operation, self.delete_file, activity.thumbnail, activity.state)
        cm = [(self.delete_file, 'RunPlugin(%s)' % delete.url())]

        item = activity.playable_item()
        item.addContextMenuItems(cm)
        return item

    def add_file(self, addon_handle, filename, fullpath):
        file_action = action.of(self.name, self.playback, filename, state={'url': fullpath})
        list_item = self.add_context_menu(file_action)
        file_action.directory_item().setPath(fullpath)

        xbmcplugin.addDirectoryItem(addon_handle, fullpath, list_item, isFolder=False)

    def list_downloads(self, addon_handle):
        datapath = properties.get_property('download', constants.DATA_PATH)
        for f in list_files():
            fullpath = os.path.join(datapath, f)
            self.add_file(addon_handle, f, fullpath)

        self.add_clear_downloads(addon_handle)
        xbmcplugin.endOfDirectory(addon_handle)

    def apply(self, addon_handle, activity):
        if constants.APPLY_LOG:
            xbmc.log('%s.apply %s %s' % (self.name, addon_handle, activity.tostring()), 1)

        if activity.operation == self.playback:
            self.list_downloads(addon_handle)
        elif activity.operation == self.delete_operation:
            delete_download(activity.state['url'])
        elif activity.operation == self.clear_operation:
            delete_downloads()


def extract_filename(url):
    filename = re.sub('^.*/', '', url)
    filename = re.sub('\?.*', '', filename)
    return filename


def list_files():
    files = []
    datapath = properties.get_property('download', constants.DATA_PATH)
    for f in os.listdir(datapath):
        fullpath = os.path.join(datapath, f)
        if os.path.isfile(fullpath) and f != 'settings.xml' and f != '.DS_Store':
            files.append(f)
    return files


def delete_downloads():
    datapath = properties.get_property('download', constants.DATA_PATH)
    for f in list_files():
        fullpath = os.path.join(datapath, f)
        os.remove(fullpath)
    xbmc.executebuiltin('Container.Refresh')


def delete_download(fullpath):
    os.remove(fullpath)
    xbmc.executebuiltin('Container.Refresh')
