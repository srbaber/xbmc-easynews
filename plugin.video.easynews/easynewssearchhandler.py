import html
import re

import action
import constants
import getrequest
import properties
import xbmc
import xbmcgui
import xbmcplugin
from downloadhandler import DownloadHandler
from easynewscleanuphandler import add_watched
from filehandler import extract_filename

SORT_BY_DATE_SELECTION = '0'
SORT_BY_SIZE_SELECTION = '1'
SORT_BY_NAME_SELECTION = '2'
SORT_BY_SUBJECT_SELECTION = '3'

SORT_BY_SIZE = 'dsize'
SORT_BY_NAME = 'nrfile'
SORT_BY_DATE = 'dtime'
SORT_BY_SUBJECT = 'nsubject'
ASCENDING = '+'
DESCENDING = '-'
MAIN_URL = 'https://members.easynews.com/1.0/global5/search.html'

DEFAULT_PER_PAGE = 100


#
# handler responsible for performing the basic search for easynews
#
class EasynewsSearchHandler:
    name = 'EasynewsSearchHandler'
    search_and_order_operation = 'SearchAndOrder'
    search_recent_operation = 'SearchRecent'
    search_abort_operation = 'AbortSearchPlease'
    search_group_operation = 'SearchGroup'
    playbackOperation = 'Video'
    nextPage = 'Next Page'

    video_extensions = ('AVI|MPEG|MPG|WMV|ASF|FLV|MKV|MKA|QT4|MP4|M4A|AAC|NUT|OGG|' +
                        'OGM|RAM|RM|RV|RA|RMVB|3GP|VIV|PVA|NUV|NSV|NSA|FLI|FLC|DVR|WTV')
    image_extensions = 'bmp|gif|jp[eg]|png|tga'

    num_significant_chars = 10

    def __init__(self):
        pass

    def build_url(self, activity):
        return MAIN_URL

    def build_params(self, activity):
        params = {}

        # get the configurations
        extensions = properties.get_property('extensions', self.video_extensions)
        groups = properties.get_property('groups', '')
        per_page = properties.get_property('perpage', DEFAULT_PER_PAGE)
        filter_video = properties.get_property('videos', 'true') == 'true'
        filter_image = properties.get_property('images', 'false') == 'true'
        min_size = properties.get_property('minsize', '')
        sort = properties.get_property('sort', SORT_BY_DATE_SELECTION)
        descending = properties.get_property('descending', 'true') == 'true'

        # apply the search phrase
        params['gps'] = activity.state.get('search_phrase', '')

        # set the group if we are doing a group search or if group regex is configured
        params['ns'] = activity.state.get('group', groups)

        params['fex'] = extensions

        params['pby'] = per_page
        params['pno'] = get_page_number(activity)

        # apply the sorts
        if sort == SORT_BY_DATE_SELECTION:
            params['s1'] = SORT_BY_DATE
            params['s2'] = SORT_BY_SUBJECT
            params['s3'] = SORT_BY_SIZE
        elif sort == SORT_BY_SIZE_SELECTION:
            params['s1'] = SORT_BY_SIZE
            params['s2'] = SORT_BY_SUBJECT
            params['s3'] = SORT_BY_DATE
        elif sort == SORT_BY_NAME_SELECTION:
            params['s1'] = SORT_BY_NAME
            params['s2'] = SORT_BY_DATE
            params['s3'] = SORT_BY_SIZE
        elif sort == SORT_BY_SUBJECT_SELECTION:
            params['s1'] = SORT_BY_SUBJECT
            params['s2'] = SORT_BY_DATE
            params['s3'] = SORT_BY_SIZE

        if descending:
            params['s1d'] = DESCENDING
        else:
            params['s1d'] = ASCENDING

        params['s2d'] = ASCENDING
        params['s3d'] = ASCENDING

        # response should be in RSS feed format for easy parsing
        params['sS'] = '5'

        # allow easynews to filter on video or image
        params['fty[]'] = []
        if filter_video:
            params['fty[]'].append("VIDEO")

        if filter_image:
            params['fty[]'].append("IMAGE")

        # allow easynews to filter on file size
        if min_size != '':
            params['b1'] = min_size + 'mb'
            params['b1t'] = ''
            params['b2'] = ''
            params['b2t'] = ''

        # apply the filter for 1 week for recent search
        if activity.operation == self.search_recent_operation:
            params['d1t'] = '1'
            params['d2t'] = '12'  # less than 1 week old

        params['submit'] = 'Search'
        params['fly'] = '2'

        # xbmc.log("%s.build_params : %s" % (self.name, params), 1)
        return params

    def search(self, activity):
        url = self.build_url(activity)
        params = self.build_params(activity)

        if 'gps' in params and params['gps'] == self.search_abort_operation:
            # handle the cancel buttons on the data entry dialogs
            return None
        elif 'search' in params and params['search'] == self.search_abort_operation:
            # handle the cancel buttons on the data entry dialogs
            return None
        else:
            # otherwise performs the search
            return getrequest.get(url, params)

    def build_thumbnail_url(self, url):
        sixth_slash = find_nth(url, "/", 6)
        if sixth_slash == -1:
            return None

        seventh_slash = find_nth(url, "/", 7)
        if seventh_slash == -1:
            return None

        html_params = url.find("?", seventh_slash)
        if html_params == -1:
            html_params = len(url)

        extension_dot = url.rfind('.', 0, seventh_slash)
        if extension_dot == -1 or extension_dot < sixth_slash:
            extension_dot = seventh_slash

        extension = url[extension_dot + 1: extension_dot + 4]
        is_image = len(re.compile(self.image_extensions, re.DOTALL).findall(extension)) > 0

        thumb_dot = url.rfind('.', 0, html_params)
        if thumb_dot == -1 or thumb_dot < seventh_slash:
            thumb_dot = html_params

        thumb_url = 'https://th.easynews.com/thumbnails-'
        thumb_url += url[sixth_slash + 1: sixth_slash + 4]

        if is_image:
            thumb_url += '/sm-'
        else:
            thumb_url += '/th-'

        thumb_url += url[sixth_slash + 1: extension_dot]
        thumb_url += '.jpg/th-'
        thumb_url += url[seventh_slash + 1: thumb_dot]
        thumb_url += '.jpg'

        # xbmc.log("%s.build_thumbnail_url : %s -> %s" % (self.name, url, thumb_url), 1)
        return thumb_url

    def add_next_page(self, addon_handle, activity):
        activity.state['page_number'] = paginate(activity)
        page_action = action.of(activity.handler, activity.operation, self.nextPage,
                                state=activity.state)
        xbmcplugin.addDirectoryItem(addon_handle, page_action.url(), page_action.directory_item(), isFolder=True)

    def add_context_menu(self, activity):
        download = action.of(DownloadHandler.name, DownloadHandler.download_operation, DownloadHandler.download_file,
                             activity.thumbnail, activity.state)
        cm = [(DownloadHandler.download_file, 'RunPlugin(%s)' % download.url())]

        item = activity.playable_item()
        item.addContextMenuItems(cm)
        return item

    def add_video(self, addon_handle, url, title, thumbnail):
        video_action = action.of(self.name, self.playbackOperation, title, thumbnail, {'url': url})
        list_item = self.add_context_menu(video_action)
        xbmcplugin.addDirectoryItem(addon_handle, video_action.url(), list_item, isFolder=False)

    def parse(self, addon_handle, response):
        session_id = response.headers.get(getrequest.easynews_session_id, None)
        data = re.sub('\n', '', response.text)
        items = re.compile('<item>(.+?)</item>', re.DOTALL).findall(data)
        if items:
            for item in items:
                gurl = re.compile('<link>(.+?)</link>', re.DOTALL).findall(item)
                gurl = html.unescape(gurl[0])

                title = re.compile('<title>(.+?)</title>', re.DOTALL).findall(item)
                title = html.unescape(title[0])
                title = cleanup_title(title, gurl)

                thumbnail = self.build_thumbnail_url(gurl)

                url = getrequest.url_auth(gurl, session_id)

                self.add_video(addon_handle, url, title, thumbnail)

    def apply(self, addon_handle, activity):
        if constants.APPLY_LOG:
            xbmc.log('%s.apply %s %s' % (self.name, addon_handle, activity.tostring()), 1)

        if check_for_invalid_user_id():
            go_to_main_menu(addon_handle)
            return

        if activity.operation == self.playbackOperation:
            add_watched(activity)
            xbmcplugin.setResolvedUrl(addon_handle, succeeded=True, listitem=activity.playable_item())
        else:
            response = self.search(activity)
            if response.text is None:
                go_to_main_menu(addon_handle)
            else:
                self.parse(addon_handle, response)

                self.add_next_page(addon_handle, activity)

                xbmcplugin.endOfDirectory(addon_handle)


