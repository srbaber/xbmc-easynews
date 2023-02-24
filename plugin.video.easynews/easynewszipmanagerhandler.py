import xbmc, xbmcplugin

import action, constants, getrequest, re, html
import easynewssearchhandler

MAIN_URL = 'https://members.easynews.com/2.0/tools/zip-manager/index.html'
REMOVE_URL = 'https://members.easynews.com/2.0/tools/zip-manager'

#
# handler responsible for build the zip manager menu
#
class EasynewsZipManagerHandler(easynewssearchhandler.EasynewsSearchHandler):
    name = 'EasynewsZipManagerHandler'

    listQueue = 'ListQueue'
    listQueues = 'ListQueues'
    remove = 'Remove From Queue'

    def __init__(self):
        pass

    def build_url(self):
        return MAIN_URL

    def build_params(self, action):
        params = {}
        params['editzip'] = action.state['queue']
        return params

    def zipitem(self, videoAction):
        remove = action.of(self.name, self.remove, self.remove, videoAction.thumbnail, videoAction.state)
        cm = [(self.remove, 'RunPlugin(%s)' % remove.url())]

        item = videoAction.playableitem()
        item.addContextMenuItems(cm)
        return item

    def add_video(self, addonhandle, videoItem):
        state = {
            'url': videoItem['gurl'],
            'sig': videoItem['sig'],
            'val': videoItem['val'],
            'queue': videoItem['queue']
        }
        videoAction = action.of(self.name, self.playbackOperation, videoItem['title'], videoItem['thumbnail'], state)
        item = self.zipitem(videoAction)

        xbmcplugin.addDirectoryItem(addonhandle, videoItem['gurl'], item, isFolder=False)

    def add_zip_queue(self, addonhandle, title, queuename):
        queueAction = action.of(EasynewsZipManagerHandler.name, EasynewsZipManagerHandler.listQueue, title, state={'queue':queuename})
        xbmcplugin.addDirectoryItem(addonhandle, queueAction.url(), queueAction.directoryitem(), isFolder=True)

    def list_queues_menu(self, addonhandle):
        self.add_zip_queue(addonhandle, 'Unqueued Files', 'Z')
        for queuenumber in range (1,11):
            title = 'Queue %02d' % queuenumber
            queuename = 'Q%02d' % queuenumber
            self.add_zip_queue(addonhandle, title, queuename)

    def search(self, action):
        return getrequest.get(self, self.build_url(), self.build_params(action))

    def delete(self, action):
        params = self.build_params(action)
        params[action.state['sig']] = action.state['val']
        params['DEL'] = 'Remove+Checked+Files'
        return getrequest.get(self, REMOVE_URL, params)

    def parsevideoitem(self, item, queue):
        title = re.compile('target="fileTarget" >(.+?)</a>', re.DOTALL).findall(item)
        title = html.unescape(title[0])
        title = self.cleanup_title(title)

        gurl = re.compile('<a href="(.+?)" target="fileTarget" >', re.DOTALL).findall(item)
        gurl = html.unescape(gurl[0])

        thumbnail = self.build_thumbnail_url (gurl)

        gurl = getrequest.url_auth(gurl)

        sig = re.compile('name="(.+?)" value=', re.DOTALL).findall(item)
        sig = html.unescape(sig[0])

        val = re.compile('value="(.+?)"', re.DOTALL).findall(item)
        val = html.unescape(val[0])

        videoItem = {
            'title': title,
            'thumbnail': thumbnail,
            'gurl': gurl,
            'sig': sig,
            'val': val,
            'queue': queue
        }

        return videoItem

    def parse(self, addonhandle, data, queue):
        items = re.compile('<tr class="rRow(.+?)</tr>', re.DOTALL).findall(data)
        videoItems = []
        if items:
            for item in items:
                videoItem = self.parsevideoitem(item, queue)
                videoItems.append(videoItem)

        videoItems.sort(key=sortByTitle, reverse=True)
        for videoItem in videoItems:
            self.add_video(addonhandle, videoItem)

    def apply(self, addonhandle, activity):
        if constants.APPLY_LOG:
            xbmc.log('%s.apply %s %s' % (self.name, addonhandle, activity.tostring()), 1)

        if activity.operation == self.listQueue:
            response = self.search(activity)
            self.parse(addonhandle, response, activity.state['queue'])
        elif activity.operation == self.remove:
            self.delete(activity)
            xbmc.executebuiltin('Container.Refresh')
        else:
            self.list_queues_menu(addonhandle)

        xbmcplugin.endOfDirectory(addonhandle)

def sortByTitle(videoAction):
    return videoAction['title']

