import easynewssearchhandler
import historyhandler
import properties
import xbmc


#
# handler responsible for performing the keyword search for easynews
#
class EasynewsKeywordHandler(easynewssearchhandler.EasynewsSearchHandler):
    name = 'EasynewsKeywordHandler'
    search_operation = 'SearchKeywordAndOrderBySize'
    search_videos = properties.get_localized_string(30310, 'Search Easynews.com Videos')

    def build_params(self, action):
        params = super().build_params(action)

        searchPhrase = historyhandler.last_search()
        if not 'pagenumber' in action.state or action.state['pagenumber'] == '1':
            kb = xbmc.Keyboard(searchPhrase, self.search_videos, False)
            kb.doModal()
            if kb.isConfirmed():
                # get text from keyboard
                searchPhrase = kb.getText()
                historyhandler.add_search(searchPhrase)

        params['gps'] = searchPhrase

        return params
