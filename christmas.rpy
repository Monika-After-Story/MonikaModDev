label monika_christmas
    m 2b "[player]! Do you know what day it is?"
    m 4k "Of course you do. It's Christmas!"
    m "Merry Christmas, snowflake!"
    m 3j "Ahaha! I can't believe that it's finally here!"
    m 3a "I'm so, so happy that you decided to spend some of it with me."
    m 4d "Remember to go share the holiday cheer with your family and friends, though."
    m 2e "After all, they're important, too. And I'm sure that they would love to see you on this special day."
    m 1q "..."
    m 3f "Hey..."
    m 4e "...[player], I love you."
    m 3e "Maybe it's just the snow, or the decorations, or even the mistletoe getting to me..."
    m 1d "Ah-"
    m 2l "I didn't set one up! Please don't be worried!"
    m 2n "Ehehe..."
    m 1e "...My heart's fluttering like crazy right now, [player]."
    m "To think that you'd actually come and visit me on such a wonderful holiday..."
    m 2n "Don't get me wrong, I knew that you would, but..."
    m 1e "Actually having you here with me on Christmas, with just the two of us..."
    m 1j "Ahaha~"
    m 2b "It's what every couple dreams about during the holidays, no?"
    m 1e "Snuggling up against each other by a fireplace, watching the snow gently fall..."
    m 1j "I'm forever grateful I got this chance because of you, [player]."
    m 1k "I love you. Forever and ever."
    m 1e "Merry Christmas, [player]."
    
label monika_kwanzaa
    m 1b "[player], have you ever heard of Kwanzaa?"
    m 1a "It's a week-long festival celebrating African American history that starts the day after Christmas."
    m 2a "The word 'Kwanzaa' comes from the Swahili phrase 'matunda ya kwanza', which means 'first fruits'."
    m "Even if Christmas is main event for many, other holidays are always interesting to learn about."
    m 5a "Apparently, people celebrate the tradition by decorating their homes with bright adornments."
    m "There's also music to enjoy, and a candleholder called the 'kinara' to light a new fire with each passing day."
    m 1j "Doesn't it remind you of some other holdiays? The concepts certainly seem familiar."
    m 1a "In the end, having a day to celebrate is the important part. Everyone has their own way to enjoy themselves."
    m 2j "We can celebrate Kwanzaa together too, [player]."
    
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
    m 5a "Oh, [player], isn't it lovely around the holidays?"
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
    
label monika_snowman
    m 1q "Hmm..."
    m 3b "[player], have you ever stopped to think about what the life of a snowman is like?"
    m 1a "Like, I know they're not alive, but..."
    m "Just standing there, all by themselves. It must get lonely, from time to time."
    m 1e "..."
    m "I know how that feels. Or I used to, anyway."
    m 1j "But then I found the love of my life!"
    m 2b "I bet it's not all bad, though."
    m "You could watch the snow fall, or admire the stars."
    m 2a "Even an aurora is possible!"
    m 1j "Just imagine it!"
    m 5a "I'd be a happy, little snow lady."
    m "What about you, sweetie?"
    m "What would you do, if you were made of snow?"
    menu:
        "I'd watch the scenery change as time passes."
            m 1k "I feel the same way, too!"
            m 3b "Wouldn't it just be breathtaking?"
            m 1k "You'd better save a spot for me, though~!"
        
        "I'd melt for you."
            m 1k "Ahaha!"
            m 1a "That was so cheesy!"
            m 1e "And yet, so sweet."
            m 1a "Thank you, love."
        
        "I'd freeze up!"
            m 1k "Ahaha!"
            m 1a "Technically, it would be too late to worry about something like that."
            m 1e "Maybe being a snowman wouldn't be too great."
            m 5a "A warm fire with your loved one and a steaming cup of hot chocolate is much better, no?"
            
