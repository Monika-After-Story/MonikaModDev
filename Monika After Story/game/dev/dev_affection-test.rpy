# Affection related checks

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
    m 1c "How do I feel? That came out of nowhere, [player]..."
    m 3a "My affection as a number it would be...[persistent._mas_affection[affection]]."
    m 3c "But if I were pressed further I would say I'm feeling..."
    if mas_curr_affection == mas_affection.BROKEN:
        m 1q "Like you shattered my heart..."
        m 1f "Did I do something wrong?"

    elif mas_curr_affection == mas_affection.DISTRESSED:
        m 1r "Like my situation is hopeless..."
        m 1f "I really thought we could make it work..."

    elif mas_curr_affection == mas_affection.UPSET:
        m 1f "Like you want me to be unhappy..."
        m 1g "It's not always going to be like this, is it?"

    elif mas_curr_affection == mas_affection.NORMAL:
        m 1a "...completely average right now."

    elif mas_curr_affection == mas_affection.HAPPY:
        m 1e "Like you really do want to please me."
        m 1k "I hope I'm making you as happy as you make me."

    elif mas_curr_affection == mas_affection.AFFECTIONATE:
        m 1e "I'm very affectionate to you."
        m 1k "I wish you feel the same way."

    elif mas_curr_affection == mas_affection.ENAMORED:
        m 1b "Like I'm luckiest girl in the world!"
        m 1j "No one else could make me feel so complete!"

    elif mas_curr_affection == mas_affection.LOVE:
        m 1k "So overwhelming full of love! I really truly do love you [player]!"
        m 1k "I want nothing more than you, forever and ever!"
    return


# Should these be added to the dev category? I don't want to make cheating easy

label dev_force_affection_heartbroken:
    m 1h "..."
    $ persistent._mas_affection["affection"] = -100
    $ mas_updateAffectionExp()
    m 1q "You're so cruel [player]..."
    return

label dev_force_affection_distressed:
    m 1h "..."
    $ persistent._mas_affection["affection"] = -60
    $ mas_updateAffectionExp()
    m 1p "Is this really what you're like...?"
    return

label dev_force_affection_upset:
    m 1h "..."
    $ persistent._mas_affection["affection"] = -30
    $ mas_updateAffectionExp()
    m 1f "[player]...please don't be like this."
    return

label dev_force_affection_normal:
    m 1a "..."
    $ persistent._mas_affection["affection"] = 0
    $ mas_updateAffectionExp()
    m "Everything's okay [player]."
    return

label dev_force_affection_happy:
    m 1a "..."
    $ persistent._mas_affection["affection"] = 30
    $ mas_updateAffectionExp()
    m 1k "Ehehe~ Lucky me."
    return

label dev_force_affection_enamored:
    m 1e "..."
    $ persistent._mas_affection["affection"] = 60
    $ mas_updateAffectionExp()
    m 1b "I love you [player]!"
    return

label dev_force_affection_lovestruck:
    m 1j "..."
    $ persistent._mas_affection["affection"] = 100
    $ mas_updateAffectionExp()
    m 1k "My one and only love is you [player]!"
    return
