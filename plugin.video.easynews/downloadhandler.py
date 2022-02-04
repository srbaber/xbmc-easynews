import re,os

import xbmc, xbmcplugin, xbmcgui

import action
import constants
import getrequest

progressDialog = xbmcgui.DialogProgress()

#
# handler responsible for downloading content
#
class DownloadHandler():
    name = 'DownloadHandler'
    download = 'Download'
    delete = 'Delete'

    def __init__(self):
        pass

    def extract_filename(self, url):
        filename = re.sub('^.*/', '', url)
        filename = re.sub('\?.*', '', filename)
        return filename

    def apply(self, addonhandle, activity):
        xbmc.log('%s.apply %s %s' % (self.name, addonhandle, activity.tostring()), 1)

        url = activity.state['url']
        filename = self.extract_filename(url)

        progressDialog.create('Easynews Downloading')
        fullpath = getrequest.download(self, url, filename, download_report_hook)
        progressDialog.close()

        if fullpath is not None and os.path.isfile(fullpath):
            title = 'Download Complete'
        else:
            title = 'Download Failed'

        xbmcgui.Dialog().ok(title, filename)

def download_report_hook(size, totalsize):
    percent = int(float(size * 100) / totalsize)
    progressDialog.update(percent)
    if progressDialog.iscanceled():
        raise KeyboardInterrupt