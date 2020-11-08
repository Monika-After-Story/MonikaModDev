# deco testing


image dev_monika_bg_one = "dev/deco/fakebg_1.png"
image dev_monika_bg_two = "dev/deco/fakebg_2.png"
image dev_monika_deco_one = "dev/deco/fakedeco_1_0.png"
image dev_monika_deco_two = "dev/deco/fakedeco_2_0.png"


init -1 python:
    dev_mas_bg_1 = MASFilterableBackground(
        "dev_mas_bg_1",
        "Fake BG 1",
        MASFilterWeatherMap(
            day=MASWeatherMap({
                store.mas_weather.PRECIP_TYPE_DEF: "dev_monika_bg_one",
            }),
            night=MASWeatherMap({
                store.mas_weather.PRECIP_TYPE_DEF: "dev_monika_bg_one",
            }),
            sunset=MASWeatherMap({
                store.mas_weather.PRECIP_TYPE_DEF: "dev_monika_bg_one",
            }),
        ),
        store.mas_background.default_MBGFM(),
        unlocked=True
    )
    dev_mas_bg_2 = MASFilterableBackground(
        "dev_mas_bg_2",
        "Fake BG 2",
        MASFilterWeatherMap(
            day=MASWeatherMap({
                store.mas_weather.PRECIP_TYPE_DEF: "dev_monika_bg_two",
            }),
            night=MASWeatherMap({
                store.mas_weather.PRECIP_TYPE_DEF: "dev_monika_bg_two",
            }),
            sunset=MASWeatherMap({
                store.mas_weather.PRECIP_TYPE_DEF: "dev_monika_bg_two",
            }),
        ),
        store.mas_background.default_MBGFM(),
        unlocked=True
    )


init -1 python:
    # spaceroom will be default position
    MASImageTagDecoDefinition.register_img(
        "dev_monika_deco_one",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=6)
    )
    MASImageTagDecoDefinition.register_img(
        "dev_monika_deco_two",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(zorder=6)
    )

    # fake bg 1 will have the image moved to top left 
    MASImageTagDecoDefinition.register_img(
        "dev_monika_deco_one",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(at_list=[topleft], zorder=6)
    )
    MASImageTagDecoDefinition.register_img(
        "dev_monika_deco_two",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(at_list=[topleft], zorder=6)
    )

    # fake bg 2 will have image moved to topright
    MASImageTagDecoDefinition.register_img(
        "dev_monika_deco_one",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(at_list=[topright], zorder=6)
    )
    MASImageTagDecoDefinition.register_img(
        "dev_monika_deco_two",
        store.mas_background.MBG_DEF,
        MASAdvancedDecoFrame(at_list=[topright], zorder=6)
    )


init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_deco_tag_test",
            category=["dev"],
            prompt="DECO TAG TEST",
            pool=True,
            unlocked=True
        )
    )

label dev_deco_tag_test:
    # TODO:
    #   1. show image - not Now
    #   2. change bg
    #   3. hide image - not Now
    #   4. change bg
    #   5. show image now
    #   6. change bg
    #   7. hide image now
    #   8. change bg
    return

