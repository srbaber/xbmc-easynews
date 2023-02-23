import re,os

import constants
import xbmcgui

import getrequest
import properties

progressDialog = xbmcgui.DialogProgress()

#
# handler responsible for downloading content
#
class DownloadHandler():
    name = 'DownloadHandler'
    download = 'Download'

    def __init__(self):
        pass

    def extract_filename(self, url):
        filename = re.sub('^.*/', '', url)
        filename = re.sub('\?.*', '', filename)
        return filename

    def apply(self, addonhandle, activity):
        url = activity.state['url']
        filename = self.extract_filename(url)
        datapath = properties.get_property('download', constants.DATA_PATH)
        fullpath = os.path.join(datapath, filename)

        progressDialog.create('Easynews Downloading')
        getrequest.download(self, url, fullpath, download_report_hook)
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