def go_to_main_menu(addon_handle):
    main_menu_action = action.of('MainMenuHandler')
    xbmcplugin.setResolvedUrl(addon_handle, succeeded=False, listitem=main_menu_action.directory_item())


def find_nth(data, val, occurrence):
    start = data.find(val)
    while start >= 0 and occurrence > 1:
        start = data.find(val, start + len(val))
        occurrence -= 1
    return start


def split_index(title, open_char, close_char):
    inside_paren_count = 0
    start_idx = len(title) - 1
    while start_idx >= 0:
        if title[start_idx] == close_char:
            inside_paren_count += 1
        elif title[start_idx] == open_char:
            inside_paren_count -= 1
            if inside_paren_count == 0:
                break
        start_idx -= 1

    return start_idx


def normalize(title):
    return re.sub('\W', '', title).lower()


def cleanup_title(title, gurl=''):
    # xbmc.log("Clean Title < : %s" % title, 1)

    title = re.sub(' AutoUnRAR', '', title)
    title = re.sub('\.part[0-9]*\.rar', '', title)
    title = re.sub('y[eE]nc \([0-9]*/[0-9]*\) ', '', title)
    title = re.sub('\[[0-9]*/[0-9]*] ', '', title)
    org_title = title

    filesize = re.search('[0-9.]+ .B$', title)
    if filesize is not None:
        filesize = filesize[0]
        title = title[0:len(title) - len(filesize) - 1]
    else:
        filesize = ''

    split_pos = split_index(title, '(', ')')
    if split_pos == -1:
        description = title
        filename = extract_filename(gurl)
    else:
        description = title[0:split_pos - 1]
        description = re.sub('\w{15,}', '', description)
        filename = title[split_pos:len(title)]
        filename = re.sub('[()]', '', filename)

    if description.find('"') == -1:
        quoted_text = ''
    else:
        quoted_text = re.sub('^(.*?)"', '', description)
        quoted_text = re.sub('".*$', '', quoted_text)

    normalized_filename = re.sub('\.[^.]+$', '', filename)
    normalized_filename = normalize(normalized_filename)
    normalized_description = normalize(description)

    title = filename

    if normalized_description.find(normalized_filename) == -1:
        if len(quoted_text) > 10:
            title += ' "' + quoted_text + '"'
        elif len(description) > 20:
            title += ' (' + description + ')'

    if len(filesize) > 0:
        title += ' ' + filesize

    if len(title) < 20:
        title = org_title

    # xbmc.log("    filename    : %s" % filename, 1)
    # xbmc.log("    quoted text : %s" % quoted_text, 1)
    # xbmc.log("    description : %s" % description, 1)
    # xbmc.log("    normal desc : %s" % normalized_description, 1)
    # xbmc.log("    normal file : %s" % normalized_filename, 1)
    # xbmc.log("Clean Title > : %s\n" % title, 1)
    return title


def get_page_number(activity):
    page_number = int(activity.state.get('page_number', '1'))
    return page_number


def paginate(activity):
    return get_page_number(activity) + 1


def check_for_invalid_user_id():
    user_name = properties.get_property('username')
    passwd = properties.get_property('password')
    if user_name is None or user_name == '' or passwd is None or passwd == '':
        xbmcgui.Dialog().ok('Easynews Configuration',
                            'Please configure your username and password in the settings')
        return True
    else:
        return False
