## This file is for overriding specific declarations from DDLC
## Use this if you want to change a few variables, but don't want
## to replace entire script files that are otherwise fine.

## Normal overrides
## These overrides happen after any of the normal init blocks in scripts.
## Use these to change variables on screens, effects, and the like.
init 10 python:
    pass

## Early overrides
## These overrides happen before the normal init blocks in scripts.
## Use this in the rare event that you need to overwrite some variable
## before it's called in another init block.
## You likely won't use this.
init -10 python:
    # Python 3 / Ren'Py 8 compatibility fallback for Poem class (Android APK environment)
    if not hasattr(store, "Poem"):
        class Poem(object):
            def __init__(self, author="", title="", text="", yuri_2=False, yuri_3=False):
                self.author = author
                self.title = title
                self.text = text
                self.yuri_2 = yuri_2
                self.yuri_3 = yuri_3

    # Python 3 / Ren'Py 8 compatibility fallback for poemwords.
    # This block defines PoemWord and loads full_wordlist for environments where
    # 'scripts.rpa' is not loaded (such as the Android APK build). This prevents
    # AttributeError crashes in translation files (like Spanish) that expect these definitions.
    class PoemWord:
        def __init__(self, word, sPoint, nPoint, yPoint, glitch=False):
            self.word = word
            self.sPoint = sPoint
            self.nPoint = nPoint
            self.yPoint = yPoint
            self.glitch = glitch

    full_wordlist = []
    try:
        with renpy.open_file('poemwords.txt', encoding='utf-8') as wordfile:
            for line in wordfile:
                line = line.strip()
                if line == '' or line[0] == '#': continue
                x = line.split(',')
                full_wordlist.append(PoemWord(x[0], float(x[1]), float(x[2]), float(x[3])))
    except Exception:
        pass

## Super early overrides
## You'll need a block like this for creator defined screen language
## Don't use this unless you know you need it
python early in mas_overrides:
    import io
    from renpy import config, loadsave, savelocation
    import threading

    # Python 3 / Ren'Py 8 compatibility patch for 'scripts.rpa' (PC environment).
    # Monkey-patches renpy.file so that DDLC's original compiled script-poemgame.rpyc (inside scripts.rpa)
    # reads 'poemwords.txt' as a UTF-8 text stream instead of a bytes stream in Python 3.
    # Note: This is separate from the fallback above, which is used when 'scripts.rpa' is absent (Android APK).
    if not hasattr(renpy, "_orig_renpy_file_mas"):
        renpy._orig_renpy_file_mas = renpy.file

        def _mas_renpy_file_override(fn, *args, **kwargs):
            f = renpy._orig_renpy_file_mas(fn, *args, **kwargs)
            if isinstance(fn, str) and fn.endswith('poemwords.txt'):
                try:
                    content = f.read().decode('utf-8')
                    return io.StringIO(content)
                except Exception:
                    pass
            return f

        renpy.file = _mas_renpy_file_override

    def verify_data_override(*args, **kwargs):
        """
        Verify the data in a save token.

        Originally, this function is used to check against a checksum to verify the persistent should be loaded
        But because we want to allow anyone be able to migrate and transfer their data, we will just return True
        """
        return True

    renpy.savetoken.verify_data = verify_data_override


    def savelocation_init_override():
        """
        Run **SOME** of the stuff savelocation.init runs

        basically we trying to keep saves in the AppData/equivalent folder
        to make backups/restoring easier.

        The only difference here is that this skips over game savedirs and
        'extra' save dirs (so just omissions)

        TODO: Find a way to avoid overriding the entire function just
        to disable 2 save locations, this is more bug prone
        """
        savelocation.quit()
        savelocation.quit_scan_thread = False

        location = savelocation.MultiLocation()

        # 1. User savedir.
        location.add(savelocation.FileLocation(config.savedir))

        # 2. Game-local savedir.
        # if (not renpy.mobile) and (not renpy.macapp):
        #     path = os.path.join(renpy.config.gamedir, "saves")
        #     location_add(path)

        # 3. Extra savedirs.
        for i in config.extra_savedirs:
            location.add(savelocation.FileLocation(i))

        # Scan the location once.
        location.scan()

        loadsave.location = location

        # if not renpy.emscripten:
        savelocation.scan_thread = threading.Thread(target=savelocation.run_scan_thread)
        savelocation.scan_thread.start()

    savelocation.init = savelocation_init_override

init -999 python:
    # With our override we should save only to one save location
    # If there's more, we better just crash than let some data mismatch
    if len(renpy.loadsave.location.locations) > 1:
        raise RuntimeError("multiple savelocations detected, exiting")

init 21 python:
    # Patch getSeenPoemsMenu to exclude stock DDLC poems (category "ddlc")
    # since they are already hardcoded in the showpoem menu, preventing duplication.
    def _get_seen_poems_menu_patch():
        return sorted([
            (poem.prompt, poem, False, False)
            for poem in store.mas_poems.poem_map.values()
            if poem.is_seen() and poem.category != "ddlc"
        ], key=store.mas_poems.poem_menu_sort_key)
        
    store.mas_poems.getSeenPoemsMenu = _get_seen_poems_menu_patch

    # Dynamically translate Monika's stock DDLC poems from the translation database
    # at startup. This prevents the need to copy-paste the poem texts or redefine
    # screens/labels, keeping the overrides file very clean.
    for name in ["poem_m1", "poem_m2", "poem_m21", "poem_m22", "poem_m3", "poem_m4"]:
        p = getattr(store, name, None)
        if p:
            p.title = _(p.title)
            p.text = _(p.text)

