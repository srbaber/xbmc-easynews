import requests
import base64
import json
import os

import xbmc, xbmcvfs

import properties
import constants

timeout = 60

def url_auth(url):
    usernm = properties.get_property('username')
    passwd = properties.get_property('password')
    return url.replace('https://', 'https://%s:%s@'% (usernm, passwd))

def stream(self, url, params, stream):
    usernm = properties.get_property('username')
    passwd = properties.get_property('password')

    response = requests.get(url, params=params, auth=(usernm, passwd), timeout=timeout, stream=stream)
    return response

def get(self, url, params={}):
    return stream(self, url, params, False).text

def download(self, url, filename, download_report_hook):
    with stream(self, url, None, True) as response:
        size = response.headers['Content-Length']
        if not size is None:
            read = 0
            size = int(size)
            chunk_size=max(int(size/1000), 1024*1024)
            filename = os.path.join(constants.DATA_PATH, filename)

            with open(filename, 'wb') as filehandle:
                for buf in response.iter_content(chunk_size):
                    if buf:
                        filehandle.write(buf)
                        read += len(buf)
                        download_report_hook(read, size)

            download_report_hook(size, size)


