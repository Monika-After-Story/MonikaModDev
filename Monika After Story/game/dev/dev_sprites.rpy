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


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_acs_pose_test",
            category=["dev"],
            prompt="ACCESSORY POSE TEST",
            pool=True,
            random=True,
            unlocked=True
        )
    )

label dev_acs_pose_test:
    m "Hi there!"
    m "I'm going to test the wonderful accessory system."
    m "First, gonna clear current accessories"
    $ monika_chr.remove_all_acs()
    m 6sub "Now going to put on the ring"
    $ monika_chr.wear_acs_pst(mas_acs_promisering)
    m 1eua "OKAY THIS SHOULD BE VISIBLE NOW"
    m 2eua "NOT VISIBLE"
    m 3eua "VISIBLE"
    m 4eua "VISIBLE"
    m 5eua "NOT VISIBLE"
    m 6sub "NOT VISIBLE"
    m "time to remove accessories"
    $ monika_chr.remove_all_acs()
    m "Try this again at night/day so we get everything we need"
    return
