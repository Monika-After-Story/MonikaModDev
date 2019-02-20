#Basic copy cat design of the mood file.
#Figured I shouldn't fix something that isn't broken.
#Shout out to whoever did it right the first time.

default persistent_.mas_food_database = {}

default persistent_.mas_food_current = None

init 1 python in mas_food:
    food_db = dict()

    TYPE_FOOD = 0
    TYPE_DRINK = 1

    FOOD_X = 680
    FOOD_Y = 40
    FOOD_W = 560
    FOOD_H = 640
    FOOD_XALIGN = -0.05
    FOOD_AREA = (FOOD_X, FOOD_Y, FOOD_W, FOOD_H)
    FOOD_RETURN = "Nothing"


    def getFoodType(food_label):

        food = food_db.get(food_label)

        if food:
            return food.category[0]

        return None

label mas_food_start:
    python:

        import store.mas_food as mas_food


        filtered_food= Event.filterEvents(
            mas_food.food_db,
            unlocked=True,
            aff=mas_curr_affection
            )

        food_menu_items = [
        (mas_food.food_db[k].prompt, k, False, False)
        for k in filtered_food
        ]

        food_menu_items.sort()

        final_item = (mas_food.FOOD_RETURN, False, False, False, 20)
    call screen mas_gen_scrollable_menu(food_menu_items, mas_food.FOOD_AREA, mas_food.FOOD_XALIGN, final_item=final_item)
    if _return:
        $ pushEvent(_return)

        $ persistent._mas_food_current = _return
    return _return



init 5 python:
    addEvent(Event(persistent._mas_food_database,'mas_food_coffee',prompt='Coffee',category=[store.mas_food.TYPE_DRINK],unlocked=True,),code='FOO')

label mas_food_coffee:
    m 1eka "That sounds wonderful."
    m "I really miss having coffee."
    m "I would always have a cup before and after school."
    m "Maybe even sometimes during class"
    m "I wish I could figure out a way to get some in here."
    m "Who knows, maybe you could share a cup with me [player]"
    return

init 5 python:
    addEvent(Event(persistent._mas_food_database,'mas_food_water',prompt='Water',category=[store.mas_food.TYPE_DRINK],unlocked=True,),code='FOO')
label mas_food_water:
    m "I'm really happy to hear that [player]!"
    m "Water is probably the healthiest thing that you could drink."
    m "Seeing how we can only live for a few days without it."
    m "Just promise you get plenty of drink each day."
    m "I don't want you getting sick because you didn't drink any."
    m "Even if it's just a glass or two, do it for me."
    return
init 5 python:
    addEvent(Event(persistent._mas_food_database,'mas_food_milk',prompt='Milk',category=[store.mas_food.TYPE_DRINK],unlocked=True,),code='FOO')
label mas_food_milk:
    m "You know, I've never really drank a lot milk before."
    m "It wasn't because I didn't like it either."
    m "I just never really thought about it, unless I put it in coffee, or mixed chocolate in with it."
    m "I guess I could learn to love it if you do [player]."
    m "Be sure to pour an extra glass for me next time."
    return
