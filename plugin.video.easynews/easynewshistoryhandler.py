import xbmc

import easynewssearchhandler

#
# handler responsible for performing the size search for easynews
#
class EasynewsHistoryHandler(easynewssearchhandler.EasynewsSearchHandler):
    name = 'EasynewsHistoryHandler'
    searchKeyword = 'SearchKeywordAndOrderBySize'
    searchPhrase = ''

    def __init__(self):
        pass

    def build_params(self):
        params = super().build_params()
        params['gps'] = self.searchPhrase
        return params

    def apply(self, addonhandle, activity):
        xbmc.log('%s.apply %s %s' % (self.name, addonhandle, activity.tostring()), 1)
        self.searchPhrase = activity.state['searchPhrase']
        super().apply(addonhandle, activity)
