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

# User-Agent used for playback
ios_ua = 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_1 like Mac OS X) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.0 Mobile/14E304 Safari/602.1'
USER_AGENT_STRING = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3'


def get_html(url, cookie=None, user_agent=None, referer=None, username=None, password=None):
    xbmc.log("Get Url: %s %s %s" % (url, username, password))
    d = gethtml.get(url, __datapath__, cookie=cookie, user_agent=user_agent, referer=referer, username=username, password=password)
    return six.ensure_text(d) if six.PY3 else d

def download(url, cookie=None, user_agent=None, referer=None, username=None, password=None):
    xbmc.log("Download Url: %s %s %s" % (url, username, password))
    d = gethtml.download(url, __datapath__, cookie=cookie, user_agent=user_agent, referer=referer, username=username, password=password)
    return d

def Notify(title, message, times, icon):
    xbmcgui.Dialog().notification(title, message, icon, times, False)

def getProperty(name, withDefault = None):
    usrsettings = xbmcaddon.Addon(id=__addonname__)
    value = usrsettings.getSetting(name)
    if value:
        return value
    else:
        return withDefault

def STARTUP_ROUTINES():
    # deal with bug that happens if the datapath doesn't exist
    if not os.path.exists(__datapath__):
        os.makedirs(__datapath__)

def CATEGORIES():
    groups = getProperty('groups')

    mode = 1
    addDir('Videos By Date (' + groups + ')',
           main_url + '?&ns=' + groups + '&fex=mp4&pby=500&pno=1&s1=dtime&s1d=-&s2=nrfile&s2d=-&s3=dsize&s3d=-&sS=5&d1t=&d2t=&b1t=&b2t=&px1t=&px2t=&fps1t=&fps2t=&bps1t=&bps2t=&hz1t=&hz2t=&rn1t=&rn2t=&grpF[]=&fty[]=VIDEO&spamf=1&u=1&st=adv&safeO=0&sb=1', mode, default_image)
    addDir('Videos By Size (' + groups + ')',
           main_url + '?&ns=' + groups + '&fex=mp4&pby=500&pno=1&s1=dsize&s1d=-&s2=nrfile&s2d=-&s3=dtime&s3d=-&sS=5&d1t=&d2t=&b1t=&b2t=&px1t=&px2t=&fps1t=&fps2t=&bps1t=&bps2t=&hz1t=&hz2t=&rn1t=&rn2t=&grpF[]=&fty[]=VIDEO&spamf=1&u=1&st=adv&safeO=0&sb=1', mode, default_image)

    mode = 2

    # didn't need to pass search a url. so i was lazy and passed it the
    # main_url as a dummy
    addDir('Search', main_url, 5, default_image)

    xbmc.log('pluginhandle %s' % pluginhandle)
    xbmcplugin.endOfDirectory(pluginhandle)


def SEARCH(url):
    kb = xbmc.Keyboard('', 'Search Easynews.com Videos', False)
    kb.doModal()
    if kb.isConfirmed():
        # get text from keyboard
        search = kb.getText()

        # if the search text is not nothing
        if search != '':
            # create the search url
            search_url = main_url + '?&gps=' + search + '&fex=mp4&pby=500&pno=1&s1=dsize&s1d=-&s2=nrfile&s2d=-&s3=dtime&s3d=-&sS=5&d1t=&d2t=&b1t=&b2t=&px1t=&px2t=&fps1t=&fps2t=&bps1t=&bps2t=&hz1t=&hz2t=&rn1t=&rn2t=&grpF[]=&fty[]=VIDEO&spamf=1&u=1&st=adv&safeO=0&sb=1'
            xbmc.log('SEARCH:%s' % search_url)
            INDEX(search_url)

def cleanupAutoUnrar(title):
    if title.index('AutoUnRAR'):
        title = re.sub('.+?\(', '', title)
        title = re.sub(' AutoUnRAR\)', '', title)

def INDEX(url):
    user = getProperty('username')
    passwd = getProperty('password')

    data = get_html(url, username=user, password=passwd)

    items = re.compile('<item>(.+?)</item>',
                       re.DOTALL).findall(data)
    xbmc.log("Items: %s" % items)
    if items:
        for item in items:
            title = re.compile('<title>(.+?)</title>', re.DOTALL).findall(item)
            title = html.unescape(title[0])
            title = cleanupAutoUnrar(title)
            gurl = re.compile('<link>(.+?)</link>', re.DOTALL).findall(item)
            gurl = html.unescape(gurl[0])
            addSupportedLinks(gurl, title, "easynews")

    xbmcplugin.endOfDirectory(pluginhandle)


def addSupportedLinks(gurl, name, thumbnail):
    mode = 4
    addLink(name, gurl, mode, thumbnail)
    return


def PLAY(url, thumbnail):
    user = getProperty('username')
    passwd = getProperty('password')

    xbmc.log('Download URL: %s' % url)
    vidfile = download(url, username=user, password=passwd)
    item = xbmcgui.ListItem(path=vidfile)
    result = True
    if vidfile is not None and os.path.isfile(vidfile):
        result = False

    return xbmcplugin.setResolvedUrl(pluginhandle, result, item)

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


def addLink(name, url, mode, iconimage):
    u = sys.argv[0] + "?url=" + urllib_parse.quote_plus(url) + "&mode=" + str(mode) \
        + "&name=" + urllib_parse.quote_plus(name) + "&iconimage=" \
        + urllib_parse.quote_plus(iconimage)
    ok = True
    liz = xbmcgui.ListItem(name)
    liz.setArt({'thumb': iconimage,
                'icon': 'DefaultVideo.png',
                'poster': iconimage})
    liz.setProperty('IsPlayable', 'true')
    liz.setInfo(type='Video', infoLabels={'Title': name})
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,
                                     listitem=liz)
    return ok


def addDir(name, url, mode, iconimage):
    u = sys.argv[0] + "?url=" + urllib_parse.quote_plus(url) + "&mode=" + str(mode) \
        + "&name=" + urllib_parse.quote_plus(name)
    ok = True
    liz = xbmcgui.ListItem(name)
    liz.setArt({'thumb': iconimage,
                'icon': 'DefaultVideo.png',
                'poster': iconimage})
    liz.setInfo(type='Video', infoLabels={'Title': name})
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u,
                                     listitem=liz, isFolder=True)
    return ok


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

STARTUP_ROUTINES()

if topmode is None:
    xbmc.log('Generate Main Menu')
    CATEGORIES()
elif topmode == 1:
    xbmc.log('Indexing Videos')
    INDEX(topurl)
elif topmode == 2:
    xbmc.log('Indexing Collections')
elif topmode == 3:
    xbmc.log('Indexing Personal Videos')
elif topmode == 4:
    xbmc.log('Play Video')
    PLAY(topurl, topthumbnail)
elif topmode == 5:
    xbmc.log('Category: Search')
    SEARCH(topurl)

xbmcplugin.endOfDirectory(int(sys.argv[1]))
