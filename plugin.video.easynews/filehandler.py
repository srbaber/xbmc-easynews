import os

import action
import constants
import properties
import xbmc
import xbmcplugin


#
# handler responsible for listing downloaded content
#
class FileHandler():
    name = 'FileHandler'
    playback = 'Video'
    delete_operation = 'Delete'
    clear_operation = 'Clear'
    deletefile = properties.get_localized_string(30330, 'Delete Download')
    clearall = properties.get_localized_string(30331, 'Clear Downloads')

    def add_clear_downloads(self, addonhandle):
        historyAction = action.of(self.name, self.clear_operation, self.clearall)
        xbmcplugin.addDirectoryItem(addonhandle, historyAction.url(), historyAction.directoryitem(), isFolder=False)

    def contextmenu(self, activity):
        delete = action.of(self.name, self.delete_operation, self.deletefile, activity.thumbnail, activity.state)
        cm = [(self.deletefile, 'RunPlugin(%s)' % delete.url())]

        item = activity.playableitem()
        item.addContextMenuItems(cm)
        return item

    def add_file(self, addonhandle, filename, fullpath):
        fileAction = action.of(self.name, self.playback, filename, state={'url': fullpath})
        contextmenu = self.contextmenu(fileAction)
        contextmenu.setPath(fullpath)

        xbmcplugin.addDirectoryItem(addonhandle, fullpath, contextmenu, isFolder=False)

    def list_files(self):
        files = []
        datapath = properties.get_property('download', constants.DATA_PATH)
        for f in os.listdir(datapath):
            fullpath = os.path.join(datapath, f)
            if os.path.isfile(fullpath) and f != 'settings.xml' and f != '.DS_Store':
                files.append(f)
        return files

    def list_downloads(self, addonhandle):
        datapath = properties.get_property('download', constants.DATA_PATH)
        for f in self.list_files():
            fullpath = os.path.join(datapath, f)
            self.add_file(addonhandle, f, fullpath)

        self.add_clear_downloads(addonhandle)
        xbmcplugin.endOfDirectory(addonhandle)

    def delete_downloads(self, addonhandle):
        datapath = properties.get_property('download', constants.DATA_PATH)
        for f in self.list_files():
            fullpath = os.path.join(datapath, f)
            os.remove(fullpath)
        xbmc.executebuiltin('Container.Refresh')

    def delete_download(self, addonhandle, fullpath):
        os.remove(fullpath)
        xbmc.executebuiltin('Container.Refresh')

    def apply(self, addonhandle, activity):
        if constants.APPLY_LOG:
            xbmc.log('%s.apply %s %s' % (self.name, addonhandle, activity.tostring()), 1)

        if activity.operation == self.playback:
            self.list_downloads(addonhandle)
        elif activity.operation == self.delete_operation:
            self.delete_download(addonhandle, activity.state['url'])
        elif activity.operation == self.clear_operation:
            self.delete_downloads(addonhandle)
