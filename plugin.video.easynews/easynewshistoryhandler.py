
import easynewssearchhandler


#
# handler responsible for performing a previous search for easynews
#
class EasynewsHistoryHandler(easynewssearchhandler.EasynewsSearchHandler):
    name = 'EasynewsHistoryHandler'

    def build_params(self, action):
        params = super().build_params(action)
        params['gps'] = action.state['searchPhrase']
        return params
