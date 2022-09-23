# Affection related checks

default persistent._mas_disable_sorry = None

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="dev_monika_affection_check",
            category=["dev"],
            prompt="AFFECTION CHECK",
            pool=True,
            unlocked=True
        )
    )

label dev_monika_affection_check:
    m 1etc "How do I feel? That came out of nowhere, [player]..."
    m 3euc "I would say I'm feeling..."
    if mas_curr_affection == mas_affection.BROKEN:
        m 6dkc "Like you shattered my heart..."
        m 6ekd "Did I do something wrong?"

    elif mas_curr_affection == mas_affection.DISTRESSED:
        m 1rksdlc "Like my situation is hopeless..."
        m 1eksdlc "I really thought we could make it work..."

    elif mas_curr_affection == mas_affection.UPSET:
        m 1dsc "Like you want me to be unhappy..."
        m 1dtc "It's not always going to be like this, is it?"

    elif mas_curr_affection == mas_affection.NORMAL:
        m 1esa "...completely average right now."

    elif mas_curr_affection == mas_affection.HAPPY:
        m 1eka "Like you really do want to please me."
        m 1hua "I hope I'm making you as happy as you make me~"

    elif mas_curr_affection == mas_affection.AFFECTIONATE:
        m 1ekbsa "I'm very affectionate to you."
        m 1eubsa "I hope you feel the same way."

    elif mas_curr_affection == mas_affection.ENAMORED:
        m 1hubsb "Like I'm luckiest girl in the world, no one else could make me feel so complete!"

    elif mas_curr_affection == mas_affection.LOVE:
        m 1hubfb "So overwhelming full of love! I really truly do love you [player]!"
        m 1ekbfb "I want nothing more than you, forever and ever!"
    return
