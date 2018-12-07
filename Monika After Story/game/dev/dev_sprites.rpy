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
            unlocked=True
        )
    )

label dev_acs_pose_test:
    m 1hua "Hello there!"
    m 1eua "I'm going to test the wonderful accessory system."
    m "First, I'll clear all current accessories."
    $ monika_chr.remove_all_acs()
    m 6sub "I'm going to put on the ring now~"
    $ monika_chr.wear_acs_pst(mas_acs_promisering)
    m 1eua "You should see it now!"
    m 2eua "And it's gone."
    m 3eua "Here it is!"
    m 4eua "Still here~"
    m 5eua "And it's gone."
    m 6sub "Still gone..."
    m "And let's take it all off now~"
    $ monika_chr.remove_all_acs()
    m "Please remember to try it at different times!"
    m 1hua "We wouldn't want anything missing now, would we?"
    return
