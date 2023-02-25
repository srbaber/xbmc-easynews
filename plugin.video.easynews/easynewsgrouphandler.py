import constants
import easynewssearchhandler
import xbmc


#
# handler responsible for performing the size search for easynews
#
class EasynewsGroupHandler(easynewssearchhandler.EasynewsSearchHandler):
    name = 'EasynewsGroupHandler'
    searchGroup = 'SearchGroup'
    group = ''

    def build_params(self, action):
        params = super().build_params(action)
        params['ns'] = self.group
        return params

    def apply(self, addonhandle, activity):
        if constants.APPLY_LOG:
            xbmc.log('%s.apply %s %s' % (self.name, addonhandle, activity.tostring()), 1)
        self.group = activity.state['group']
        super().apply(addonhandle, activity)
