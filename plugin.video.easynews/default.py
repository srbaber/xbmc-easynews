#!/usr/bin/python
# Code Heavily modified from  Demo by TV DASH - by You 2008.
#
# Written by Ksosez with help from anarchintosh
# Released under GPL(v2)
# Adapted to easynews by Stevie B

from __future__ import absolute_import
import six
from six.moves import urllib_parse, range
import html
import re
import json
import os
import sys
from kodi_six import xbmcplugin, xbmcaddon, xbmcgui, xbmc, xbmcvfs


# python 2 and 3 compatibility defs
TRANSLATEPATH = xbmcvfs.translatePath if six.PY3 else xbmc.translatePath

# addon name
__addonname__ = 'plugin.video.easynews'

# get path the default.py is in.
__addonpath__ = xbmcaddon.Addon(id=__addonname__).getAddonInfo('path')

# datapath
__datapath__ = TRANSLATEPATH('special://profile/addon_data/' + __addonname__)

# append lib directory
sys.path.append(os.path.join(__addonpath__, 'resources', 'lib'))

# import from lib directory
import gethtml


pluginhandle = int(sys.argv[1])

# example of how to get path to an image
default_image = os.path.join(__addonpath__, 'resources', 'images',
                             'provocative_logo.png')

# string to simplify urls
main_url = 'https://secure.members.easynews.com/global5/search.html'
groups_url = 'https://secure.members.easynews.com/index.html'

# User-Agent used for playback
ios_ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'
USER_AGENT_STRING = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'

DEFAULT_EXTENSION = '.mp4'

SORT_BY_SIZE = 'dsize'
SORT_BY_NAME = 'nrfile'
SORT_BY_DATE = 'dtime'
GROUP_TOKEN = 'YOURGROUPHERE'
EXTENSION_TOKEN = 'YOUREXTENSIONSHERE'
PERPAGE_TOKEN = 'YOURPERPAGESHERE'

def get_html(url, cookie=None, user_agent=None, referer=None, username=None, password=None):
    xbmc.log("Get Url: %s %s %s" % (url, username, password))
    d = gethtml.get(url, __datapath__, cookie=cookie, user_agent=user_agent, referer=referer, username=username, password=password)
    return six.ensure_text(d) if six.PY3 else d

def stream(url, cookie=None, user_agent=None, referer=None, username=None, password=None):
    xbmc.log("Stream Url: %s %s %s" % (url, username, password))
    d = gethtml.stream(url, __datapath__, cookie=cookie, user_agent=user_agent, referer=referer, username=username, password=password)
    return d

def download(url, cookie=None, user_agent=None, referer=None, username=None, password=None):
    xbmc.log("Download Url: %s %s %s" % (url, username, password))
    d = gethtml.download(url, __datapath__, cookie=cookie, user_agent=user_agent, referer=referer, username=username, password=password)
    return d

def onNotification(self, sender, method, data):
    if method in ['System.OnQuit', 'System.OnRestart', 'System.OnSleep']:
        xbmc.log("Shutdown Cleanup")

def notify(title, message, times, icon):
    xbmcgui.Dialog().notification(title, message, icon, times, False)

def get_property(name, withDefault = None):
    usrsettings = xbmcaddon.Addon(id=__addonname__)
    value = usrsettings.getSetting(name)
    if value:
        return value
    else:
        return withDefault

def startup():
    # deal with bug that happens if the datapath doesn't exist
    if not os.path.exists(__datapath__):
        os.makedirs(__datapath__)

def build_url_groups(groups = None):
    xbmc.log('Groups: %s' % (groups))
    url = groups_url + '?nocache=1635253521&sortOpt=0'
    if groups != None:
        url += '&search=' + urllib_parse.quote_plus(groups)
    return url

def build_url_sorting(url, idx, sort, sortdesc):
    url += '&s%d=' % idx + sort
    if sortdesc:
        url += '&s%dd=-' % idx
    else:
        url += '&s%dd=+' % idx
    return url

