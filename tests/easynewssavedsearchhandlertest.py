import unittest

import action
from easynewssavedsearchhandler import EasynewsSavedSearchHandler
from easynewssearchhandler import EasynewsSearchHandler
from filehandler import read_whole_file


class EasynewsSavedSearchHandlerTestMock(EasynewsSavedSearchHandler):
    count = 0

    def add_saved_search(self, addon_handle, search_phrase, search_url):
        self.count += 1


class EasynewsSearchHandlerTestMock(EasynewsSearchHandler):
    count = 0

    def add_video(self, addon_handle, url, title, thumbnail):
        self.count += 1


class EasynewsSavedSearchHandlerTestCase(unittest.TestCase):
    def test_saved_searches(self):
        handler = EasynewsSavedSearchHandlerTestMock()
        response = read_whole_file('saved_search_1.xml')
        handler.parse_saved_searches("EasynewsSavedSearchHandler", response)
        self.assertEqual(13, handler.count)

    def test_saved_searches_many_results(self):
        handler = EasynewsSearchHandlerTestMock()
        response = read_whole_file('saved_search_many_results.xml')
        handler.parse("EasynewsSearchHandler", response)
        self.assertEqual(1000, handler.count)

    def test_saved_search_returns_rss(self):
        handler = EasynewsSavedSearchHandlerTestMock()
        search_phrase = 'tulsa king s02 1080 megusta'
        search_url = 'https://members.easynews.com/1.0/global5/?st=adv&safeO=0&sb=1&gps=tulsa+king+s02+1080+megusta&sbj=&from=&ns=&fil=&fex=&vc=&ac=&s1=nrfile&s1d=%2B&s2=dsize&s2d=%2B&s3=dsize&s3d=%2B&fty%5B%5D=VIDEO&u=1&pby=100&pno=1&sS=3&d1=&d1t=&d2=&d2t=&b1=&b1t=&b2=&b2t=&px1=&px1t=&px2=&px2t=&fps1=&fps1t=&fps2=&fps2t=&bps1=&bps1t=&bps2=&bps2t=&hz1=&hz1t=&hz2=&hz2t=&rn1=&rn1t=&rn2=&rn2t=&go=Search&sb=1'
        search_action = action.of(EasynewsSavedSearchHandler.name, EasynewsSearchHandler.search_and_order_operation,
                                  search_phrase, state={'searchUrl': search_url})
        url = handler.build_url(search_action)
        self.assertTrue(url.index('sS=5') > 0)

    def test_search_returns_rss(self):
        handler = EasynewsSavedSearchHandlerTestMock()
        search_phrase = 'from s02'
        search_url = 'https://members.easynews.com/1.0/global5/search.html?gps=from+s02&sbj=&from=&ns=&fil=&fex=&vc=&ac=&fty%5B%5D=VIDEO&s1=nsubject&s1d=%2B&s2=nrfile&s2d=%2B&s3=dsize&s3d=%2B&pby=100&pno=1&sS=5&svL=&d1=&d1t=&d2=&d2t=&b1=&b1t=&b2=&b2t=&px1=&px1t=&px2=&px2t=&fps1=&fps1t=&fps2=&fps2t=&bps1=&bps1t=&bps2=&bps2t=&hz1=&hz1t=&hz2=&hz2t=&rn1=&rn1t=&rn2=&rn2t=&submit=Search&fly=2'
        search_action = action.of(EasynewsSavedSearchHandler.name, EasynewsSearchHandler.search_and_order_operation,
                                  search_phrase, state={'searchUrl': search_url})
        url = handler.build_url(search_action)
        self.assertTrue(url.index('sS=5') > 0)

    def test_saved_search_results_with_quoted_ampersand_test(self):
        handler = EasynewsSearchHandlerTestMock()
        response = read_whole_file('saved_search_with_quoted_ampersand.xml')
        handler.parse("EasynewsSavedSearchHandler", response)
        self.assertEqual(11, handler.count)

    def test_saved_search_results_from(self):
        handler = EasynewsSearchHandlerTestMock()
        response = read_whole_file('saved_search_from_2024.xml')
        handler.parse("EasynewsSavedSearchHandler", response)
        self.assertEqual(1, handler.count)

    def test_search_results_ramsey(self):
        handler = EasynewsSearchHandlerTestMock()
        response = read_whole_file('saved_search_ramsey_2024.xml')
        handler.parse("EasynewsSavedSearchHandler", response)
        self.assertEqual(17, handler.count)


if __name__ == '__main__':
    unittest.main()
