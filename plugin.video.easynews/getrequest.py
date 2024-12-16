import os
import re
import html

import requests

import constants
import properties
import xbmc

timeout = 60
session_id_cookie = 'ENSESSID'


def url_auth(url, session_id=None):
    user_name = properties.get_property('username')
    passwd = properties.get_property('password')

    # strip old values if present
    authorized_url = html.escape(url, quote=False)
    authorized_url = re.sub('^https://.*@', 'https://', authorized_url)
    authorized_url = re.sub('\|' + session_id_cookie + '=.*$', '', authorized_url)
    authorized_url = html.unescape(authorized_url)

    # add the username, password, and session id
    authorized_url = re.sub('^https://', 'https://%s:%s@' % (user_name, passwd), authorized_url)
    if session_id is not None:
        return authorized_url + '|' + session_id_cookie + '=' + session_id
    else:
        return authorized_url


def stream(url, params, data_stream):
    user_name = properties.get_property('username')
    passwd = properties.get_property('password')

    if constants.REQUEST_LOG:
        xbmc.log('%s.stream %s %s' % ('getRequest', url, params), 1)

    response = requests.get(url, params=params, auth=(user_name, passwd), timeout=timeout, stream=data_stream)
    return response


def submit(url, params, data_stream):
    if constants.REQUEST_LOG:
        xbmc.log('%s.submit %s %s' % ('getRequest', url, params), 1)

    user_name = properties.get_property('username')
    passwd = properties.get_property('password')

    response = requests.post(url, data=params, auth=(user_name, passwd), timeout=timeout, stream=data_stream)
    return response


def get(url, params=None):
    if params is None:
        params = {}
    return stream(url, params, False)


def post(url, params=None):
    if params is None:
        params = {}
    return submit(url, params, False)


def download(url, filename, download_report_hook):
    with stream(url, None, True) as response:
        size = response.headers['Content-Length']
        if size is not None:
            read = 0
            size = int(size)
            chunk_size = max(int(size / 1000), 1024 * 1024)
            filename = os.path.join(constants.DATA_PATH, filename)

            with open(filename, 'wb') as filehandle:
                for buf in response.iter_content(chunk_size):
                    if buf:
                        filehandle.write(buf)
                        read += len(buf)
                        download_report_hook(read, size)

            download_report_hook(size, size)
