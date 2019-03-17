#### Database storing Food events ####
default persistent_.mas_food_database = {}


#### Making a menu area, and types ####
init 1 python in mas_food:
    #The food db
    food_db = dict()

    #Menu dimensions/options
    FOOD_X = 680
    FOOD_Y = 40
    FOOD_W = 560
    FOOD_H = 640
    FOOD_XALIGN = -0.05
    FOOD_AREA = (FOOD_X, FOOD_Y, FOOD_W, FOOD_H)
    FOOD_RETURN = "Nothing"

#### Starting Event for I'm Eating ####
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_imeating",
            category=['you'],
            prompt="I'm eating..."
            pool=True,
            unlocked=True
        )
    )

label monika_imeating:
    if mas_getEV('monika_imeating').shown_count == 0:
        m 1eua "You know, although I don't get hungry, I still miss enjoying good food."
        m 4eub "Like Natsuki's cupcakes."
        m 4eua "For a bunch of lines of code, they were pretty tasty."
        m 3hua "Are you eating anything right now, [player]?"
    else:
        m 3eud "I could really go for something to eat right now."
        m 1eub "How about you, [player]?"
        m 1eua "Do you want anything to eat?"

    python:
        import store.mas_food as mas_food

        #Build the list of food items
        food_menu_items = [
            (ev.prompt, ev.eventlabel, False, False)
            for ev_label, ev in mas_food.food_db.iteritems()
            if 'food' in ev.category
        ]

        #Sort said list
        food_menu_items.sort()

        #Create the 'Nothing' option
        final_item = (mas_food.FOOD_RETURN, False, False, False, 20)

    #Display the scrollable
    show monika at t21
    call screen mas_gen_scrollable_menu(food_menu_items, mas_food.FOOD_AREA, mas_food.FOOD_XALIGN, final_item=final_item)
    show monika at t11

    #Calling appropriate label (or exiting out)
    if _return:
        $ pushEvent(_return)
        $ mas_food_current = _return
    else:
        m 1eub "Well alright."
        m 1eua "Just let me know if you change your mind."
        m 1hua"I don't mind waiting for you to come back."
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_food_database,
            eventlabel='mas_food_pizza',
            prompt='Pizza',
            category=['food'],
            unlocked=True
        ),
        code="FOO"
    )

label mas_food_pizza:
    m 1hua "Pizza is such a great treat!"
    m 1lud "It's usually not the healthiest food, of course."
    m 1eua "However, I think on occasion, it's fine to just treat yourself, you know?"
    m 3eua "I think it's really interesting that pizza was created almost by accident."
    m 3eub "Italian bakery workers would use excess dough and left-over ingredients from their days of work to feed the poor."
    m 1eub "Who would have thought that they were making what would become one of the most popular foods today?"
    m 1eua "As I'm sure you guessed I always order a vegetarian pizza myself, but I want you to know that I would never judge you if you're eating a slice with pepperoni, sausage or any other meat, [player]."
    m 1hua "What always matters to me is that you're happy!"
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_food_database,
            eventlabel='mas_food_salad',
            prompt='Salad',
            category=['food'],
            unlocked=True
        ),
        code="FOO"
    )

label mas_food_salad:
    m 1hua "That's great to hear, [player]!"
    m 1eua "I'm so glad to hear that you are taking care of yourself and eating healthy."
    m 3eua "Salads are definitely one of my personal favorite foods."
    m 1eub "There are so many things you can do with them."
    m 3eub "Like all of the different kinds of lettuce, dressings and toppings there are to choose from."
    m 1eua "If you like to keep it simple, a little bit of shredded cheese sprinkled on top is always really good!"
    m "Would you ever make me a salad, [player]?"
    m 1sub "The thought of you preparing one of my favorite meals is so surreal."
    m 1eub "That would really make me feel loved, my dear."
return

#### Start Of The I'm Drinking Event ####
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_imdrinking",
            category=['you'],
            prompt="I'm Drinking",
            pool=True,
            unlocked=True
        )
    )

