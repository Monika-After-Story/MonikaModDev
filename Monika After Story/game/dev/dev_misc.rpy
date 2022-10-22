init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_ev_ctx_start",
            category=["dev"],
            prompt="TEST EVENT CONTEXT",
            pool=True,
            unlocked=True
        )
    )

label dev_ev_ctx_start:
    m 1eua "hi there, I'm going to push another event with context"
    $ _some_string = "this is string"
    $ _some_var = 9873
    m "the context will be '[_some_string]' set in 'str_test' and '[_some_var]' set in 'var_test'"

    $ ctx = MASEventContext()
    $ ctx.str_test = _some_string
    $ ctx.var_test = _some_var
    $ MASEventList.push("dev_ev_ctx_end", skipeval=True, context=ctx)

    m 6wuw "The event has been pushed - see you in a bit!"
    return


label dev_ev_ctx_end:
    m 1eua "ok, time to check context"
    $ new_ctx = MASEventContext.get()

    m "checking string: [new_ctx.str_test]"
    m "checking var: [new_ctx.var_test]"
    m "now checking random var: [new_ctx.random_var] - this should not crash"

    m 6wuw "ok we done now"
    return

init 5 python:
    addEvent(
        Event(
            persistent.farewell_database,
            eventlabel="bye_dev_ev_ctx",
            prompt="DEV BYE, CTX TEST",
            pool=True,
            unlocked=True
        ),
        code="BYE"
    )

label bye_dev_ev_ctx:
    m 1eua "hi there, im going to say goodbye but with a context-based event on the event list"
    $ _some_string = "this str 2"
    $ _some_var = 4212
    m "the context will be '[_some_string]' set in 'str_test' and '[_some_var]' set in 'var_test'"

    $ ctx = MASEventContext()
    $ ctx.str_test = _some_string
    $ ctx.var_test = _some_var
    $ MASEventList.push("dev_ev_ctx_end", context=ctx)

    m 6wuw "The Event has been pushed - now to say goodbye"
    m "The ctx event will be trigger after the greeting"
    m "BYE"
    return "quit"

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_ev_ctx_restart_start",
            category=["dev"],
            prompt="TEST EVENT CONTEXT (restart)",
            pool=True,
            unlocked=True
        )
    )

default persistent._dev_ev_ctx_test = False

label dev_ev_ctx_restart_start:
    m 1eua "hi there, im going to crash the game but make sure a topic that is currently running restarts with context."
    $ _some_string = "this restart str"
    $ _some_var = 1023
    m "the context will be '[_some_string]' set in 'str_test' and '[_some_var]' set in 'var_test'"

    $ ctx = MASEventContext()
    $ ctx.str_test = _some_string
    $ ctx.var_test = _some_var
    $ MASEventList.push("dev_ev_ctx_restart", skipeval=True, context=ctx)

    m 6wuw "an event that will be restarted with context has been pushed"
    return

label dev_ev_ctx_restart:
    if persistent._dev_ev_ctx_test:
        call dev_ev_ctx_end
        $ persistent._dev_ev_ctx_test = False
    else:
        m 1eua "i am now going to crash. restart the game afterwards"
        $ persistent._dev_ev_ctx_test = True
        $ renpy.save_persistent()
        $ raise Exception("fake crash")
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_ev_ctx_invalid_start",
            category=["dev"],
            prompt="TEST EVENT CONTEXT (invalid ctx data)",
            pool=True,
            unlocked=True
        )
    )

label dev_ev_ctx_invalid_start:
    m 1eua "hi there, im going to attempt to add data that should not be allowed to the context."
    m "the game should {b}NOT{/b} crash"

    $ ctx = MASEventContext()
    $ ctx.this_is_bad = object()
    $ ctx.this_is_worse = mas_hair_def
    $ ctx.oh_my_god = store.mas_ev_data_ver._strict_can_pickle # functions cannot be pickled

    m 2eub "done - no crash should have happend"
    m "now to check that these have no data"

    if ctx.this_is_bad is None and ctx.this_is_worse is None and ctx.oh_my_god is None:
        m 1hua "Yay it worked"
        m "the bad values will also be logged to mas_log"
    else:
        m 6hftsc "{b}NO IT DID NOT WORK{/b}"

    m 6wuw "ok we done now"
    return
