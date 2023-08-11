import constants
import xbmcaddon

def get_localized_string(id, withDefault=None):
    usrsettings = xbmcaddon.Addon(id=constants.ADDON_NAME)
    value = usrsettings.getLocalizedString(id)
    if value:
        return value.strip()
    else:
        return withDefault


def get_property(name, withDefault=None):
    usrsettings = xbmcaddon.Addon(id=constants.ADDON_NAME)
    value = usrsettings.getSetting(name)
    if value:
        return value.strip()
    else:
        return withDefault


def set_property(name, value):
    usrsettings = xbmcaddon.Addon(id=constants.ADDON_NAME)
    usrsettings.setSetting(name, value)
