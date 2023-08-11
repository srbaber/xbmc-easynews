import os
import re

import constants
import getrequest
import properties
import xbmcgui

progressDialog = xbmcgui.DialogProgress()


#
# handler responsible for downloading content
#
class DownloadHandler():
    name = 'DownloadHandler'
    download_operation = 'Download'
    download_file = properties.get_localized_string(30300, 'Download')
    downloading = properties.get_localized_string(30301,'Downloading Easynews')
    download_complete = properties.get_localized_string(30302,'Downloading Complete')
    download_failed = properties.get_localized_string(30303, 'Download Failed')

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

        progressDialog.create(self.downloading)
        getrequest.download(self, url, fullpath, download_report_hook)
        progressDialog.close()

        if fullpath is not None and os.path.isfile(fullpath):
            title = self.download_complete
        else:
            title = self.download_failed

        xbmcgui.Dialog().ok(title, filename)


def download_report_hook(size, totalsize):
    percent = int(float(size * 100) / totalsize)
    progressDialog.update(percent)
    if progressDialog.iscanceled():
        raise KeyboardInterrupt
