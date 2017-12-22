init 501:
    python:
        import datetime

        now = datetime.datetime.now()
        christmas_time = datetime.datetime(2017,12,26)
        is_christmas_time = now < christmas_time

    if is_christmas_time:
        #body poses
        image body_1 = im.Composite((1280,742),(0,0),"mod_assets/monika/torso-xmas.png",(0,0),"mod_assets/monika/arms-steepling-xmas.png")
        image body_1_n = im.Composite((1280,742),(0,0),"mod_assets/monika/torso-n-xmas.png",(0,0),"mod_assets/monika/arms-steepling-n-xmas.png")
        image body_2 = im.Composite((1280,742),(0,0),"mod_assets/monika/torso-xmas.png",(0,0),"mod_assets/monika/arms-crossed-xmas.png")
        image body_2_n = im.Composite((1280,742),(0,0),"mod_assets/monika/torso-n-xmas.png",(0,0),"mod_assets/monika/arms-crossed-n-xmas.png")
        image body_3 = im.Composite((1280,742),(0,0),"mod_assets/monika/torso-xmas.png",(0,0),"mod_assets/monika/arms-restleftpointright-xmas.png")
        image body_3_n = im.Composite((1280,742),(0,0),"mod_assets/monika/torso-n-xmas.png",(0,0),"mod_assets/monika/arms-restleftpointright-n-xmas.png")
        image body_4 = im.Composite((1280,742),(0,0),"mod_assets/monika/torso-xmas.png",(0,0),"mod_assets/monika/arms-pointright-xmas.png")
        image body_4_n = im.Composite((1280,742),(0,0),"mod_assets/monika/torso-n-xmas.png",(0,0),"mod_assets/monika/arms-pointright-n-xmas.png")
        image body_5 = im.Composite((1280,742),(0,0),"mod_assets/monika/body-leaning-xmas.png")
        image body_5_n = im.Composite((1280,742),(0,0),"mod_assets/monika/body-leaning-n-xmas.png")

        image monika_room = "mod_assets/monika_room_xmas.png"
        image monika_day_room = "mod_assets/monika_day_room_xmas.png"

        image room_mask = Movie(channel="window_1", play="mod_assets/window_1_snow.webm",mask=None,image="mod_assets/window_1_fallback.png")
        image room_mask2 = Movie(channel="window_2", play="mod_assets/window_2_snow.webm",mask=None,image="mod_assets/window_2_fallback.png")
        image room_mask3 = Movie(channel="window_3", play="mod_assets/window_3_snow.webm",mask=None,image="mod_assets/window_3_fallback.png")
        image room_mask4 = Movie(channel="window_4", play="mod_assets/window_4_snow.webm",mask=None,image="mod_assets/window_4_fallback.png")


#This file contains all the special events for Christmas
init 6 python:
    import datetime

    now = datetime.datetime.now()
    christmas = datetime.datetime(2017,12,25)
    before_christmas = now < christmas

    if before_christmas and not seen_event('monika_holiday_intro'):
        queueEvent('monika_holiday_intro')

label monika_holiday_intro:
    m 1b "Happy holidays!"
    m 2a "Do you like what I've done with the room?"
    m 2j "I must say that I'm pretty proud of it."
    m 4a "Christmas time has always been one of my favorite occasions of the year."
    m 2a "And I'm so glad that you're here to share it with me~"
    return

init 5 python:
    import datetime

    now = datetime.datetime.now()
    if now.day == 25 and now.month == 12 and not seen_event('monika_christmas'):
        queueEvent('monika_christmas')

