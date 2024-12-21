import constants
import xbmcaddon

in_memory_properties = {}


def get_localized_string(property_id, default_value=None):
    return in_memory_properties.get(property_id, default_value)


def get_property(name, default_value=None):
    return in_memory_properties.get(name, default_value)


def set_property(name, value):
    in_memory_properties[name] = value
