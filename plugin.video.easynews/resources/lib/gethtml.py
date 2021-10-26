'''
gethtml with cookies support  v1
by anarchintosh @ xbmcforums
Copyleft = GNU GPL v3 (2011 onwards)

import gethtml

to load html without cookies
source = gethtml.get(url)

to load html with cookies
source = gethtml.get(url, 'my-path-to-cookiefile')
'''

from six.moves import urllib_request, urllib_error, http_cookiejar
import os
import re
import sys
import tempfile
from kodi_six import xbmc, xbmcgui, xbmcvfs

# !!!!!!!!!!! Please set the compatible_urllist
# set the list of URLs you want to load with cookies.
# matches bits of url, so that if you want to match www243.megaupload.com/ you
# can just put '.megaupload.com/' in the list.
compatible_urllist = ['.easynews.com']

USER_AGENT_STRING = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

VIDEO_EXTENSION = '.mp4'

progressDialog = xbmcgui.DialogProgress()

def url_for_cookies(url):
    # ascertain if the url contains any of the phrases in the list. return True
    # if a match is found.
    for compatible_url in compatible_urllist:
        if re.search(compatible_url, url):
            url_is_compatible = True
            break
        else:
            url_is_compatible = False
    return url_is_compatible

def make_cookie(name, value):
        return http_cookiejar.Cookie(
            version=0,
            name=name,
            value=value,
            port=None,
            port_specified=False,
            domain=compatible_urllist[0],
            domain_specified=True,
            domain_initial_dot=False,
            path="/",
            path_specified=True,
            secure=False,
            expires=None,
            discard=False,
            comment=None,
            comment_url=None,
            rest={},
        )

def createOpener(cookiepath, username, password):
    # check if user has supplied only a folder path, or a full path
    if not os.path.isfile(cookiepath):
        # if the user supplied only a folder path, append on to the end
        # of the path a common filename.
        cookiepath = os.path.join(cookiepath, 'cookies.moz')

    # check that the cookie exists
    cj = http_cookiejar.MozillaCookieJar()
    if os.path.exists(cookiepath):
        cj.load(cookiepath)
    cj.set_cookie(make_cookie(name="chickenlicker", value="noahbuddy:sh1tface"))
    cj.set_cookie(make_cookie(name="c_f", value="5Q4kjKmsz%2FmGtZIDLQBmwse%2BNWvZz9KddfBc19Jc7Q4tpQYKKngPZtCLBTlZSonihNLkujDLAuguV4Ug%2BCcgASrRL13mouk9jXocCziCYk9zvdi5XV%2ByZK3O9puyucMuosQlhoPYznF2ozIjQdQMk34clW55KuozQl2caDhBPtc%3D"))
    cj.save(cookiepath)

    # create a password manager
    password_mgr = urllib_request.HTTPPasswordMgrWithDefaultRealm()
    urllib_request.HTTPBasicAuthHandler(password_mgr),

    if username and password:
        top_level_url = 'easynews.com'
        password_mgr.add_password(None, top_level_url, username, password)

    return urllib_request.build_opener(urllib_request.HTTPCookieProcessor(cj), urllib_request.HTTPBasicAuthHandler(password_mgr))

def createRequest(url, cookie, user_agent, referer):
    req = urllib_request.Request(url)
    if user_agent:
        req.add_header('User-Agent', user_agent)
    else:
        req.add_header('User-Agent', USER_AGENT_STRING)
    if referer:
        req.add_header('Referer', referer)
    if cookie:
        req.add_header('Cookie', cookie)

    return req

def stream(url, cookiepath=None, cookie=None, user_agent=None, referer=None, username=None, password=None):
    # use cookies if cookiepath is set and if the cookiepath exists.
    if cookiepath is not None:
        req = createRequest(url, cookie, user_agent, referer)
        opener = createOpener(cookiepath, username, password)

        try:
            response = opener.open(req)
        except urllib_error.URLError as e:
            xbmc.log('%s Error opening %s' % (e, url))
            sys.exit(1)
        return response
    else:
        return load_without_cookies(url, user_agent)

def get(url, cookiepath=None, cookie=None, user_agent=None, referer=None, username=None, password=None):
    link = stream()
    link = response.read()
    response.close()
    return link

def load_without_cookies(url, user_agent):
    xbmc.log('Loading without cookies')
    url = url.replace('http:', 'https:')

    req = createRequest(url, None, user_agent, referer)

    try:
        response = urllib_request.urlopen(req)
    except urllib_error.HTTPError as e:
        xbmc.log("%s %s" % (url, e.reason), xbmc.LOGFATAL)
        sys.exit(0)
    return response

def download(url, cookiepath=None, cookie=None, user_agent=None, referer=None, username=None, password=None):
    tmp_file = os.path.join(cookiepath, 'easynews' + VIDEO_EXTENSION)
    tmp_file = xbmcvfs.makeLegalFilename(tmp_file)

    # use cookies if cookiepath is set and if the cookiepath exists.
    if cookiepath is not None:
        progressDialog.create('Easynews')

        req = createRequest(url, cookie, user_agent, referer)
        opener = createOpener(cookiepath, username, password)
        urllib_request.install_opener(opener)

        try:
            urllib_request.urlretrieve(url,
                                   tmp_file,
                                   video_report_hook)
        except:
            xbmc.log('Download aborted')
            tmp_file=None

        progressDialog.close()
        return tmp_file

def clean_filename(s):
    if not s:
        return ''
    badchars = '\\/:*?\"<>|'
    return s.strip(badchars)


def video_report_hook(count, blocksize, totalsize):
    percent = int(float(count * blocksize * 100) / totalsize)
    progressDialog.update(percent)
    if progressDialog.iscanceled():
        raise KeyboardInterrupt