label monika_christmas:
    m 1b "[player]! Do you know what day it is?"
    m 3k "Of course you do. It's Christmas!"
    m 1j "Merry Christmas, [player]!"
    m 1b "Ahaha! I can't believe that it's finally here!"
    m 3j "I'm so, so happy that you decided to spend some of it with me."
    m 3d "Remember to go share the holiday cheer with your family and friends, though."
    m 1e "After all, they're very important, too."
    m 1a "And I'm sure that they would love to see you at this special time."
    m 1f "But..."
    m 1q "..."
    m 1e "[player], I love you."
    m 1e "Maybe it's just the snow, or the decorations." 
    m 3n "...or even the mistletoe getting to me."
    m 1l "Don't worry! I didn't hang one up."
    m 1m "...Maybe~"
    m 1n "Ehehe..."
    m 1e "My heart's fluttering like crazy right now, [player]."
    m 1j "I couldn't imagine a better way to spend this special holiday..."
    m 3m "Don't get me wrong, I knew that you would."
    m 3e "Actually having you here with me on Christmas, with just the two of us..."
    m 1k "Ahaha~"
    m 2a "It's every couple's dream in the holidays, [player]."
    m 2e "Snuggling with each other by a fireplace, watching the snow gently fall..."
    m 2j "I'm forever grateful I got this chance with you, [player]."
    m 5a "I love you. Forever and ever~"
    m "Merry Christmas, [player]~"
    return

init 5 python:
    import datetime

    now = datetime.datetime.now()
    if (now.day >= 12 and now.day <=20) and now.month == 12 and now.year == 2017 and not seen_event('monika_hanukkah'):
        queueEvent('monika_hanukkah')
        
label monika_hanukkah:
    m 1q "'{i}One for each night, they shed a sweet light, to remind of days long ago{/i}.'"
    m 1r "'{i}One for each night, they shed a sweet light, to remind of days long ago{/i}.'"
    m 3a "It is said in the Jewish tradition, that one day's worth of olive oil gave the menorah eight days of light."
    m 1b "Eight nights worth of celebration!"
    m 3a "Hanukkah also shifts a bit from year to year. It's date is determined by the Hebrew Lunar Calendar."
    m "It's on the 25th of Kislev, meaning 'trust' or 'hope'."
    m 1j "A very appropriate meaning for such an occasion, don't you think?"
    m 1a "Anyway, have you ever had fried sufganiyot before?" 
    m "It's a special kind of doughnut made during this holiday."
    m 3b "It's filled in with something really sweet, deep fried, and rolled onto some sugar."
    m "It's really good pastry! I especially love the ones filled with strawberry filling~"
    m 3n "Definitely better than Natsuki's cupcakes."
    m 1j "This time of year sure has a lot wonderful holidays and traditions."
    m 1d "I don't know if you celebrate Hanukkah, but can we watch a menorah lighting ceremony together, anyway?"
    m 1k "We can sing and dance the night away~"
    return

init 5 python:
    import datetime

    now = datetime.datetime.now()
    if (now.day >= 26 and now.day <=30) and now.month == 12 and now.year == 2017 and not seen_event('monika_kwanzaa'):
        queueEvent('monika_kwanzaa')

label monika_kwanzaa:
    m 1b "[player], have you ever heard of Kwanzaa?"
    m 1a "It's a week-long festival celebrating African American history that starts the day after Christmas."
    m 2a "The word 'Kwanzaa' comes from the Swahili phrase 'matunda ya kwanza', which means 'first fruits'."
    m "Even if Christmas is the main event for many, other holidays are always interesting to learn about."
    m 4a "Apparently, people celebrate the tradition by decorating their homes with bright adornments."
    m "There's also music to enjoy, and a candleholder called the 'kinara' to light a new fire with each passing day."
    m 1j "Doesn't it remind you of some other holidays? The concepts certainly seem familiar."
    m 1a "In the end, having a day to celebrate is the important part. Everyone has their own way to enjoy themselves."
    m 2j "We can celebrate Kwanzaa together too, [player]."
    return

init 5 python:
    import datetime

    now = datetime.datetime.now()
    if now.day == 31 and now.month == 12 and not seen_event('monika_newyear1'):
        queueEvent('monika_newyear1')

