import constants
import easynewssearchhandler
import xbmc


#
# handler responsible for performing the group search for easynews
#
class EasynewsGroupHandler(easynewssearchhandler.EasynewsSearchHandler):
    name = 'EasynewsGroupHandler'
    search_group_operation = 'SearchGroup'
    group = ''

    def build_params(self, action):
        params = super().build_params(action)
        params['ns'] = self.group
        return params

    def apply(self, addon_handle, activity):
        if constants.APPLY_LOG:
            xbmc.log('%s.apply %s %s' % (self.name, addon_handle, activity.tostring()), 1)

        self.group = activity.state['group']
        super().apply(addon_handle, activity)
