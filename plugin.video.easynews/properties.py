import xbmcaddon

import constants

def get_property(name, withDefault = None):
    usrsettings = xbmcaddon.Addon(id=constants.ADDON_NAME)
    value = usrsettings.getSetting(name)
    if value:
        return value.strip()
    else:
        return withDefault

def set_property(name, value):
    usrsettings = xbmcaddon.Addon(id=constants.ADDON_NAME)
    usrsettings.setSetting(name, value)