label monika_newyear1:
    m 1a "[player]! It's almost time, isn't it?"
    m "It's incredible to think that the year is almost over."
    m 1e "Time flies by so quickly."
    m 1j "Especially when I get to see you so often."
    m 1a "Well, there's still a bit of time left before midnight."
    m 2b "We might as well enjoy this year while it lasts."
    m 1l "Usually, I'd reprimand you for staying up late, but..."
    m 1a "Today is a special day."
    m "Do you have any resolutions, [player]?"
    menu:
        "Yes.":
            m 1a "It's always nice to set goals for yourself in the coming year."
            m 2l "Even if they can be hard to reach or maintain."
            m 2a "I'll be here to help you, if need be!"
            m 1j "My resolution is to be an even better girlfriend for you, my love."

        "No.":
            m 1e "Oh, is that so?"
            m 2a "You don't have to change. I think you're wonderful the way you are."
            m 1c "But if anything does come to mind before the clock strikes twelve, do write it down for yourself."
            m 1j "Maybe you'll think of something that you want to do, [player]."
    return

init 5 python:
    import datetime

    now = datetime.datetime.now()
    if now.day == 1 and now.month == 1 and not seen_event('monika_newyear2'):
        queueEvent('monika_newyear1')

label monika_newyear2:
    m 1b "[player]!"
    m 1e "We've been through a lot together this past year, huh?"
    m 1a "I'm so happy, knowing we can spend even more time together."
    m 2j "Let's make this year as wonderful as the last one, okay?"
    m 1a "I love you, [player]."
    m 1j "Happy new year~"
    return

init 5 python:
    import datetime

    now = datetime.datetime.now()
    endofwinter = datetime.datetime(2018,1,15)
    if now < endofwinter:
        for key in ['cold','weather','cozy','warm','warmth','winter']:
            monika_topics.setdefault(key,[])
            monika_topics[key].append('monika_cozy') #id
        monika_random_topics.append('monika_cozy')

label monika_cozy:
    m 1a "Do you know the one thing I love about the cold weather, [player]?"
    m 3j "Anything warm feels really nice~"
    m 3a "Those who get cold hands really appreciate that feeling."
    m "It's like feeling a loved one's embrace~"
    m 2b "You also get to wear your winter clothes that have been stuck in your closet."
    m "Finally able to whip out your winter fashion set is always a feeling."
    m 2a "But you know what the best way to warm yourself up is?"
    m 2j "Cuddling with the one you love in front of the fireplace~"
    m 2a "Just sitting there under a warm blanket, sharing a hot beverage."
    m 3e "Ah, if I got to feel your warmth everytime we cuddle, I'd wish for cold weather everyday!"
    m 1j "I'd never let you go once I got a hold of you, [player]~"
    return

init 5 python:
    import datetime

    now = datetime.datetime.now()
    endofwinter = datetime.datetime(2018,1,15)
    if now < endofwinter:
        for key in ['cold','weather','snow','ice','winter']:
            monika_topics.setdefault(key,[])
            monika_topics[key].append('monika_snow') #id
        monika_random_topics.append('monika_snow')

label monika_snow:
    m 5a "Does it ever snow where you live, [player]?"
    m 4j "I've always liked the peaceful aura it seems to give off."
    m 4b "It usually accompanies the holiday season in a lot of places, too."
    m 1c "After reading a bit about other seasons that come and go, I don't think I'd enjoy a sweltering summer very much..."
    m 1a "It's just that I'd prefer a balmy and gentle heat more, ahaha."
    m 3b "But snow is just so much more... tranquil and intimate, you know?"
    m 1e "There's a quiet beauty in watching a soft, white blanket of ice tuck the world away to sleep."
    return

init 5 python:
    import datetime

    now = datetime.datetime.now()
    endofwinter = datetime.datetime(2018,1,15)
    if now < endofwinter:
        for key in ['winter','snowman','outdoors','decorate','decorating']:
            monika_topics.setdefault(key,[])
            monika_topics[key].append('monika_winter') #id
        monika_random_topics.append('monika_winter')
        
