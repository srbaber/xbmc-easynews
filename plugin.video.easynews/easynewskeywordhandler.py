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

        search_phrase = historyhandler.last_search()
        if 'page_number' not in action.state or action.state['page_number'] == '1':
            kb = xbmc.Keyboard(search_phrase, self.search_videos, False)
            kb.doModal()
            if kb.isConfirmed():
                # get text from keyboard
                search_phrase = kb.getText()
                historyhandler.add_search(search_phrase)
            else:
                search_phrase = self.search_abort_operation

        params['gps'] = search_phrase

        return params
