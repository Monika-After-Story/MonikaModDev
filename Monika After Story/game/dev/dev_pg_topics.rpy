# This file sets up special topics for testing the mas poem minigame
# configuration

##### TESTING ========================########################################
init 5 python:
    for key in ["zzpgone"]:
        monika_topics.setdefault(key,[])
        monika_topics[key].append("zz_mas_poemgame_actone")

## This label directly calls actone style poem minigame
label zz_mas_poemgame_actone:
    $ HKBHideButtons()
    $ store.songs.enabled = False
    call mas_poem_minigame_actone(show_monika=True,trans_fast=True) from _call_mpg_one
    $ testvalues = _return
    $ HKBShowButtons()
    $ play_song(store.songs.current_track)
    $ store.songs.enabled = True
    $ scene_change = True
    return


init 5 python:
    for key in ["zzpgtwo"]:
        monika_topics.setdefault(key,[])
        monika_topics[key].append("zz_mas_poemgame_acttwo")

## This label directly calls act two style poem minigame
label zz_mas_poemgame_acttwo:
    $ HKBHideButtons()
    $ store.songs.enabled = False
    call mas_poem_minigame_acttwo(show_monika=True,trans_fast=True) from _call_mpg_two
    $ testvalues = _return
    $ HKBShowButtons()
    $ play_song(store.songs.current_track)
    $ store.songs.enabled = True
    $ scene_change = True
    return

init 5 python:
    for key in ["zzpgthr"]:
        monika_topics.setdefault(key,[])
        monika_topics[key].append("zz_mas_poemgame_actthr")

## This label directly calls act three style poem minigame
label zz_mas_poemgame_actthr:
    $ HKBHideButtons()
    $ store.songs.enabled = False
    call mas_poem_minigame_actthree(trans_fast=True) from _call_mpg_three
    $ testvalues = _return
    $ HKBShowButtons()
    $ play_song(store.songs.current_track)
    $ store.songs.enabled = True
    $ scene_change = True
    return

init 5 python:
    for key in ["zzpgthrm"]:
        monika_topics.setdefault(key,[])
        monika_topics[key].append("zz_mas_poemgame_actthrm")

## This label calls actthree but with hopping monika and words gathered
label zz_mas_poemgame_actthrm:
    $ HKBHideButtons()
    $ store.songs.enabled = False
    call mas_poem_minigame_actthree(trans_fast=True,hop_monika=True,gather_words=True) from _call_mpg_threem
    $ testvalues = _return
    $ HKBShowButtons()
    $ play_song(store.songs.current_track)
    $ store.songs.enabled = True
    $ scene_change = True
    return

init 5 python:
    for key in ["zzpgonept"]:
        monika_topics.setdefault(key,[])
        monika_topics[key].append("zz_mas_poemgame_actonept")

## This label calls act one but with words being gathered
label zz_mas_poemgame_actonept:
    $ HKBHideButtons()
    $ store.songs.enabled = False
    call mas_poem_minigame_actone(trans_fast=True,gather_words=True) from _call_mpg_onept
    $ testvalues = _return
    $ HKBShowButtons()
    $ play_song(store.songs.current_track)
    $ store.songs.enabled = True
    $ scene_change = True
    return

init 5 python:
    for key in ["zzpgdg"]:
        monika_topics.setdefault(key,[])
        monika_topics[key].append("zz_mas_poemgame_dg")

## This label does a display mode run while gathering words
## This also shows how to do the call via kwargs
label zz_mas_poemgame_dg:
    $ HKBHideButtons()
    $ store.songs.enabled = False
    $ from store.mas_poemgame_consts import DISPLAY_MODE
    # setup dict of kwargs
    python:
        pg_kwargs = {
            "show_monika": True,
            "show_natsuki": True,
            "show_sayori": True,
            "show_yuri": True,
            "show_yuri_cut": True,
            "total_words": 15,
            "trans_fast": True,
            "gather_words": True
        }

        # now make the call
        # NOTE: call is midly dangerous. be careful when using
        renpy.call("mas_poem_minigame", DISPLAY_MODE, **pg_kwargs)

    $ testvalues = _return
    $ HKBShowButtons()
    $ play_song(store.songs.current_track)
    $ store.songs.enabled = True
    $ scene_change = True
    return

init 5 python:
    for key in ["zzpgbgm"]:
        monika_topics.setdefault(key,[])
        monika_topics[key].append("zz_mas_poemgame_bgm")

# This label runs stock mode background music
# also only returns the winner
label zz_mas_poemgame_bgm:
    $ HKBHideButtons()
    $ store.songs.enabled = False
    $ from store.mas_poemgame_consts import STOCK_MODE
    # setup dict of kwargs
    python:
        pg_kwargs = {
            "show_monika": True,
            "show_natsuki": True,
            "show_sayori": True,
            "show_yuri": True,
            "total_words": 15,
            "trans_fast": True,
            "gather_words": True,
            "music_filename": "BACK",
            "only_winner": True
        }

        # now make the call
        # NOTE: call is midly dangerous. be careful when using
        renpy.call("mas_poem_minigame", STOCK_MODE, **pg_kwargs)

    $ testvalues = _return
    $ HKBShowButtons()
    # $ play_song(store.songs.current_track)
    $ store.songs.enabled = True
    $ scene_change = True
    return