def build_url(search = None, groups = None, extensions = None, sort1 = SORT_BY_SIZE, sort1desc = True, sort2 = SORT_BY_NAME, sort2desc = True, sort3 = SORT_BY_DATE, sort3desc = True, page = "1", perpage = None):
    xbmc.log('Search: %s Groups: %s Extensions: %s' % (search, groups, extensions))

    url = main_url + '?'
    if search != None:
        url += '&gps=' + urllib_parse.quote_plus(search)
    if groups != None:
        url += '&ns=' + urllib_parse.quote_plus(groups)
    if extensions == None:
        extensions = EXTENSION_TOKEN
    if extensions == '':
        extensions = DEFAULT_EXTENSION
    if perpage == None:
        perpage = PERPAGE_TOKEN
    if perpage == '':
        perpage = 5

    url += '&fex=' + urllib_parse.quote_plus(extensions)
    url += '&pby=' + urllib_parse.quote_plus(perpage)
    url += '&pno=' + page
    url = build_url_sorting(url, 1, sort1, sort1desc)
    url = build_url_sorting(url, 2, sort2, sort2desc)
    url = build_url_sorting(url, 3, sort3, sort3desc)
    url += '&sS=5&d1t=&d2t=&b1t=&b2t=&px1t=&px2t=&fps1t=&fps2t=&bps1t=&bps2t=&hz1t=&hz2t=&rn1t=&rn2t=&grpF[]=&fty[]=VIDEO&spamf=1&u=1&st=adv&safeO=0&sb=1'
    return url

def replace_url_tokens(url):
    url = url.replace(EXTENSION_TOKEN, get_property('extensions'))
    url = url.replace(GROUP_TOKEN, get_property('groups'))
    url = url.replace(PERPAGE_TOKEN, get_property('perpage'))
    return url

def build_nextpage_url(url):
    idx = url.find('&pno=') + 5
    end_idx = url.find('&', idx)
    next_page = url[idx:end_idx]
    next_page = int(next_page) + 1
    next_url="%s%d%s" % (url[0:idx], next_page, url[end_idx:])
    xbmc.log("Next Url: %s" % next_url)
    return next_url


def build_thumbnail_url (url):
    thumb_url = 'https://th.easynews.com/thumbnails-'
    thumb_url += url[40 : 43]
    thumb_url += '/pr-'
    thumb_url += url[40 : 81]
    thumb_url += '.jpg/th-'
    thumb_url += url[90 : url.index('?', 91) - 4]
    thumb_url += '.jpg'
    xbmc.log("Url      : %s" % url)
    xbmc.log("Thumbnail: %s" % thumb_url)
    return thumb_url

def CATEGORIES():
    mode = 1
    add_dir('Videos By Date',
        build_url(groups = GROUP_TOKEN, sort1 = SORT_BY_DATE, sort3 = SORT_BY_SIZE),
        mode,
        default_image)
    add_dir('Videos By Size',
        build_url(groups = GROUP_TOKEN),
        mode,
        default_image)

    mode = 2

    # didn't need to pass search a url. so i was lazy and passed it the
    # main_url as a dummy
    add_dir('Search', main_url, 5, default_image)

    mode = 3

    add_dir('Groups',
        build_url_groups(groups = GROUP_TOKEN),
        mode,
        default_image)

    xbmc.log('pluginhandle %s' % pluginhandle)
    xbmcplugin.endOfDirectory(pluginhandle)


def GROUPS(url):
    user = get_property('username')
    passwd = get_property('password')

    url = replace_url_tokens(url)
    data = get_html(url, username=user, password=passwd)

    mode = 1

    results=re.compile('<table class="grouplist"(.+?)</table>',
                    re.DOTALL).findall(data)[0]
    items = re.compile('<tr class=(.+?)</tr>',
                    re.DOTALL).findall(results)

    if items:
        for item in items:
            count = re.compile('<td class="count">(.+?)</td>',
                  re.DOTALL).findall(item)
            count = count[0]

            group = re.compile('value="(.+?)"',
                    re.DOTALL).findall(item)
            group = html.unescape(group[0])

            xbmc.log('Group : %s %s' % (count, group))

            add_dir('%s (%s)' % (group , count),
                build_url(groups = group),
                mode,
                default_image)

    xbmcplugin.endOfDirectory(pluginhandle)

def SEARCH(url):
    kb = xbmc.Keyboard('', 'Search Easynews.com Videos', False)
    kb.doModal()
    if kb.isConfirmed():
        # get text from keyboard
        searchPhrase = kb.getText()

        # if the search text is not nothing
        if searchPhrase != '':
            # create the search url
            search_url = build_url(search = searchPhrase)
            xbmc.log('SEARCH:%s' % search_url)
            INDEX(search_url)

