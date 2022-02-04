import requests
import base64
import json

import xbmc, xbmcvfs

import properties

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
        xbmc.log("Stream ready %s" % size, 1)
        if size is None:
            pass
        else:
            read = 0
            size = int(size)
            chunk_size=max(int(size/1000), 1024*1024)

            with open(filename, 'wb') as filehandle:
                xbmc.log("Starting download", 1)
                for buf in response.iter_content(chunk_size):
                    if buf:
                        filehandle.write(buf)
                        read += len(buf)
                        download_report_hook(read, chunk_size, size)
                xbmc.log("Finished download", 1)

            download_report_hook(size, chunk_size, size)

    return filename

