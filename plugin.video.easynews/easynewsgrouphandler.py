import xbmc

import easynewssearchhandler

#
# handler responsible for performing the size search for easynews
#
class EasynewsGroupHandler(easynewssearchhandler.EasynewsSearchHandler):
    name = 'EasynewsGroupHandler'
    searchGroup = 'SearchGroup'
    group = ''

    def __init__(self):
        pass

    def build_params(self):
        params = super().build_params()
        params['ns'] = self.group
        return params

    def apply(self, addonhandle, activity):
        xbmc.log('%s.apply %s %s' % (self.name, addonhandle, activity.tostring()), 1)
        self.group = activity.state['group']
        super().apply(addonhandle, activity)
