import os

import xbmcaddon
import xbmcvfs

#
# constants for the plugin to use
#
ADDON_NAME = 'plugin.video.easynews'
PLUGIN_URL = 'plugin://' + ADDON_NAME + '/?'
ADDON_PATH = xbmcaddon.Addon(ADDON_NAME).getAddonInfo('path')
DATA_PATH = xbmcvfs.translatePath('special://profile/addon_data/' + ADDON_NAME)

LOGO_IMAGE = os.path.join(ADDON_PATH, 'resources', 'images', 'provocative_logo.png')

APPLY_LOG = False
REQUEST_LOG = False
