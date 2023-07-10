init 1 python in mas_unittests:
    @testclass
    class TestInActiveWindowRegexp(unittest.TestCase):
        def test_simple_youtube_detection(self):
            self.assertTrue(
                store.mas_windowutils.evaluateInWindowHandle(
                    "- YouTube",
                    "CA Celeste Piano Collections: 11 Reach for the Summit (Lena Raine, Trevor Alan Gomes) - YouTube"
                )
            )

        #Jpn characters
        def test_jpn_character_detection(self):
            self.assertTrue(
                store.mas_windowutils.evaluateInWindowHandle(
                    "ドキドキ",
                    "【DDLC】ドキドキ文芸部に入部してみるぺこ！【ホロライブ/兎田ぺこら】 - YouTube - Opera"
                )
            )


        #r34 (titles are taken from images/posts w/o explicit content)
        def test_r34_site_detection(self):
            r34_regexp = r"(?i)(((r34|rule\s?34).*monika)|(post \d+:[\w ]+monika)|([[\w \]\-()]*monika[\w?()\-: ]*(r34|rule34)))"

            with self.subTest("r34_site_detection (r34xxx)"):
                self.assertTrue(
                    store.mas_windowutils.evaluateInWindowHandle(
                        r34_regexp,
                        "Rule 34 - 1girls black legwear black thighhighs blondynkitezgraja blue skirt brown hair cleavage clothing doki doki literature club female female only green eyes long hair medium breasts monika monika (doki doki literature club) piano skirt skirt lift thighhighs | 4046712"
                    )
                )

            with self.subTest("r34_site_detection (r34paheal)"):
                self.assertTrue(
                    store.mas_windowutils.evaluateInWindowHandle(
                        r34_regexp,
                        "Post 4187900: Monika cosplay squchan tagme"
                    )
                )

            with self.subTest("r34_site_detection (rDDLCRule34)"):
                self.assertTrue(
                    store.mas_windowutils.evaluateInWindowHandle(
                        r34_regexp,
                        "[Commission] Office Monika for Hisame-kun (light nsfw) : DDLCRule34"
                    )
                )
