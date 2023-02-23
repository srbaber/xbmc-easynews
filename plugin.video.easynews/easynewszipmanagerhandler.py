import xbmc, xbmcplugin

import action, constants, getrequest, re, html
import easynewssearchhandler

MAIN_URL = 'https://members.easynews.com/2.0/tools/zip-manager/index.html'

#
# handler responsible for build the zip manager menu
#
class EasynewsZipManagerHandler(easynewssearchhandler.EasynewsSearchHandler):
    name = 'EasynewsZipManagerHandler'

    listQueue = 'ListQueue'
    listQueues = 'ListQueues'

    def __init__(self):
        pass

    def build_url(self):
        return MAIN_URL

    def build_params(self, action):
        params = {}

        params['editzip'] = action.state['queue']
        params['listOnly'] = '1'

        return params

    def add_zip_queue(self, addonhandle, title, queuename):
        queueAction = action.of(EasynewsZipManagerHandler.name, EasynewsZipManagerHandler.listQueue, title, state={'queue':queuename})
        xbmcplugin.addDirectoryItem(addonhandle, queueAction.url(), queueAction.videoitem(), isFolder=True)

    def list_queues_menu(self, addonhandle):
        self.add_zip_queue(addonhandle, 'Unqueued Files', 'Z')
        for queuenumber in range (1,11):
            title = 'Queue %02d' % queuenumber
            queuename = 'Q%02d' % queuenumber
            self.add_zip_queue(addonhandle, title, queuename)

    def search(self, action):
        return getrequest.get(self, self.build_url(), self.build_params(action))

    def parse(self, addonhandle, data):
        items = re.compile('<td class="fileName" >(.+?)</td>', re.DOTALL).findall(data)
        videoActions = []
        if items:
            for item in items:
                title = re.compile('target="fileTarget" >(.+?)</a>', re.DOTALL).findall(item)
                title = html.unescape(title[0])
                title = self.cleanup_title(title)

                gurl = re.compile('<a href="(.+?) target="fileTarget" >', re.DOTALL).findall(item)
                gurl = html.unescape(gurl[0])

                thumbnail = self.build_thumbnail_url (gurl)

                gurl = getrequest.url_auth(gurl)

                videoActions.append(action.of(self.name, self.playbackOperation, title, thumbnail, gurl))

        videoActions.sort(key=sortByTitle)
        for videoAction in videoActions:
            self.add_video(addonhandle, videoAction.state, videoAction.title, videoAction.thumbnail)

    def apply(self, addonhandle, activity):
        if constants.APPLY_LOG:
            xbmc.log('%s.apply %s %s' % (self.name, addonhandle, activity.tostring()), 1)

        if activity.operation == self.listQueue:
            response = self.search(activity)
            self.parse(addonhandle, response)
        else:
            self.list_queues_menu(addonhandle)

        xbmcplugin.endOfDirectory(addonhandle)

def sortByTitle(videoAction):
    return videoAction.title

