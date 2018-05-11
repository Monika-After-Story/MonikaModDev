init python:
    class RectCluster(object):
        def __init__(self, theDisplayable, numRects=12, areaWidth = 30, areaHeight = 30):
            self.sm = SpriteManager(update=self.update)
            self.rects = [ ]
            self.displayable = theDisplayable
            self.numRects = numRects
            self.areaWidth = areaWidth
            self.areaHeight = areaHeight
            
            for i in range(self.numRects):
                self.add(self.displayable)
        
        def add(self, d):
            s = self.sm.create(d)
            s.x = (random.random() - 0.5) * self.areaWidth * 2
            s.y = (random.random() - 0.5) * self.areaHeight * 2
            s.width = random.random() * self.areaWidth / 2
            s.height = random.random() * self.areaHeight / 2
            self.rects.append(s)
        
        def update(self, st):
            for s in self.rects:
                s.x = (random.random() - 0.5) * self.areaWidth * 2
                s.y = (random.random() - 0.5) * self.areaHeight * 2
                s.width = random.random() * self.areaWidth / 2
                s.height = random.random() * self.areaHeight / 2
            return 0

image n_rects_ghost1:
    RectCluster(Solid("#000"), 4, 15, 5).sm
    pos (580, 270)
    size (20, 25)
    alpha 0.0
    8.0
    easeout 12 alpha 1.0

image n_rects_ghost2:
    RectCluster(Solid("#000"), 4, 15, 5).sm
    pos (652, 264)
    size (20, 25)
    alpha 0.0
    8.0
    easeout 12 alpha 1.0

image n_rects_ghost3:
    RectCluster(Solid("#000"), 4, 15, 5).sm
    pos (616, 310)
    size (25, 15)
    alpha 0.0
    8.0
    easeout 12 alpha 1.0

image n_rects_ghost4:
    RectCluster(Solid("#000"), 4, 15, 5).sm
    pos (735, 310)
    size (25, 20)
    0.5
    easeout 0.25 zoom 4.5 xoffset 250 yoffset -250

image n_rects_ghost5:
    RectCluster(Solid("#000"), 4, 15, 5).sm
    pos (740, 376)
    size (25, 20)
    0.5
    easeout 0.25 zoom 4.5 xoffset 250 yoffset -100

