import easynewscleanuphandler
import easynewssearchhandler
import properties
import xbmc


#
# handler responsible for performing the keyword search for easynews
#
class EasynewsKeywordHandler(easynewssearchhandler.EasynewsSearchHandler):
    name = 'EasynewsKeywordHandler'
    search_operation = 'SearchKeywordAndOrderBySize'
    search_videos = properties.get_localized_string(30310, 'Search Easynews.com Videos')

    def build_params(self, activity):
        # use the last search  phrase as the default value
        search_phrase = easynewscleanuphandler.last_search()

        # only prompt on the first page of the search results
        if activity.state.get('page_number', '1') == '1':
            kb = xbmc.Keyboard(search_phrase, self.search_videos, False)
            kb.doModal()
            if kb.isConfirmed():
                search_phrase = kb.getText()
                easynewscleanuphandler.add_search(search_phrase)
                activity.state['search_phrase'] = search_phrase
            else:
                activity.state['search_phrase'] = self.search_abort_operation

        return super().build_params(activity)
