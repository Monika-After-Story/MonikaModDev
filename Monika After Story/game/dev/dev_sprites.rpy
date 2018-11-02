# sprite testing code

init 100 python:
    def mas_test_sitting():
        dd = {
            "clothing": "def",
            "hair": "def",
            "eyebrows": "mid",
            "eyes": "normal",
            "nose": "def",
            "mouth": "smile"
        }

        return [
            store.mas_sprites._ms_sitting(
                isnight=False,
                arms="crossed",
                **dd
            ),
            store.mas_sprites._ms_sitting(
                isnight=True,
                arms="crossed",
                **dd
            ),
            store.mas_sprites._ms_sitting(
                isnight=False,
                lean="def",
                **dd
            ),
            store.mas_sprites._ms_sitting(
                isnight=True,
                lean="def",
                **dd
            ),
            store.mas_sprites._ms_sitting(
                isnight=False,
                arms="crossed",
                eyebags="def",
                sweat="def",
                blush="def",
                tears="def",
                emote="def",
                **dd
            ),
            store.mas_sprites._ms_sitting(
                isnight=True,
                arms="crossed",
                eyebags="def",
                sweat="def",
                blush="def",
                tears="def",
                emote="def",
                **dd
            ),
            store.mas_sprites._ms_sitting(
                isnight=True,
                lean="def",
                eyebags="def",
                sweat="def",
                blush="def",
                tears="def",
                emote="def",
                **dd
            )
        ]

    def mas_supertest():
        abc = open("test.log", "w")
        tests = mas_test_sitting()

        for line in tests:
            abc.write(line + "\n")

        abc.close()