label monika_winter:
    m 1d "Oh, [player]!"
    m 2a "What do you think about winter?"
    m "All sorts of fun activities only come around during this time..."
    m 2b "Playing with the snow is usually something that can be enjoyed a few times a year."
    m "Building a snowman, sledding…"
    m 2m "Even staying indoors seems so much more comfortable when there’s snow outside."
    m 4b "The festivities are lovely too, of course."
    m 1c "I wonder if it's acceptable to start decorating..."
    m 1 "But I hope you’re enjoying yourself during this merry season, [player]."
    m 1a "You can always spend some time with me, if you want to chill..."
    m 3m "Or maybe you’d rather heat things up~?"
    m 3l "Ahaha! I'm only teasing you, [player]~"
    m 1j "Just do be sure to visit often, okay?"
    return

init 5 python:
    import datetime

    now = datetime.datetime.now()
    endofwinter = datetime.datetime(2018,1,15)
    if now < endofwinter:
        for key in ['snow ball','snowball']:
            monika_topics.setdefault(key,[])
            monika_topics[key].append('monika_snowballfight') #id

label monika_snowballfight:
    m 1a "Snowball fighting?"
    m 1k "Having one with you sounds like a ton of fun, [player]!"
    m 1r "Fair warning, though..."
    m 1n "I've got quite the throwing arm."
    m 1j "So I certainly won't be going easy on you!"
    m 1m "Maybe you're better at snowball fights than Pong~?"
    return

init 5 python:
    import datetime

    now = datetime.datetime.now()
    endofwinter = datetime.datetime(2018,1,15)
    if now < endofwinter:
        for key in ['iceskate','iceskating','skate','skating','winter','cold','ice']:
            monika_topics.setdefault(key,[])
            monika_topics[key].append('monika_iceskating') #id
        monika_random_topics.append('monika_iceskating')

label monika_iceskating:
    m 1d "Hey, [player], do you know how to ice skate?"
    m 1b "It's a really cool thing to learn!"
    m 1a "Especially for those who can do a lot of athletic tricks."
    m 3n "I mean, it's hard enough to keep your balance on ice in the first place."
    m 2e "Being able to turn it into a performance is really impressive."
    m 2c "There's actually a lot of ways to ice skate!"
    m "Figure skating, speed skating, and even in theatrical performances!"
    m 1o "Though, while doing something like that sounds like a great time..."
    m 1n "I don't know if I'll be able to join in on the fun anytime soon."
    m 1e "But having you here with me is enough to keep me happy."
    m 1k "I love you so much, [player]~"
    return

init 5 python:
    import datetime

    now = datetime.datetime.now()
    christmas_time = datetime.datetime(2017,12,26)
    if now < christmas_time:
        for key in ['Christmas','gifts','you want','present','gift','presents']:
            monika_topics.setdefault(key,[])
            monika_topics[key].append('monika_whatiwant') #id
        monika_random_topics.append('monika_whatiwant')

label monika_whatiwant:
    m 5a "Oh, [player], isn't it lovely around the holidays?"
    m 5b "I hope you don't mind, but I have a little something special to say today."
    m 1j "Ehehe, I hope it's not too cheesy..."
    m 3l "Here goes."
    m 1r "..."
    m 1e "You really are the joy to my world, [player]."
    m "A thousand glittering stars couldn't match your brilliance."
    m 1 "This melancholy, frostbitten heart of mine needs only your warmth to beat anew."
    m "Underneath the sprawling branches of yonder Christmas tree..."
    m 1e "You'll always be the only present I will ever need."
    m 1r "..."
    m 4l "Ahaha! Sorry if that sounded too serious!"
    m 2a "Winter's a wonderful time to read some lengthy works."
    m 1q "But..."
    m 1r "I wasn't lying, [player]."
    m 3e "Don't worry about getting me a present."
    m 4j "After all, I have you. And that's all I want."
    m 1k "I love you with all my heart, [player]~"
    return

init 5 python:
    import datetime

    now = datetime.datetime.now()
    endofwinter = datetime.datetime(2018,1,15)
    if now < endofwinter:
        for key in ['winter','snowman','snowmen','snow']:
            monika_topics.setdefault(key,[])
            monika_topics[key].append('monika_snowman') #id
        monika_random_topics.append('monika_snowman')

