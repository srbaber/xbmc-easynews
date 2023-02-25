import urllib

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

    def contextmenu(self, activity):
        remove = action.of(self.name, self.remove, self.remove, activity.thumbnail, activity.state)
        cm = [(self.remove, 'RunPlugin(%s)' % remove.url())]

        item = activity.playableitem()
        item.addContextMenuItems(cm)
        return item

    def add_video(self, addonhandle, title, thumbnail, gurl, state):
        videoAction = action.of(self.name, self.playbackOperation, title, thumbnail, state)
        contextmenu = self.contextmenu(videoAction)
        xbmcplugin.addDirectoryItem(addonhandle, gurl, contextmenu, isFolder=False)

    def parse(self, addonhandle, data, queue):
        items = re.compile('<tr class="rRow(.+?)</tr>', re.DOTALL).findall(data)
        if items:
            for item in items:
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

                state = {
                    'url': gurl,
                    'sig': sig,
                    'val': val,
                    'queue': queue
                }

                self.add_video(addonhandle, title, thumbnail, gurl, state)

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
        formdata = {}
        formdata['editque'] = action.state['queue']
        formdata['sS'] = '0'
        formdata['nameZipQ0'] = ''
        formdata['copyque'] = ''
        formdata['nameZipQ'] = ''
        formdata[action.state['sig']] = action.state['val']
        formdata['DEL'] = 'Remove Checked Files'

        getrequest.post(self, REMOVE_URL, formdata)

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

def sort_by_title(videoAction):
    return videoAction['title']