label natsuki_exclusive2_1:
    scene bg club_day
    with wipeleft_scene
    n "Ugh...!"
    "I hear Natsuki utter an exasperated sigh from within the closet."
    "She seems to be annoyed by something."
    "I approach her, in case she needs a hand."
    play music t6 fadeout 1
    scene bg closet
    show natsuki 4r zorder 2 at t11
    with wipeleft_scene
    $ style.say_dialogue = style.normal
    mc "You looking for something in there?"
    $ style.say_dialogue = style.edited
    n 4x "fucking monikammmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm"
    $ style.say_dialogue = style.normal
    $ _history_list[-1].what = "Freaking Monika..."
    n "She never puts my stuff back in the right spot!"
    n "What's the point in keeping your collection organized if someone else is just gonna mess it up?"
    "Natsuki slides a bunch of stacked books and boxes across the shelf."
    mc "Manga..."
    n 2c "You read manga, right?"
    mc "Ah--"
    mc "...Sometimes..."
    "Manga is one of those things where you can't admit you're really into it until you figure out where the other person stands."
    mc "...How did you know, anyway?"
    n 2k "I heard you bring it up at some point."
    n "Besides, it's kind of written on your face."
    "What's that supposed to mean...?"
    mc "I-I see..."
    "There's a lone volume of manga amidst a stack of various books on the side of one of the shelves."
    "Curious, I pull it out of the stack."
    n 1b "{i}There{/i} it is!"
    "Natsuki snatches it out of my hand."
    "She then turns to a box of manga and slips the volume right into the middle of the rest."
    n 4d "Aah, much better!"
    n "Seeing a box set with one book missing is probably the most irritating sight in the world."
    mc "I know that feel..."
    "I get a closer look at the box set she's admiring."
    mc "Parfait Girls...?"
    "It's a series I've never heard of in my life."
    "That probably means it's either way out of my demographic, or it's simply terrible."
    n 5g "If you're gonna judge, you can go do it through the glass on that door."
    "She points to the classroom door."
    mc "H-Hey, I wasn't judging anything...!"
    mc "I didn't even say anything."
    n 5c "It was the tone of your voice."
    $ style.say_dialogue = style.normal
    n "But I'll tell you one thing, [player]."
    n 4l "Consider this a lesson straight from the Literature Club:{nw}"
    $ _history_list[-1].what = "Consider this a lesson straight from the Literature Club: Don't judge a book by its cover!"
    $ style.say_dialogue = style.edited
    n "don't judge a bookkkkkkkkkkkkkkkkk kkkkk kk{space=20}k{space=40}k{space=120}k{space=160}k{space=200}k"
    $ style.say_dialogue = style.normal
    $ _history_list.pop()
    n "In fact--"
    "Natsuki pulls out the first volume of Parfait Girls from the box."
    n "I'm gonna show you exactly why!"
    "She shoves the book right into my hands."
    mc "Ah..."
    "I stare at the cover."
    "It features four girls in colorful attire striking animated feminine poses."
    "It's...exceedingly \"moe\"."
    n 4b "Don't just stand there!"
    mc "Uwa--"
    show natsuki zorder 1 at thide
    hide natsuki
    "Natsuki grabs my arm and pulls me out of the closet."
    "She then takes a seat against the wall, beneath the windowsills."
    "She pats on the ground next to her, signaling me to sit there."
    show bg club_day
    show natsuki 2a zorder 2 at t11
    with wipeleft
    mc "Wouldn't chairs be more comfortable...?"
    "I take my seat."
    n 2k "Chairs wouldn't work."
    n "We can't read at the same time like that."
    mc "Eh? Why's that?"
    mc "Ah...I guess it's easier to be close together like this..."
    n 2o "--!"
    n 5r "D-Don't just say that!"
    n "You'll make me feel weird about it!"
    "Natsuki crosses her arms and scootches an inch away from me."
    mc "Sorry..."
    show natsuki 5g
    "I didn't exactly expect to be sitting this close to her, either..."
    "Not that I can say it's a particularly bad thing."
    "I open the book."
    "It's only a few seconds before Natsuki once again inches closer, reclaiming the additional space while she hopes I won't notice."
    "I can feel her peering over my shoulder, much more eager to begin reading than I am."
    n 1k "Wow, how long has it been since I read the beginning...?"
    mc "Hm?"
    mc "You don't go back and flip through the older volumes every now and then?"
    n 2k "Not really."
    n "Maybe sometimes after I've already finished the series."
    n 2c "Hey, are you paying attention?"
    mc "Uh..."
    "I am, but nothing's really happened yet, so I can talk at the same time."
    "It looks like it's about a bunch of friends in high school."
    "Typical slice-of-life affair."
    "I kind of grew out of these, since it's rare for the writing to be entertaining enough to make up for the lack of plot."
    $ persistent.clear[0] = True
    $ renpy.save_persistent()
    scene n_cg1_bg
    show n_cg1_base
    with dissolve_cg
    mc "...Are you sure this isn't boring for you?"
    n "It's not!"
    mc "Even though you're just watching me read?"
    n "Well...!"
    n "I'm...fine with that."
    mc "If you say so..."
    mc "...I guess it's fun sharing something you like with someone else."
    mc "I always get excited when I convince any of my friends to pick up a series I enjoy."
    mc "You know what I mean?"
    n "...?"
    mc "Hm?"
    mc "You don't?"
    show n_cg1_exp2 at cgfade
    n "Um..."
    n "That's not..."
    n "Well, I wouldn't really know."
    mc "...What do you mean?"
    mc "Don't you share your manga with your friends?"
    hide n_cg1_exp2
    show n_cg1_exp3 at cgfade
    n "Could you not rub it in?"
    n "Jeez..."
    mc "Ah... Sorry..."
    n "Hmph."
    n "Like I could ever get my friends to read this..."
    n "They just think manga is for kids."
    n "I can't even bring it up without them being all like..."
    n "'Eh? You still haven't grown out of that yet?'"
    n "Makes me want to punch them in the face..."
    mc "Urgh, I know those kinds of people..."
    mc "Honestly, it takes a lot of effort to find friends who don't judge, much less friends who are also into it..."
    mc "I'm already kind of a loser, so I guess I gravitated toward the other losers over time."
    mc "But it's probably harder for someone like you..."
    hide n_cg1_exp3
    n "Hm."
    n "Yeah, that's pretty accurate."
    "{i}...Wait, which part??{/i}"
    $ style.say_dialogue = style.normal
    n "I mean, I feel like I can't even keep it in my own room..."

    $ style.say_dialogue = style.edited
    n "My dad would beat the shit out of me if he found this."
    $ style.say_dialogue = style.normal
    $ _history_list[-1].what = "I don't even know what my dad would do if he found this."
    n "At least it's safe here in the clubroom."
    show n_cg1_exp3 at cgfade
    n "'Cept Monika's kind of a jerk about it..."
    n "Ugh! I just can't win, can I?"
    mc "Well, it paid off in the end, didn't it?"
    mc "I mean, here I am, reading it."
    n "Well, it's not like that solves any of my problems."
    mc "Maybe..."
    mc "But at least you're enjoying yourself, right?"
    hide n_cg1_exp3
    show n_cg1_exp2 at cgfade
    n "--"
    n "..."
    n "...So?"
    mc "Ahaha."
    hide n_cg1_exp2
    show n_cg1_exp3 at cgfade
    n "Jeez, that's enough!"
    n "Are you gonna keep reading, or what?"
    mc "Yeah, yeah..."
    "I flip the page."
    show black with dissolve_cg
    "..."
    "..."
    "....."
    "......."
    "........."
    "Time passes."
    hide n_cg1_exp3
    show n_cg1_exp4 behind black at cgfade
    "Natsuki is strangely quiet now."
    "I glance over at her."
    hide black with dissolve_cg
    "It looks like she's started to fall asleep."
    mc "Hey, Natsuki..."
    hide n_cg1_exp4
    show n_cg1_exp5 at cgfade
    n "Y-Yeah...?"
    "Suddenly, Natsuki collapses straight into me."
    play sound fall
    $ style.say_dialogue = style.normal
    mc "H-Hey--"
    show n_cg1_exp5
    hide n_cg1_exp5

    show n_cg1b
    hide n_cg1_base

    $ currentpos = get_pos()
    $ audio.t6g = "<from " + str(currentpos) + " loop 10.893>bgm/6g.ogg"
    play music t6g
    $ ntext = glitchtext(96)
    $ style.say_dialogue = style.edited
    n "{color=#000}[ntext]{/color}"
    $ ntext = glitchtext(96)
    n "{color=#000}[ntext]{/color}"
    $ style.say_dialogue = style.normal

    stop music
    window hide(None)
    window auto
    scene bg club_day
    show monika 1r zorder 2 at t11
    m "Oh jeez..."
    m 1d "Natsuki, are you okay?"
    show monika zorder 2 at t21
    show natsuki 12b zorder 3 at f22
    n "..."
    show natsuki zorder 2 at t22
    show monika zorder 3 at f21
    m 1a "Here..."
    show monika zorder 2 at t21
    "Monika reaches into her bag and pulls out some kind of protein bar."
    "She throws it in Natsuki's direction."
    "Natsuki's eyes suddenly light up again."
    "She snatches the bar from the floor and immediately tears off the wrapper."
    show natsuki zorder 3 at f22
    n 1s "I told you not to give mmph..."
    show natsuki zorder 2 at t22
    "She doesn't even finish her sentence before stuffing it into her mouth."
    show natsuki zorder 1 at thide
    hide natsuki
    show monika 3b zorder 2 at t11
    m "Don't worry, [player]."
    m "She's fine."
    m "It just happens every now and then."
    m 1a "That's why I always keep a snack in my bag for her."
    m 5a "Anyway...!"
    m "Why don't we all share poems now?"

    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