label monika_snowman:
    m 2q "Hmm..."
    m 2c "[player], have you ever stopped to think about what the life of a snowman is like?"
    m 2o "Like, I know they're not alive, but..."
    m "Just standing there, all by themselves. It must get lonely, from time to time."
    m 1q "..."
    m 1i "I know how that feels."
    m 3p "Or I used to, anyway."
    m 1a "But then I found the love of my life!"
    m 1c "I bet it's not all bad, though."
    m 1 "You could watch the snow fall, or admire the stars."
    m 1a "Or see an aurora!"
    m 1j "Just imagine it!"
    m 1j "I'd be a happy, little snow lady."
    m 1a "What about you, [player]?"
    m 3 "What would you do, if you were made of snow?"
    menu:
        "I'd watch the scenery change as time passes.":
            m 1k "I feel the same way, too!"
            m 3b "Wouldn't it just be breathtaking?"
            m 1k "You better save a spot for me, though~!"

        "I'd melt for you.":
            m 1k "Ahaha!"
            m 1l "That was so cheesy!"
            m 1e "And yet, so sweet."
            m 1j "Thank you, [player]."

        "I'd freeze up!":
            m 1k "Ahaha!"
            m 3e "Technically, it would be too late to worry about something like that."
            m 1m "Maybe being a snowman wouldn't be too great."
            m 5a "A warm fire with your loved one and a steaming cup of hot chocolate is much better, no?"
    return

init 5 python:
    import datetime

    now = datetime.datetime.now()
    endofwinter = datetime.datetime(2018,1,15)
    if now < endofwinter:
        for key in ['winter','sled','sledding']:
            monika_topics.setdefault(key,[])
            monika_topics[key].append('monika_sledding') #id
        monika_random_topics.append('monika_sledding')

label monika_sledding:
    m 3a "You know what I would love to do with you?"
    m 1j "Sledding!"
    m 2a "You might think it's only for kids, but I think it could be fun for us, too!"
    m 4 "We could try using an inner tube, a kicksled, a saucer, or even a traditional toboggan."
    m "I've heard each one gives a different experience. Plus, both of us could easily fit on a toboggan."
    m 1l "The kicksled is a bit small, though."
    m 1k "Ahaha!"
    m 1m "I'd have to sit in your lap for that one."
    m 1n "And I'd still be at risk of tumbling off."
    m 1e "But I know you wouldn't let that happen. You'd hold me tight, right~?"
    m 1j "That would probably be the best part."
    return

init 5 python:
    import datetime

    now = datetime.datetime.now()
    endofwinter = datetime.datetime(2018,1,15)
    if now < endofwinter:
        for key in ['mistletoe','kiss']:
            monika_topics.setdefault(key,[])
            monika_topics[key].append('monika_mistletoe') #id
        monika_random_topics.append('monika_mistletoe')

label monika_mistletoe:
    m 1a "Say, [player]."
    m 1b "You've heard about the mistletoe tradition, right?"
    m 1m "When lovers end up underneath it, they're expected to kiss."
    m 1a "It actually originated from Victorian England!"
    m 1l "A man was allowed to kiss any woman standing underneath mistletoe..."
    m 1p "And any woman who refused the kiss was cursed with bad luck."
    m 1o "..."
    m 3p "Come to think of it, that sounds more like taking advantage of someone."
    m 1j "But I'm sure it's different now!"
    m 1j "Perhaps one day we'll be able to kiss under the mistletoe, [player]."
    m 2b "...Maybe I can even add one in here!"
    m 1a "Ehehe~"
    return

init 5 python:
    import datetime

    now = datetime.datetime.now()
    endofwinter = datetime.datetime(2018,1,15)
    if now < endofwinter:
        for key in ['relax','winter','danger']:
            monika_topics.setdefault(key,[])
            monika_topics[key].append('monika_relax') #id
        monika_random_topics.append('monika_relax')