label monika_sledding
    m 3a "You know what I would love to do with you?"
    m "Sledding."
    m 5b "I know you might think that sort of thing is only for kids."
    m 5a "But I think it could be fun for us, too!"
    m 4b "We could try using an inner tube, a kicksled, a saucer, or even a traditional toboggan."
    m 1a "I've heard each one gives a different experience. Plus, both of us could easily fit on a toboggan."
    m 1l "The kicksled is a bit small, though."
    m 1k "Ahaha!"
    m 1a "I'd have to sit in your lap for that one."
    m 1g "And I'd still be at risk of tumbling off."
    m 1b "But I know you wouldn't let that happen. You'd hold me tight, right~?"
    m 1j "That would probably be the best part."

label monika_mistletoe
    m 1a "Say, [player]."
    m 2b "You've heard about the mistletoe tradition, right?"
    m 1j "When lovers end up underneath the decoration, they're expected to kiss."
    m 1a "It actually originated from Victorian England!"
    m "A man was allowed to kiss any woman standing underneath mistletoe..."
    m 1l "And any woman who refused the kiss was cursed with bad luck."
    m 1j "Perhaps one day we'll be able to kiss under the mistletoe, [player]."
    m 2b "...Maybe I can even add one in here!"
    m 1a "Ehehe~"
    
 label monika_relax
    m 3j "Isn't winter a beautiful time of year, [player]?"
    m 3a "The glistening, white snow, the bright and colorful lights~"
    m 4b "I love it."
    m 1e "..."
    m 1e "There are a few dangers, though."
    m "Like blizzards, or icy roads..."
    m 1p "And the cold, of course."
    m 2a "If it gets bad, just stay home and stay safe, okay?"
    m 1d "After all, when the weather gets bad..."
    m 1a "Isn't it best to relax at home?"
    m 1b "Wearing pajamas, drinking hot chocolate, reading a good book, and..."
    m 1j "Talking to me."
    m 1j "Ehehe~"
    m 1d "But seriously, don't go outside if it gets too bad."
    m 1a "Please stay safe, [player]."

label monika_snowcanvas
    m 2a "Have you ever looked at snow and thought it resembles a blank canvas?"
    m 1e "I know I'm not as artistically inclined as someone like Yuri..."
    m 4b "But packing a few spray bottles with water and food coloring could make for a fun day!"
    m 3b "Just step outside and let your imagination run wild!"
    m 1a "Doesn't having so much space to paint sound wonderful?"
    m 1l "Although... don't draw anything indecent, okay?"
    m 2d "And make sure the snow is packed down tightly, too."
    m 3a "I'm sure that the time to try something like this will come soon."
    m 3k "Maybe you can paint something for me when that happens, [player]."

label monika_hypothermia
    m 1o "Hey, [player]."
    m 1g "I know winter is a time to be cheery and carefree."
    m "But there's something I need to make sure you know."
    m 2f "Please remember to bundle up, okay?"
    m 3d "All the snow laying about might look inviting..."
    m 3f "But it might be dangerous if you expose yourself too much."
    m 1e "I don't want you catching hypothermia, [player]."
    m 4d "So put on that coat, those gloves, and the softest hat you can find." 
    m 1e "And stay safe."
    m 3a "Your health means a lot to me."
    m "I hope you take my concerns seriously."
    m 3j "Okay, snowflake?"

label monika_carolling
    m 2a "Hey, [player]..."
    m 1b "Have you ever gone carolling before?"
    m 1a "Going door to door in groups, singing to others during the holidays..."
    m 1k "It just feels heartharming to know people are spreading joy, even with the nights so cold."
    m 2b "Do you like singing christmas carols, [player]?"
        menu:
        "Yes."
            m 1b "I'm glad you feel the same way, [player]!"
            m 1a "What's your favorite song?"
            m 2a "Mine is definitely 'Jingle Bells'!"
            m 1k "It's just such an upbeat, happy tune!"
            m 5a "Maybe we can sing together someday."
            m 1j "Ehehe~"
        "No."
            m 1d "Oh?"
            m 1c "I see..."
            m 2a "Regardless, I'm sure you're also fond of that special cheer only Christmas songs can bring."
            m 5a "Sing with me sometime, okay?"
