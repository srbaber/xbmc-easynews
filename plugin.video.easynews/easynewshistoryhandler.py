import constants
import easynewssearchhandler
import xbmc


#
# handler responsible for performing the size search for easynews
#
class EasynewsHistoryHandler(easynewssearchhandler.EasynewsSearchHandler):
    name = 'EasynewsHistoryHandler'
    search_operation = 'SearchKeywordAndOrderBySize'
    search_phrase = ''

    def build_params(self, action):
        params = super().build_params(action)
        params['gps'] = self.search_phrase
        return params

    def apply(self, addonhandle, activity):
        if constants.APPLY_LOG:
            xbmc.log('%s.apply %s %s' % (self.name, addonhandle, activity.tostring()), 1)
        self.search_phrase = activity.state['searchPhrase']
        super().apply(addonhandle, activity)