label monika_relax:
    m 1j "Isn't winter a beautiful time of year, [player]?"
    m 1a "The glistening, white snow, the bright and colorful lights~"
    m 3k "I love it."
    m 1q "..."
    m 1i "There are a few dangers, though."
    m 3h "Like blizzards, or icy roads..."
    m 1o "And the cold, of course."
    m 1f "If it gets bad, just stay home and stay safe, okay?"
    m 1q "After all, when the weather gets bad..."
    m "..."
    m 3l "So isn't it best to relax at home?"
    m 1b "Wearing pajamas, drinking hot chocolate, reading a good book, and..."
    m 1j "Talking to me."
    m 1k "Ehehe~"
    m 1g "But seriously, don't go outside if it gets too bad."
    m 1e "Please stay safe, [player]."
    return

init 5 python:
    import datetime

    now = datetime.datetime.now()
    endofwinter = datetime.datetime(2018,1,15)
    if now < endofwinter:
        for key in ['snow','canvas','painting','paint']:
            monika_topics.setdefault(key,[])
            monika_topics[key].append('monika_snowcanvas') #id
        monika_random_topics.append('monika_snowcanvas')

label monika_snowcanvas:
    m 3c "Have you ever looked at snow and thought it resembles a blank canvas?"
    m 1e "I know I'm not as artistically inclined as someone like Yuri..."
    m 3b "But packing a few spray bottles with water and food coloring could make for a fun day!"
    m 3j "Just step outside and let your imagination run wild!"
    m 1b "Doesn't having so much space to paint sound wonderful?"
    m 1l "Although... don't draw anything indecent, okay?"
    m 3 "And make sure the snow is packed down tightly, too."
    m 1e "I'd love to do this with you some day."
    m 3k "Maybe you can paint something for me when that happens, [player]."
    return

init 5 python:
    import datetime

    now = datetime.datetime.now()
    endofwinter = datetime.datetime(2018,1,15)
    if now < endofwinter:
        for key in ['cold','hypothermia','freeze','freezing']:
            monika_topics.setdefault(key,[])
            monika_topics[key].append('monika_hypothermia') #id
        monika_random_topics.append('monika_hypothermia')

label monika_hypothermia:
    m 2f "Hey, [player]."
    m 2o "I know winter is a time to be cheery and carefree."
    m "But there's something I need to make sure you know."
    m 2g "Please remember to bundle up, okay?"
    m 2d "All the snow laying about might look inviting..."
    m 2f "But it might be dangerous if you expose yourself too much."
    m 2g "I don't want you catching hypothermia, [player]."
    m 4c "So put on that coat, those gloves, and the softest hat you can find."
    m 1e "And stay safe."
    m "Your health means a lot to me, [player]."
    m "I hope you take my concerns seriously."
    m 1j "Okay, snowflake?"
    return

init 5 python:
    import datetime

    now = datetime.datetime.now()
    christmas_time = datetime.datetime(2017,12,26)
    if now < christmas_time:
        for key in ['christmas','carols','carolling','sing','singing']:
            monika_topics.setdefault(key,[])
            monika_topics[key].append('monika_carolling') #id
        monika_random_topics.append('monika_carolling')

label monika_carolling:
    m 1c "Hey, [player]..."
    m 3d "Have you ever gone carolling before?"
    m 1a "Going door to door in groups, singing to others during the holidays..."
    m 1j "It just feels heartwarming to know people are spreading joy, even with the nights so cold."
    m 3a "Do you like singing Christmas carols, [player]?"
    menu:
        "Yes.":
            m 1j "I'm glad you feel the same way, [player]!"
            m 1a "What's your favorite song?"
            m 3b "Mine is definitely 'Jingle Bells!'"
            m 1k "It's just such an upbeat, happy tune!"
            m 1e "Maybe we can sing together someday."
            m 1j "Ehehe~"
        "No.":
            m 1d "Oh?"
            m 1f "I see..."
            m 1e "Regardless, I'm sure you're also fond of that special cheer only Christmas songs can bring."
            m 3j "Sing with me sometime, okay?"
    return

