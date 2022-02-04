import xbmc

import easynewssearchhandler
import properties
import historyhandler

#
# handler responsible for performing the keyword search for easynews
#
class EasynewsKeywordHandler(easynewssearchhandler.EasynewsSearchHandler):
    name = 'EasynewsKeywordHandler'
    searchKeyword = 'SearchKeywordAndOrderBySize'

    def __init__(self):
        pass

    def build_params(self):
        params = super().build_params()

        last = historyhandler.last_search()
        kb = xbmc.Keyboard(last, 'Search Easynews.com Videos', False)
        kb.doModal()
        if kb.isConfirmed():
            # get text from keyboard
            searchPhrase = kb.getText()
            params['gps'] = searchPhrase
            historyhandler.add_search(searchPhrase)

        return params