def cleanup_title(title):
    xbmc.log("Title: %s" % title)
    if title.find('AutoUnRAR') >= 0:
        title = re.sub('.*\) [0-9]* \(', '', title)
        title = re.sub(' AutoUnRAR\)', '', title)

    return title

def INDEX(url):
    user = get_property('username')
    passwd = get_property('password')

    url = replace_url_tokens(url)
    data = get_html(url, username=user, password=passwd)

    items = re.compile('<item>(.+?)</item>',
                       re.DOTALL).findall(data)
    if items:
        for item in items:
            title = re.compile('<title>(.+?)</title>', re.DOTALL).findall(item)
            title = html.unescape(title[0])
            title = cleanup_title(title)

            gurl = re.compile('<link>(.+?)</link>', re.DOTALL).findall(item)
            gurl = html.unescape(gurl[0])

            thumbnail = build_thumbnail_url (gurl)

            add_supported_link(gurl, title, thumbnail)

    add_dir('Next page', build_nextpage_url(url), 1, default_image)

    return xbmcplugin.endOfDirectory(pluginhandle)

def DOWNLOAD(url, thumbnail):
    user = get_property('username')
    passwd = get_property('password')

    vidfile = download(url, username=user, password=passwd)
    result = True
    if vidfile is not None and os.path.isfile(vidfile):
        result = False
    item = xbmcgui.ListItem(path=vidfile)

    return xbmcplugin.setResolvedUrl(pluginhandle, result, item)

def PLAY(url, thumbnail):
    user = get_property('username')
    passwd = get_property('password')

    url = url.replace('https://', 'https://%s:%s@'% (user, passwd))
    item = xbmcgui.ListItem(path=url)

    return xbmcplugin.setResolvedUrl(pluginhandle, True, item)

def get_params():
    param = {}
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if params[len(params) - 1] == '/':
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]
    return param

def add_supported_link(gurl, name, thumbnail):
    mode = 4
    add_link(name, gurl, mode, thumbnail)

def add_link(name, url, mode, iconimage):
    u = sys.argv[0] + "?url=" + urllib_parse.quote_plus(url) + "&mode=" + str(mode) \
        + "&name=" + urllib_parse.quote_plus(name) + "&iconimage=" \
        + urllib_parse.quote_plus(iconimage)
    liz = xbmcgui.ListItem(name)
    liz.setArt({'thumb': iconimage,
                'icon': 'DefaultVideo.png',
                'poster': iconimage})
    liz.setProperty('IsPlayable', 'true')
    liz.setInfo(type='Video', infoLabels={'Title': name})
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,
                                     listitem=liz)

def add_dir(name, url, mode, iconimage):
    u = sys.argv[0] + "?url=" + urllib_parse.quote_plus(url) + "&mode=" + str(mode) \
        + "&name=" + urllib_parse.quote_plus(name)
    liz = xbmcgui.ListItem(name)
    liz.setArt({'thumb': iconimage,
                'icon': 'DefaultVideo.png',
                'poster': iconimage})
    liz.setInfo(type='Video', infoLabels={'Title': name})
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,
                                     listitem=liz, isFolder=True)

topparams = get_params()
topurl = None
topname = None
topmode = None
topthumbnail = None

try:
    topurl = urllib_parse.unquote_plus(topparams['url'])
except:
    pass
try:
    topname = urllib_parse.unquote_plus(topparams['name'])
except:
    pass
try:
    topmode = int(topparams['mode'])
except:
    pass

try:
    topthumbnail = urllib_parse.unquote_plus(topparams['iconimage'])
except:
    pass

xbmc.log('Mode: ' + str(topmode))
xbmc.log('URL: ' + str(topurl))
xbmc.log('Name: ' + str(topname))

startup()

if topmode is None:
    xbmc.log('Generate Main Menu')
    CATEGORIES()
elif topmode == 1:
    xbmc.log('Indexing Videos')
    INDEX(topurl)
elif topmode == 2:
    xbmc.log('Indexing Collections')
elif topmode == 3:
    xbmc.log('Indexing Groups')
    GROUPS(topurl)
elif topmode == 4:
    xbmc.log('Play Video')
    PLAY(topurl, topthumbnail)
elif topmode == 5:
    xbmc.log('Category: Search')
    SEARCH(topurl)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