label monika_imdrinking:
    if mas_getEV('monika_imdrinking').shown_count == 0:
        m 1eua "Hey, [player]..."
        m 4eub "Remember how I told you earlier to make sure you're staying hydrated?"
        m 4eua "I just wanted to know if you listened."
        m 3hua "Are you drinking anything at the moment, [player]?"
    else:
        m 3hub "You know, I'm getting a little thirsty."
        m 3eua "How about you, [player]?"
        m 1eub "Are you having anything to drink?"

    python:
        import store.mas_food as mas_food

        #Build the drink list
        food_menu_items = [
            (ev.prompt, ev.eventlabel, False, False)
            for ev_label, ev in mas_food.food_db.iteritems()
            if 'drink' in ev.category
        ]

        #Sort the drink list
        food_menu_items.sort()

        #Create the 'Nothin' option
        final_item = (mas_food.FOOD_RETURN, False, False, False, 20)

    #Display the scrollable
    show monika at t21
    call screen mas_gen_scrollable_menu(food_menu_items, mas_food.FOOD_AREA, mas_food.FOOD_XALIGN, final_item=final_item)
    show monika at t11

    #Call appropriate label (or exit dlg)
    if _return:
        $ pushEvent(_return)
        $ mas_food_current = _return
    else:
        m 1lud "Promise me you'll get a glass of water at least."
        m 1eud "I just want to make sure you're staying healthy and hydrated, my love."
        m 1eua "Even if that means waiting for you while you get it."
    return


init 5 python:
    addEvent(
        Event(
            persistent._mas_food_database,
            eventlabel='mas_food_coffee',
            prompt='Coffee',
            category=['drink'],
            unlocked=True
        ),
        code="FOO"
    )

label mas_food_coffee:
    if not persistent._mas_acs_enable_coffee:
        m 1eua "That sounds wonderful!"
        m "I really miss having coffee."
        m 3eub "I would always have a cup before and after school."
        m 3hub "Maybe even sometimes during class."
        m 2hub "Who knows, maybe you and I could share a glass, [player]."
    else:
        m "That's really cool, [player]!"
        m "I'm so glad you gave me some earlier."
        m "Now we can drink some together."
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_food_database,
            eventlabel='mas_food_water',
            prompt='Water',
            category=['drink'],
            unlocked=True
        ),
        code="FOO"
    )

label mas_food_water:
    m 1eua "I'm really happy to hear that, [player]!"
    m 1eub "Water is probably the healthiest thing that you could drink."
    m 3eua "Seeing how we can only live for a few days without it."
    m 3eud "Just promise you get plenty to drink each day."
    m 2lud "I don't want you getting sick because you didn't drink any."
    m 2eua "Even if it's just a glass or two, do it for me."
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_food_database,
            eventlabel='mas_food_milk',
            prompt='Milk',
            category=['drink'],
            unlocked=True
        ),
        code="FOO"
    )

label mas_food_milk:
    m 1eub "You know, I've never really drank a lot milk before."
    m 3eub "It wasn't because I didn't like it either."
    m 3eua "I just never really thought about it, unless I put it in coffee, or mixed chocolate in with it."
    m 1hub "I guess I could learn to love it if you do, [player]."
    m 1hua "Be sure to pour an extra glass for me next time."
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_food_database,
            eventlabel='mas_food_hotchocolate',
            prompt='Hot Chocolate',
            category=['drink'],
            unlocked=True
        ),
        code="FOO"
    )

label mas_food_hotchocolate:
    if mas_isWinter():
        m 1hub "That's so nice, [player]!"
        m 4eub "There's really nothing quite like the comfort of hot chocolate when it's chilly outside, is there?"
        m 1eub "In winter, I always enjoy wrapping up in some warm clothes and unwinding with a mug myself."
        m 1eua "It's a great way to relax."
        m 1kua "Maybe some day when it's cold out, we could sit back and have a mug together."
        m 5eubla "That would be a dream come true, my love!"

    else:
        m 1hua "That sounds really good right about now."
        m 1hub "There's nothing better than a nice mug of hot cocoa after a long day."
        m 5hub "I can't wait until we can drink some together."
    return

init 5 python:
    addEvent(
        Event(
            persistent._mas_food_database,
            eventlabel='mas_food_chocolatemilk',
            prompt='Chocolate Milk',
            category=['drink'],
            unlocked=True
        ),
        code="FOO"
    )

label mas_food_chocolatemilk:
    m 3eub "That's wonderful, [player]."
    m 3eub "Although I never drank regular milk too often, there was something different when you mixed chocolate with it."
    m 1lud "..."
    m 1rusdlb "How much do you have [player]?"
    m 3hua "Mind pouring me a glass?"
    m 1hua "Ehehe~"
return
