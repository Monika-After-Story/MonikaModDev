label test_show_notif:
    m 1hua "Okay!"
    m 3eua "Give me a second to make a notification...{nw}"
    show monika 2dsc
    pause 1.0

    python:
        import balloontip
        balloontip.balloon_tip("Monika","Hey, [player]?\nI love you~")

    m 1hub "Done!"
    m 1eub "Did it work?"
    return