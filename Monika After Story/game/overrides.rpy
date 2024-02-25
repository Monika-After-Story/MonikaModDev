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
    pass

## Super early overrides
## You'll need a block like this for creator defined screen language
## Don't use this unless you know you need it
python early in mas_overrides:
    import threading

    import renpy
    import renpy.savelocation as savelocation
    import renpy.parser as parser


    def verify_data_override(data, signatures, check_verifying=True):
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
        """
        savelocation.quit()
        savelocation.quit_scan_thread = False

        location = savelocation.MultiLocation()

        location.add(savelocation.FileLocation(renpy.config.savedir))

        location.scan()

        renpy.loadsave.location = location

        if not renpy.emscripten:
            savelocation.scan_thread = threading.Thread(target=savelocation.run_scan_thread)
            savelocation.scan_thread.start()

    savelocation.init = savelocation_init_override


    def parser_report_parse_errors_override():
        """
        This override is actually for something unrelated. 

        We need to prevent scripts.rpa code from being loaded, but there's
        no way to override script loading code since by the time THIS script
        is loaded (and override set), the scripts.rpa contents are already
        queued to be loaded later.

        This specific function is called before the init scripts start running
        so this is the last place we can remove the scripts rpa stuff we dont
        want.
        """
        global report_parse_errors_ran

        if not report_parse_errors_ran:
            for index, initcode in reversed(list(enumerate(renpy.game.script.initcode))):
                init_lvl, obj = initcode

                try:
                    if obj.filename == "script-poemgame.rpyc":
                        renpy.game.script.initcode.pop(index)
                except:
                    pass
            report_parse_errors_ran = True

        # non-override code below

        parser.release_deferred_errors()

        if not parser.parse_errors:
            return False

        full_text = ""

        f, error_fn = renpy.error.open_error_file("errors.txt", "w")
        with f:
            f.write("\ufeff") # BOM

            print("I'm sorry, but errors were detected in your script. Please correct the", file=f)
            print("errors listed below, and try again.", file=f)
            print("", file=f)

            for i in parser.parse_errors:

                full_text += i
                full_text += "\n\n"

                if not isinstance(i, str):
                    i = str(i, "utf-8", "replace")

                print("", file=f)
                print(i, file=f)

                try:
                    print("")
                    print(i)
                except Exception:
                    pass

            print("", file=f)
            print("Ren'Py Version:", renpy.version, file=f)
            print(str(time.ctime()), file=f)

        renpy.display.error.report_parse_errors(full_text, error_fn)

        try:
            if renpy.game.args.command == "run": # type: ignore
                renpy.exports.launch_editor([ error_fn ], 1, transient=True)
        except Exception:
            pass

        return True

    report_parse_errors_ran = False
    parser.report_parse_errors = parser_report_parse_errors_override


