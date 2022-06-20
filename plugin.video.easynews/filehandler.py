import os

import xbmc, xbmcplugin

import action
import constants
import properties

#
# handler responsible for listing downloaded content
#
class FileHandler():
    name = 'FileHandler'
    playback = 'Video'
    delete = 'Delete'
    clear = 'Clear'

    def add_clear_downloads(self, addonhandle):
        historyAction = action.of(self.name, self.clear, 'Delete Downloads')
        xbmcplugin.addDirectoryItem(addonhandle, historyAction.url(), historyAction.directoryitem(), isFolder=False)

    def add_file(self, addonhandle, filename, fullpath):
        fileAction = action.of(self.name, self.playback, filename, state={'url' : fullpath})
        item = fileAction.fileitem()
        item.setPath(fullpath)

        xbmcplugin.addDirectoryItem(addonhandle, fullpath, item, isFolder=False)

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
        xbmc.log('%s.apply %s %s' % (self.name, addonhandle, activity.tostring()), 1)

        if activity.operation == self.playback:
            self.list_downloads(addonhandle)
        elif activity.operation == self.delete:
            self.delete_download(addonhandle, activity.state['url'])
        elif activity.operation == self.clear:
            self.delete_downloads(addonhandle)

