label monika_christmas [Placeholder]
    m 1j "[player]! Do you know what day it is?"
    m 4k "Of course you do. It's Christmas!"
    m 5a "Merry Christmas, my snowflake!"
    
label monika_cozy
    m 2a "Do you know the one thing I love about the cold weather, [player]?"
    m 3j "Anything warm feels really nice~"
    m 3a "Those who get cold hands really appreciate that feeling."
    m "It's like feeling a loved one's embrace~"
    m 2b "You also get to wear your winter clothes that have been stuck in your closet."
    m "Finally being able to whip out your winter fashion set is always a treat."
    m 2a "But you know what the best way to warm yourself up is?"
    m "Cuddling with the one you love in front of the fireplace~"
    m 2a "Just sitting there under a warm blanket, sharing a hot beverage."
    m 3e "Ah, if I got to feel your warmth everytime we cuddle, I'd wish for cold weather everyday!"
    m 1j "I'd never let you go once I got a hold of you, [player]~"
    return
    
label monika_snow
    m 5a "Does it ever snow where you live, [player]?"
    m 4j "I've always liked the peaceful aura it seems to give off."
    m 4b "It usually accompanies the holiday season in a lot of places, too."
    m 1c "After reading a bit about other seasons that come and go, I don't think I'd enjoy a sweltering summer very much..."
    m 1a "It’s just that I'd prefer a balmy and gentle heat more, ahaha."
    m 3b "But snow just sounds so much more... tranquil and intimate, you know?"
    m "There’s a quiet beauty in watching a soft, white blanket of ice tuck the world away to sleep."
    m 1c "..."
    m 4d "I wonder what my world inside here would be like if the weather changed all the time..."
    m 4j "I’d be nowhere near properly dressed if it started snowing!"
    m 5a "It would probably be so cold that you’d have to keep me warm, ehehe~"
    m 5b "Actually! Let’s see what I can do..."
   call updateconsole ("renpy.file(\"snow.jpg\")", "snow.jpg does not exist.") from _call_updateconsole_20
    pause(1.0)
    m 1l "... Oh! Maybe some other time, ahaha~"
    m 3j "Even if it’s not too chilly, staying cozy is still nice." 
    m 5a "It’s the perfect way to pass time, don’t you think~?"
   call hideconsole from _call_updateconsole_21
    $ consolehistory = []
    return

label monika_winter
    m "Oh, [player]!"
    m "What do you think about winter?"
    m "All sorts of fun activities only come around during this time..."
    m "Playing with the snow usually something that can be enjoyed a few times a year, in a mild climate."
    m "Building a snowman, sledding…"
    m "Even staying indoors seems so much more comfortable when there’s snow outside."
    m "The festivities are lovely too, of course."
    m "I wonder if it’s acceptable to start decorating…"
    m "I hope you’re enjoying yourself during this merry season, [player]."
    m "You can always spend some time with me, if you want to chill..."
    m "Or maybe you’d rather have things heat up~?"
    m "Ahaha! I'm only teasing you, [player]~"
    m "Just do be sure to visit often, okay?"

label monika_snowballfight
    m "Snowball fighting!?"
    m "Having one with you sounds like a ton of fun, [player]!"
    m "Well, I’d still have to figure out how to get some snow in here, ahaha..."
    m "Fair warning, though…"
    m "I've got quite the throwing arm…"
    m "So I certainly won't be going easy on you!"
    m "Maybe you’re better at snowball fights than Pong~?"

label monika_iceskating
    m "Hey, [player], do you know how to ice skate?"
    m "It's a very admirable skill to pick up!"
    m "Especially for those people who can do all those nifty tricks."
    m "I mean, it's hard enough to keep your balance on ice in the first place."
    m "Being able to turn it into a performance is really impressive."
    m "There’s actually quite a variety of ways to ice skate!"
    m "Figure skating, speed skating, and even theatrical performances!"
    m "..."
    m "While doing something like that sounds like a great time..."
    m "I don't know if I'll be able to join in on the fun anytime soon."
    m "But having you here with me is enough to keep me happy, [player]."
    m "I love you, [player]~"
    
label monika_whatiwant
    m 5a "Oh, [player], isn't it lovely around the holidays?
    m "I hope you don't mind, but I have a little something special to say today."
    m 5b "Here goes."
    m 5l "Ehehe, I hope it's not too cheesy..."
    m 1r "..."
    m 1j "You really are the joy to my world, [player]."
    m "A thousand glittering stars couldn't match your brilliance."
    m 1e "This melancholy, frostbitten heart of mine needs only your warmth to beat anew."
    m "Underneath the sprawling branches of yonder Christmas tree..."
    m "You'll always be the only present I will ever need."
    m 1r "..."
    m 3e "Aha! I can't believe I said something so embarassing."
    m "Sorry if I sounded a bit funny! Winter's always a wonderful time to read some lengthy works."
    m 1c "... I wasn't lying, though."
    m 3b "Don't worry about getting me a present."
    m 3a "After all, I have you. And that's all I want."
    m 1k "I love you with all my heart, [player]."