init 5 python:
    import datetime

    now = datetime.datetime.now()
    christmas_time = datetime.datetime(2017,12,26)
    if now < christmas_time:
        for key in ['christmas','carols','carolling','sing','singing','jingle','bells']:
            monika_topics.setdefault(key,[])
            monika_topics[key].append('monika_jinglebells') #id
        monika_random_topics.append('monika_jinglebells')

label monika_jinglebells:
    m 1j "~hum hm hm, hum hm hum~"
    m 1d "Oh!"
    m 1l "I'm sorry, [player]."
    m 1j "I let my mind wander a bit when I think about the festive tunes that come along around this time of year."
    m 3k "I just love how the songs make everything so lively and cheerful."
    m 1j "That warm, fuzzy feeling that you get whenever you relax in front of the fireplace..."
    m 1e "Times like these make me appreciate having you around with me even more, [player]~"
    m 3d "Speaking of holiday songs..."
    m 1b "I think 'Jingle Bells' is a great one!"
    m "You know, the one that goes like..."
    m 1k "'{i}Jingle bells, jingle bells{/i}'"
    m "'{i}Jingle all the way~'{/i}"
    m 1b "{i}'Oh! what fun it is to ride...'{/i}"
    m "{i}'In a one-horse open sleigh!'{/i}"
    m 1k "'{i}Hey~!{/i}'"
    m 1l "Ahaha! I can't get enough of them~"
    m 1e "They easily cheer me up everytime."
    m 1k "It'd be more fun if you could sing with me next time, [player]!"
    return

init 5 python:
    import datetime

    now = datetime.datetime.now()
    christmas_time = datetime.datetime(2017,12,26)
    if now < christmas_time:
        for key in ['carriage','sleigh','horse','carriage']:
            monika_topics.setdefault(key,[])
            monika_topics[key].append('monika_sleigh') #id
        monika_random_topics.append('monika_sleigh')

label monika_sleigh:
    m 2c "Hey [player], a pretty nice thought just crossed my mind..."
    m 4a "Have you ever heard of carriage rides?"
    m 1k "When I get out of this place, we should totally go on one!"
    m 1b "Oh, I bet it would be magical!"
    m 1a "Nothing but the clip-clop of the horse's hooves against the pavement..."
    m "And the colorful array of Christmas lights shining in the night..."
    m 3b "Wouldn't that be so romantic, [player]?"
    m 1m "Maybe we could even take a soft, fleece blanket along to cuddle under."
    m 1l "Oh~"
    m "I wouldn't be able to contain myself. My heart would burst!"
    m 1e "The warmth of your body against mine, wrapped within the gentle cloth~"
    m "Fingers entwined..."
    m 1n "And at the perfect moment, you lean in to me and our lips touch..."
    m 1m "I really want to do that when I get there, [player]."
    m 3j "Wouldn't that be so lovely?"
    m 1k "An experience like that with you would be so breathtaking~"
    return

init 5 python:
    import datetime

    now = datetime.datetime.now()
    hanukkah_time = datetime.datetime(2017,12,21)
    if now < hanukkah_time:
        for key in ['hanukkah','dreidel','holidays','gelt']:
            monika_topics.setdefault(key,[])
            monika_topics[key].append('monika_dreidel') #id
        monika_random_topics.append('monika_dreidel')

label monika_dreidel:
    m 3a "[player], did you know that each side of a dreidel actually means something?"
    m 1a "Nun, Gimel, Hel, Shim."
    m 1 "These stand for Nes Gadol Hayah Sham - A Great Miracle Happened There."
    m "It refers to the Hanukkah story of how one day's worth of oil lasted for eight days."
    m 3a "Over in Israel, they change the last word to 'poh', making it 'A Great Miracle Happened Here.'"
    m 1j "Maybe next year, I'll have one to spin~"
    m 1m "I don't have one, unfortunately."
    m 1a "But for now, [player], do you have any gelt?"
    m 1b "The chocolate coin variety tastes really good."
    m 1k "Though money is always good too, ehehe~"
    return
