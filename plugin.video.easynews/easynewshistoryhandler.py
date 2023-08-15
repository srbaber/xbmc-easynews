import constants
import easynewssearchhandler
import xbmc


#
# handler responsible for performing the size search for easynews
#
class EasynewsHistoryHandler(easynewssearchhandler.EasynewsSearchHandler):
    name = 'EasynewsHistoryHandler'

    def build_params(self, action):
        params = super().build_params(action)
        params['gps'] = action.state['searchPhrase']
        return params
