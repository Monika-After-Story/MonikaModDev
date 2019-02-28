init 5 python:
    addEvent(Event(persistent.event_database,eventlabel="monika_imeating",
                    category=['you'],prompt="I'm Eating/Drinking",pool=True,unlocked=True))

label monika_imeating:
    if mas_getEV('monika_imeating').shown_count == 0:
        m 1eua "You know, although I don't get hungry, I still miss enjoying good food."
        m 4eub "Like Natsuki's cupcakes."
        m 4eua "For a bunch of lines of code, they were pretty tasty."
        m 3hua "Are you eating anything right now, [player]?"
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
    return
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
    m 1eua "That sounds wonderful!"
    m "I really miss having coffee."
    m 3eub "I would always have a cup before and after school."
    m 3hub "Maybe even sometimes during class."
    m 2hub "Who knows, maybe you and I could share a glass, [player]."
    return

init 5 python:
    addEvent(Event(persistent._mas_food_database,'mas_food_water',prompt='Water',category=[store.mas_food.TYPE_DRINK],unlocked=True,),code='FOO')

label mas_food_water:
    m 1eua "I'm really happy to hear that, [player]!"
    m 1eub "Water is probably the healthiest thing that you could drink."
    m 3eua "Seeing how we can only live for a few days without it."
    m 3eud "Just promise you get plenty to drink each day."
    m 2lud "I don't want you getting sick because you didn't drink any."
    m 2eua "Even if it's just a glass or two, do it for me."
    return

init 5 python:
    addEvent(Event(persistent._mas_food_database,'mas_food_milk',prompt='Milk',category=[store.mas_food.TYPE_DRINK],unlocked=True,),code='FOO')

label mas_food_milk:
    m 1eub "You know, I've never really drank a lot milk before."
    m 3eub "It wasn't because I didn't like it either."
    m 3eua "I just never really thought about it, unless I put it in coffee, or mixed chocolate in with it."
    m 1hub "I guess I could learn to love it if you do, [player]."
    m 1hua "Be sure to pour an extra glass for me next time."
    return

init 5 python:
    addEvent(Event(persistent._mas_food_database,'mas_food_hotchocolate',prompt='Hot Chocolate',category=[store.mas_food.TYPE_DRINK],unlocked=True,),code='FOO')

label mas_food_hotchocolate:
    if mas_isWinter():
        m 1hub "That's so nice, [player]!"
        m 4eub "There's really nothing quite like the comfort of hot chocolate when it's chilly outside, is there?"
        m 1eub "In winter, I always enjoy wrapping up in some warm clothes and unwinding with a mug myself."
        m 1eua "It's a great way to relax."
        m 1kua "Maybe some day when it's cold out, we could sit back and have a mug together."
        m 1duu "That would be a dream come true, my love!"

    else:
        m 1hua "That sounds really good right about now."
        m 1hub "There's nothing better than a nice mug of hot cocoa after a long day."
        m 1duu "I can't wait until we can drink some together."
    return
init 5 python:
    addEvent(Event(persistent._mas_food_database,'mas_food_chocolatemilk',prompt='Chocolate Milk',category=[store.mas_food.TYPE_DRINK],unlocked=True,),code='FOO')

label mas_food_chocolatemilk:
    m 3eub "That's wonderful, [player]."
    m 3eub "Although I never drank regular milk too often, there was something different when you mixed chocolate with it."
    m 1lud "..."
    m 1rusdlb "How much do you have [player]?"
    m 1hua "Mind pouring me a glass?" 
    m 1hub "ehehe~"
    return

init 5 python:
    addEvent(Event(persistent._mas_food_database,'mas_food_pizza',prompt='Pizza',category=[store.mas_food.TYPE_FOOD],unlocked=True,),code='FOO')

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
    addEvent(Event(persistent._mas_food_database,'mas_food_salad',prompt='Salad',category=[store.mas_food.TYPE_FOOD],unlocked=True,),code='FOO')

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
