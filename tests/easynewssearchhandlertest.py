import unittest
from easynewssearchhandler import EasynewsSearchHandler

handler = EasynewsSearchHandler()

class EasynewsSearchHandlerTestCase(unittest.TestCase):

    def test_jpg_image(self):
        url = "https://members.easynews.com/dl/iad/447/418bb2aae1121bed3349bc29a57d2a6301814fa671f16.jpg/00-hans_zimmer_and_james_newton_howard-the_dark_knight-ost-cd-flac-2008-proof.jpg?sid=7dfcd27e1b6b7e880d77a8449309e18d09452114:0&sig=MTY5MTk1NDkyNC08YXV0b3Jhci0yYWI0YzVkNGE0MzM0ZjA3OWU0ZTM0ZjY2OTAzMGIyYkBuZ1Bvc3QtOTE0NTdlMTA+"
        desired = "https://th.easynews.com/thumbnails-418/sm-418bb2aae1121bed3349bc29a57d2a6301814fa67.jpg/th-00-hans_zimmer_and_james_newton_howard-the_dark_knight-ost-cd-flac-2008-proof.jpg"
        actual = handler.build_thumbnail_url(url)
        self.assertEqual(desired, actual)

    def test_no_extension_url(self):
        url = "https://members.easynews.com/dl/iad/447/3a82a335fd40e8ebee0dbdecc63ef04607951827cae1a/UEL_2022_2023_Final_Sevilla_vs_Roma_2160p_FEED_HDTV_MP2_H_265_HBO?sid=df99baf8e98eb8bf60c0f5b6b615d003f6d69a11:6&sig=MTY4Njc5NjA5Mi08YXV0b3Jhci1mNDU5ZTE1N2IzNTE0NTZkOTBkMmFjZDAxN2I3ODYyNUBuZ1Bvc3QtNzhmNzNjNmI+"
        desired = "https://th.easynews.com/thumbnails-3a8/pr-3a82a335fd40e8ebee0dbdecc63ef04607951827c.jpg/th-UEL_2022_2023_Final_Sevilla_vs_Roma_2160p_FEED_HDTV_MP2_H_265_HBO.jpg"
        actual = handler.build_thumbnail_url(url)
        self.assertEqual(desired, actual)

    def test_lots_of_dots_url(self):
        url = "https://members.easynews.com/dl/iad/447/3a82a335fd40e8ebee0dbdecc63ef04607951827cae1a.mkv/UEL.2022.2023.Final.Sevilla.vs.Roma.2160p.FEED.HDTV.MP2.H.265-HBO.mkv?sid=df99baf8e98eb8bf60c0f5b6b615d003f6d69a11:6&sig=MTY4Njc5NjA5Mi08YXV0b3Jhci1mNDU5ZTE1N2IzNTE0NTZkOTBkMmFjZDAxN2I3ODYyNUBuZ1Bvc3QtNzhmNzNjNmI+"
        desired = "https://th.easynews.com/thumbnails-3a8/pr-3a82a335fd40e8ebee0dbdecc63ef04607951827c.jpg/th-UEL.2022.2023.Final.Sevilla.vs.Roma.2160p.FEED.HDTV.MP2.H.265-HBO.jpg"
        actual = handler.build_thumbnail_url(url)
        self.assertEqual(desired, actual)

    def test_auto_download_url(self):
        url = "https://members.easynews.com/dl/auto/443/2790b226e1cedd7b47924e4587050f9809779f17c77f4.avi/Teen%20Titans%20-%203x11%20-%20%2337%20-%20Bunny%20Raven%20or%20How%20To%20Make%20a%20TitanAnimal%20Disappear.avi"
        desired = "https://th.easynews.com/thumbnails-279/pr-2790b226e1cedd7b47924e4587050f9809779f17c.jpg/th-Teen%20Titans%20-%203x11%20-%20%2337%20-%20Bunny%20Raven%20or%20How%20To%20Make%20a%20TitanAnimal%20Disappear.jpg"
        actual = handler.build_thumbnail_url(url)
        self.assertEqual(desired, actual)

    def test_iad_download_url(self):
        url = "https://members.easynews.com/dl/iad/447/d130c8aca87927f1019e0d2b7d83eb8f0e0235a314fcc.mkv/b75bd85864bd5c16408c8064976eb2017023661f5525ac8f7fbb1bd1a7fe0c96.mkv?sid=492c2937286ee9b64e41d734c367a1df45026cba:98&sig=MTY5MTc1MDE4MS08WHVHY0lqVG9PYkF3SmtMeFp3UWpRbE53LTE2OTE3MTU1MTUzMDRAUFJpVkFURT4="
        desired = "https://th.easynews.com/thumbnails-d13/pr-d130c8aca87927f1019e0d2b7d83eb8f0e0235a31.jpg/th-b75bd85864bd5c16408c8064976eb2017023661f5525ac8f7fbb1bd1a7fe0c96.jpg"
        actual = handler.build_thumbnail_url(url)
        self.assertEqual(desired, actual)

    def test_its_all_crap(self):
        desired = "e1f654e1433d40249b09a70460057c38.mkv 97.31 GB"
        actual = handler.cleanup_title("e1f654e1433d40249b09a70460057c38 [251/263] \"e1f654e1433d40249b09a70460057c38.part250.rar\" yEnc (1/103) (e1f654e1433d40249b09a70460057c38.mkv AutoUnRAR) 97.31 GB")
        self.assertEqual(desired, actual)

    def test_nothing_really_matches(self):
        desired = "f7781073491242a7a22303521769f54f.mkv 53.34 GB"
        actual = handler.cleanup_title("Y15YZ20YyxAn3o3 [8/13] \"0ko7fwYW7jBbEp_tXbqTlcygLxb.rar\" yEnc (31/59) (f7781073491242a7a22303521769f54f.mkv AutoUnRAR) 53.34 GB")
        self.assertEqual(desired, actual)

    def test_nothing_really_matches_again(self):
        desired = "f7781073491242a7a22303521769f54f.mkv 53.34 GB"
        actual = handler.cleanup_title("0ko7fwYW7jBbEp_tXbqTlcygLxb[8/13] \"Y15YZ20YyxAn3o3.rar\" yEnc (31/59) (f7781073491242a7a22303521769f54f.mkv AutoUnRAR) 53.34 GB")
        self.assertEqual(desired, actual)

    def test_nothing_really_matches_midlength_quoted_text(self):
        desired = "f7781073491242a7a22303521769f54f.mkv 53.34 GB \"12345678901.rar\""
        actual = handler.cleanup_title("0ko7fwYW7jBbEp_tXbqTlcygLxb[8/13] \"12345678901.rar\" yEnc (31/59) (f7781073491242a7a22303521769f54f.mkv AutoUnRAR) 53.34 GB")
        self.assertEqual(desired, actual)

    def test_nothing_really_matches_midlength_description(self):
        desired = "f7781073491242a7a22303521769f54f.mkv 53.34 GB"
        actual = handler.cleanup_title("12345678901 [8/13] \"0ko7fwYW7jBbEp_tXbqTlcygLxb.rar\" yEnc (31/59) (f7781073491242a7a22303521769f54f.mkv AutoUnRAR) 53.34 GB")
        self.assertEqual(desired, actual)

    def test_simple_short_string_only(self):
        desired = "ac3940846ec3caf1f 182.25 MB"
        actual = handler.cleanup_title("ac3940846ec3caf1f 182.25 MB")
        self.assertEqual(desired, actual)

    def test_simple_long_string_only(self):
        desired = "ac3940846ec3caf1fac3940846ec3caf1fac3940846ec3caf1f 182.25 MB"
        actual = handler.cleanup_title("ac3940846ec3caf1fac3940846ec3caf1fac3940846ec3caf1f 182.25 MB")
        self.assertEqual(desired, actual)

    def test_simple_long_prhase_only(self):
        desired = "There once was a man from Nantucket 182.25 MB"
        actual = handler.cleanup_title("There once was a man from Nantucket 182.25 MB")
        self.assertEqual(desired, actual)

    def test_no_name_provided(self):
        desired = "Mune.Guardian.Of.The.Moon.2014.COMPLETE.BLURAY-BLURRY - \"mune.guardian.of.the.moon.2014.complete.bluray-blurry.sample.m2ts\" 172.35 MB"
        actual = handler.cleanup_title("Mune.Guardian.Of.The.Moon.2014.COMPLETE.BLURAY-BLURRY [096/101] - \"mune.guardian.of.the.moon.2014.complete.bluray-blurry.sample.m2ts\" yEnc (001/471) 172.35 MB")
        self.assertEqual(desired, actual)

    def test_short_crap_description(self):
        desired = "Spiderhead.2022.MULTi.1080p.WEB.x264.mkv 2.45 GB \"F45920GW4KZ.11\""
        actual = handler.cleanup_title("F45920GW4KZ - [11/43] - \"F45920GW4KZ.11\" yEnc (1/80) 57281393 (Spiderhead.2022.MULTi.1080p.WEB.x264.mkv AutoUnRAR) 2.45 GB")
        self.assertEqual(desired, actual)

    def test_no_quoted_text_no_matched_name_crap_description(self):
        desired = "Along.for.the.Ride.with.David.O.Doherty.S01E03.1080p.HEVC.x265-MeGusta.mkv 868.64 MB"
        actual = handler.cleanup_title("416685b3beb6b52267c35be6d3b65029b1d0c2159e5de354979867c46f51 (Along.for.the.Ride.with.David.O.Doherty.S01E03.1080p.HEVC.x265-MeGusta.mkv AutoUnRAR) 868.64 MB")
        self.assertEqual(desired, actual)

    def test_quoted_text_matched_name_funky_rar_name(self):
        desired = "Antichrist - 2009 - german - der sir.mkv 1.42 GB"
        actual = handler.cleanup_title("(????) [18/28] - \"Antichrist - 2009 - german - der sir.part15.rar\" yEnc (001/153) (Antichrist - 2009 - german - der sir.mkv AutoUnRAR) 1.42 GB")
        self.assertEqual(desired, actual)

    def test_quoted_text_no_matched_name(self):
        desired = "ps-unc.bdx2-sample.mkv 10.45 MB \"Uncharted.2022.German.AC3D.5.1.BDRip.x264-PS\""
        actual = handler.cleanup_title("Uncharted.2022.German.AC3D.5.1.BDRip.x264-PS - [00/28] - \"Uncharted.2022.German.AC3D.5.1.BDRip.x264-PS.part18.rar\" yEnc (001/118) (ps-unc.bdx2-sample.mkv AutoUnRAR) 10.45 MB")
        self.assertEqual(desired, actual)

    def test_quoted_text_no_matched_name_crap_description(self):
        desired = "De.Geschiedenis.Van.de.VW.Kampeerwagen.GG.NLSUBBED.HDTV.x264-DDF.mkv 430.08 MB"
        actual = handler.cleanup_title("a9f8858e867110ed1cd2576966b0c1898b71ac9ec96dded3bab90b759945b1f6 - [6/7] - \"a9f8858e867110ed1cd2576966b0c1898b71ac9ec96dded3bab90b759945b1f6.part5.rar\" yEnc (1/83) (De.Geschiedenis.Van.de.VW.Kampeerwagen.GG.NLSUBBED.HDTV.x264-DDF.mkv AutoUnRAR) 430.08 MB")
        self.assertEqual(desired, actual)

    def test_special_characters_in_name(self):
        desired = "Auf Messers Schneide Ã¢ Rivalen am Abgrund - 1998 - german - der sir.mkv 1.95 GB \"Auf Messers Schneide  Rivalen am Abgrund - 1998 - german - der sir\""
        actual = handler.cleanup_title("(1243134923423) [23/33] - \"Auf Messers Schneide  Rivalen am Abgrund - 1998 - german - der sir.part20.rar\" yEnc (001/219) (Auf Messers Schneide Ã¢ Rivalen am Abgrund - 1998 - german - der sir.mkv AutoUnRAR) 1.95 GB")
        self.assertEqual(desired, actual)

    def test_case_mismatch_on_name(self):
        desired = "dark.mutants.out.of.control.2020.german.bdrip.x264-lizardsquad.mkv 6.35 MB"
        actual = handler.cleanup_title("Dark.Mutants.Out.of.Control.2020.German.BDRip.x264-LizardSquad - [00/28] - \"Dark.Mutants.Out.of.Control.2020.German.BDRip.x264-LizardSquad.part18.rar\" yEnc (01/69) (dark.mutants.out.of.control.2020.german.bdrip.x264-lizardsquad.mkv AutoUnRAR) 6.35 MB")
        self.assertEqual(desired, actual)

    def test_mismatch_on_name(self):
        desired = "dark.mutants.out.of.control.2020.german.bdrip.x264-lizardsquad.sample.mkv 6.35 MB \"Dark.Mutants.Out.of.Control.2020.German.BDRip.x264-LizardSquad\""
        actual = handler.cleanup_title("Dark.Mutants.Out.of.Control.2020.German.BDRip.x264-LizardSquad - [00/28] - \"Dark.Mutants.Out.of.Control.2020.German.BDRip.x264-LizardSquad.part18.rar\" yEnc (01/69) (dark.mutants.out.of.control.2020.german.bdrip.x264-lizardsquad.sample.mkv AutoUnRAR) 6.35 MB")
        self.assertEqual(desired, actual)

    def test_empty(self):
        desired = ""
        actual = handler.cleanup_title("")
        self.assertEqual(desired, actual)

    def test_sunny_day(self):
        desired = "Zlatan.2021.BDRip.AC3.ITA.SUB.LFi.avi 1.58 GB"
        actual = handler.cleanup_title("Zlatan.2021.BDRip.AC3.ITA.SUB.LFi.avi - [101/117] - \"Zlatan.2021.BDRip.AC3.ITA.SUB.LFi.avi.part100.rar\" yEnc (1/37) (Zlatan.2021.BDRip.AC3.ITA.SUB.LFi.avi AutoUnRAR) 1.58 GB")
        self.assertEqual(desired, actual)

if __name__ == '__main__':
    unittest.main()
