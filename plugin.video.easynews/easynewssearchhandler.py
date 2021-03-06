import re, html

import constants
import xbmc, xbmcplugin

import action
import getrequest
import properties

SORT_BY_SIZE = 'dsize'
SORT_BY_NAME = 'nrfile'
SORT_BY_DATE = 'dtime'
ASCENDING = '+'
DECENDING = '-'
MAIN_URL = 'https://members.easynews.com/global5/search.html'

DEFAULT_PERPAGE = 100

#
# handler responsible for performing the basic search for easynews
#
class EasynewsSearchHandler():
    name = 'EasynewsSearchHandler'
    searchByDate = 'SearchAndOrderByDate'
    playbackOperation = 'Video'
    nextPage = 'Next Page'

    pagenumber='1'

    num_significant_chars=10

    def __init__(self):
        pass

    def build_url(self):
        return MAIN_URL

    def build_params(self, action):
        params = {}

        extensions = properties.get_property('extensions', '')
        groups = properties.get_property('groups', '')
        perpage = properties.get_property('perpage', DEFAULT_PERPAGE)

        params['ns'] = groups
        params['fex'] = extensions

        params['pby'] = perpage
        params['pno'] = self.pagenumber

        params['s1'] = SORT_BY_DATE
        params['s1d'] = DECENDING
        params['s2'] = SORT_BY_NAME
        params['s2d'] = ASCENDING
        params['s3'] = SORT_BY_SIZE
        params['s3d'] = DECENDING

        params['sS'] = '5'
        params['fty[]'] = 'VIDEO'
        params['spamf'] = '1'
        params['u'] = '1'
        params['st'] = 'adv'
        params['safeO'] = '0'
        params['sb'] = '1'
        return params

    def search(self, action):
        return getrequest.get(self, self.build_url(), self.build_params(action))

    def build_thumbnail_url (self, url):
        if len(url) <= 40:
            return None

        firstdot = url.find('.', 40)
        if firstdot == -1:
            return None
        nextslash = url.find('/', firstdot)
        if nextslash == -1:
            return None
        seconddot = url.find('.', nextslash)
        if seconddot == -1:
            return None

        thumb_url = 'https://th.easynews.com/thumbnails-'
        thumb_url += url[40 : 43]
        thumb_url += '/pr-'
        thumb_url += url[40 : firstdot - 4]
        thumb_url += '.jpg/th-'
        thumb_url += url[nextslash + 1 : seconddot]
        thumb_url += '.jpg'

        return thumb_url

    def split_index(self, title, open_char, close_char):
        inside_paren_count = 0
        start_idx = len(title)-1
        while start_idx >= 0:
            if title[start_idx] == close_char:
                inside_paren_count += 1
            elif title[start_idx] == open_char:
                inside_paren_count -= 1
                if inside_paren_count == 0:
                    break
            start_idx -= 1

        return start_idx

    def normalize(self, title):
        return re.sub('[^\w]', '', title).lower()

    def cleanup_title(self, title):
        #xbmc.log("Clean Title < : %s" % title, 1)

        title = re.sub(' AutoUnRAR', '', title)
        title = re.sub('\.part[0-9]*\.rar', '', title)
        title = re.sub('y[eE]nc \([0-9]*/[0-9]*\) ', '', title)
        title = re.sub('\[[0-9]*/[0-9]*] ', '', title)

        org_title = title

        split_pos = self.split_index(title, '(', ')')
        if split_pos == -1:
            description = title
            filename = ''
        else:
            description = title[0:split_pos-1]
            description = re.sub('\w{15,}', '', description)
            filename = title[split_pos:len(title)]
            filename = re.sub('[()]', '', filename)

        if description.find('"') == -1:
            quoted_text = ''
        else:
            quoted_text = re.sub('^(.*?)"', '', description)
            quoted_text = re.sub('".*$', '', quoted_text)

        normalized_filename = re.sub('\.[^.]*$', '', filename)
        normalized_filename = re.sub('\.[^.]*$', '', normalized_filename)
        normalized_filename = self.normalize(normalized_filename)
        normalized_description = self.normalize(description)

        title = filename
        if len(filename) > 0 and normalized_description.find(normalized_filename) == -1:
            if len(quoted_text) > 10:
                title += ' "' + quoted_text + '"'
            elif len(description) > 20:
                title += ' (' + description + ')'

        if len(title) < 20:
            title = org_title

        # xbmc.log("    filename    : %s" % filename, 1)
        # xbmc.log("    quoted text : %s" % quoted_text, 1)
        # xbmc.log("    description : %s" % description, 1)
        # xbmc.log("    normal desc : %s" % normalized_description, 1)
        # xbmc.log("    normal file : %s" % normalized_filename, 1)
        #xbmc.log("Clean Title > : %s\n" % title, 1)
        return title

    def paginate(self, activity):
        if 'pagenumber' in activity.state:
            self.pagenumber = int(activity.state['pagenumber']) + 1

    def add_next_page(self, addonhandle, activity):
        activity.state['pagenumber'] = int(self.pagenumber) + 1
        pageAction = action.of(activity.handler, activity.operation, self.nextPage, state=activity.state)
        xbmcplugin.addDirectoryItem(addonhandle, pageAction.url(), pageAction.directoryitem(), isFolder=True)

    def add_video(self, addonhandle, url, title, thumbnail):
        videoAction = action.of(self.name, self.playbackOperation, title, thumbnail, {'url': url})
        xbmcplugin.addDirectoryItem(addonhandle, url, videoAction.videoitem(), isFolder=False)

    def parse(self, addonhandle, data):
        # xbmc.log("Parse Data : %s" % data, 1)
        items = re.compile('<item>(.+?)</item>', re.DOTALL).findall(data)
        if items:
            for item in items:
                title = re.compile('<title>(.+?)</title>', re.DOTALL).findall(item)
                title = html.unescape(title[0])
                title = self.cleanup_title(title)

                gurl = re.compile('<link>(.+?)</link>', re.DOTALL).findall(item)
                gurl = html.unescape(gurl[0])

                thumbnail = self.build_thumbnail_url (gurl)

                gurl = getrequest.url_auth(gurl)
                self.add_video(addonhandle, gurl, title, thumbnail)

    def apply(self, addonhandle, activity):
        if constants.APPLY_LOG:
            xbmc.log('%s.apply %s %s' % (self.name, addonhandle, activity.tostring()), 1)

        self.paginate(activity)

        response = self.search(activity)
        self.parse(addonhandle, response)

        self.add_next_page(addonhandle, activity)

        xbmcplugin.endOfDirectory(addonhandle)

