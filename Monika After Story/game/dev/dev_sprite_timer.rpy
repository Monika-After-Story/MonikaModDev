# timing sprite string generation
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_sprite_string_timer",
            category=["dev"],
            prompt="TIME SPRITE GEN",
            pool=True,
            unlocked=True
        )
    )

label dev_sprite_string_timer:
    m "how many iterations?"

    python:
        iterations = renpy.input("how many iterations?", allow="0123456789")

        try:
            iterations = int(iterations)
        except:
            iterations = 100000

        def test_fun():
            store.mas_sprites._ms_sitting(
                monika_chr.clothes.name,
                "def",
                "up",
                "normal",
                "def",
                "smile",
                not morning_flag,
                [],
                [],
                monika_chr.acs.get(MASMonika.PST_ACS, []),
                None,
                "steepling",
                None,
                None,
                None,
                None,
                None
            )

    m "okay we do [iterations] times.{fast}"

    python:
        import time
        t0 = time.clock()
        for i in range(iterations):
            test_fun()
        t1 = time.clock()

        total_time = t1-t0

    m "that took [total_time] seconds!"
    return



