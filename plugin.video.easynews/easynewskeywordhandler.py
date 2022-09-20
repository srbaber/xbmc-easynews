import xbmc

import easynewssearchhandler
import historyhandler

#
# handler responsible for performing the keyword search for easynews
#
class EasynewsKeywordHandler(easynewssearchhandler.EasynewsSearchHandler):
    name = 'EasynewsKeywordHandler'
    searchKeyword = 'SearchKeywordAndOrderBySize'

    def __init__(self):
        pass

    def build_params(self, action):
        params = super().build_params(action)

        searchPhrase = historyhandler.last_search()
        if not 'pagenumber' in action.state or action.state['pagenumber'] == '1':
            kb = xbmc.Keyboard(searchPhrase, 'Search Easynews.com Videos', False)
            kb.doModal()
            if kb.isConfirmed():
                # get text from keyboard
                searchPhrase = kb.getText()
                historyhandler.add_search(searchPhrase)

        params['gps'] = searchPhrase

        return params