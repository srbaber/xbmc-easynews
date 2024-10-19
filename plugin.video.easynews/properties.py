import constants
import xbmcaddon


def get_localized_string(property_id, default_value=None):
    user_settings = xbmcaddon.Addon(id=constants.ADDON_NAME)
    value = user_settings.getLocalizedString(property_id)
    if value:
        return value.strip()
    else:
        return default_value


def get_property(name, default_value=None):
    user_settings = xbmcaddon.Addon(id=constants.ADDON_NAME)
    value = user_settings.getSetting(name)
    if value:
        return value.strip()
    else:
        return default_value


def set_property(name, value):
    user_settings = xbmcaddon.Addon(id=constants.ADDON_NAME)
    user_settings.setSetting(name, value)
