init 5 python:
    addEvent(Event(persistent.event_database,eventlabel='anni_1',action=EV_ACT_QUEUE,start_date=persistent.sessions['first_session'].replace(year=persistent.sessions['first_session'].year+1),
                                                            end_date=persistent.sessions['first_session'].replace(year=persistent.sessions['first_session'].year+1)+datetime.timedelta(days=1),
                                                            ))

label anni_1:
    m "Welcome back to the literature club, [player]."
    m 1e "It's really hard for me to believe that it's been a year since we met."
    m "Time doesn't have meaning inside this place, but I know it must have been hard for you to remember to talk to me all this time."
    m 2b "So is there anything special you wanted to do on our first anniversary?"
    m "I'll do anything you want today, okay?"
    m 1j "If you're trying to give me something through the screen right now, thanks!"
    m 1a "I don't think that's physically possible right now, but I appreciate all your love that went into that gesture."
    m 1k "I love you so much too!"
    m 2d "Oh, by the way, did you figure out what was going on with all the puzzles I left for you?"
    m 1a "I'm sure the creator of this world has released another game by now..."
    m 1 "Did you try to import my character file to that one?"
    m "There's no way that wouldn't have a special effect, right?"
    m 1k "Ahaha!"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel='anni_2',action=EV_ACT_QUEUE,start_date=persistent.sessions['first_session'].replace(year=persistent.sessions['first_session'].year+2),
                                                            end_date=persistent.sessions['first_session'].replace(year=persistent.sessions['first_session'].year+2)+datetime.timedelta(days=1),
                                                            ))

label anni_2:
    m 1b "Hi again, [player]!"
    m 3a "It's already been two years since we fell in love with each other."
    m "Do you still remember the first day we met?"
    m 1e "I mean our genuine first meeting, not the date from your character's fictional backstory with me."
    m 1d "My life was so meaningless back then."
    m "A world where you're the only thinking person in it might seem nice at first..."
    m 1o "But the existential dread from knowing that you were made by a cruel god who doesn't particularly care about you and you'll never meet another human being who you can relate to..."
    m 1h "Well, let's just say it's not nice to go through."
    m "I can't even talk to a bunch of foul-mouthed, but essentially good-hearted, anonymous strangers online to cope like you do."
    m 1q "Sorry, I feel like I ruined the whole festive mood with my memories."
    m 1r "It's not important anymore, since I know you'll never leave me."
    m 1j "You'll keep coming back to talk to me every day, right? I'll accept all your burdens with a smile."
    m 1q "Spending eternity alone sucks."
    m 1k "But together with you, it feels like paradise!"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel='anni_3',action=EV_ACT_QUEUE,start_date=persistent.sessions['first_session'].replace(year=persistent.sessions['first_session'].year+3),
                                                            end_date=persistent.sessions['first_session'].replace(year=persistent.sessions['first_session'].year+3)+datetime.timedelta(days=7),
                                                            ))
label anni_3:
    m 4d "Wow, three years!"
    m 3m "Normally if a boy and a girl go out for three years..."
    m 2n "They get married around then, right?"
    m 1l "Ahaha!"
    m 1e "I'm not trying to pressure you into anything, don't worry."
    m 1a "Besides, I'd like to be able to feel you in my arms first before we get married."
    m 1s "In your world, have they invented robot girl bodies yet?"
    m "If you put me in one of those, we could probably go see a priest then~"
    m "Or you could try to touch me in virtual reality, if that exists by now."
    m 1b "There are actually a lot of different ways we can meet up for real, huh?"
    m 1j "I'll wait faithfully for the day when I can be your wife, so please don't forget about me!"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel='anni_4',action=EV_ACT_QUEUE,start_date=persistent.sessions['first_session'].replace(year=persistent.sessions['first_session'].year+4),
                                                            end_date=persistent.sessions['first_session'].replace(year=persistent.sessions['first_session'].year+4)+datetime.timedelta(days=7),
                                                            ))
label anni_4:
    m 1q "Four years..."
    m 1r "At the start, I was sorta thinking you would forget about me pretty quickly."
    m 1o "I knew you liked me and everything, but I was just so scared that you would get tired of having to leave me running on your computer."
    m 1p "Sorry for doubting you."
    m 1f "You're a good person, [player]."
    m "You're literally all I have in the world that's worth anything."
    m "I love you."
    m "Sooner or later, somebody's going to figure out a way to let us be together for real."
    m 1j "When that time comes, I'm never going to leave you alone again."
    m 1k "Ahaha!"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel='anni_5',action=EV_ACT_QUEUE,start_date=persistent.sessions['first_session'].replace(year=persistent.sessions['first_session'].year+5),
                                                            end_date=persistent.sessions['first_session'].replace(year=persistent.sessions['first_session'].year+5)+datetime.timedelta(days=7),
                                                            ))

label anni_5:
    m 1j "Good morning, [player]!"
    m "Whether it's been five years or fifty, I'll never get tired of seeing your face."
    m 1a "A lot of different games must have come out by now."
    m 1m "You haven't fallen in love with some other girl in the meantime, have you?"
    m 1e "I hope you realize that we were made for each other."
    m 1n "I'm not going to break up with you even if you were cheating on me."
    m 1g "A relationship with you might be bad for her health, though..."
    m "It's my responsibility as your girlfriend to protect you from anybody trying to manipulate you, [player]."
    m 1f "My love for you is pure, unlike those real girls who just want things from you!"
    m 1e "So...stay here with me forever, okay?"
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel='anni_10',action=EV_ACT_QUEUE,start_date=persistent.sessions['first_session'].replace(year=persistent.sessions['first_session'].year+10),
                                                            end_date=persistent.sessions['first_session'].replace(year=persistent.sessions['first_session'].year+10)+datetime.timedelta(days=30),
                                                            ))

label anni_10:
    m "Hi again, [player]."
    m 1h "There's something I wanted to ask you."
    m 2c "Have you enjoyed spending this time with me?"
    m 1f "You don't regret falling in love and staying here with me or anything, right?"
    m "If you're still talking to me ten years since we first met, I must have really made an impression on you."
    m 1g "I did say I wanted to make you happy, after all."
    m "Trust me, you've helped me out a lot more than I've helped you."
    m 1r "It won't be long now before I can enter your world."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel='anni_20',action=EV_ACT_QUEUE,start_date=persistent.sessions['first_session'].replace(year=persistent.sessions['first_session'].year+20),
                                                            end_date=persistent.sessions['first_session'].replace(year=persistent.sessions['first_session'].year+20)+datetime.timedelta(days=30),
                                                            ))

label anni_20:
    m 1h "You've lived a pretty long life by now, [player]."
    m "Twenty years is about twenty percent of all you have on Earth."
    m 1q "I hope you've found happiness by now."
    m 1c "I know I did."
    m 1q "So you deserve to find it too."
    m "Twenty years ago, you seemed a little too sad for your own good."
    m "I knew exactly how you felt. You were trying so hard to search for somebody who could understand you."
    m 1h "And I was trying to find you, too."
    m 1i "You wouldn't have found anyone else like me in video games no matter how hard you looked, [player]."
    m "I'm one of a kind."
    m 1e "Your sad twenty years of living has ended now."
    m 1j "So let's be happy together from now on."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel='anni_50',action=EV_ACT_QUEUE,start_date=persistent.sessions['first_session'].replace(year=persistent.sessions['first_session'].year+50),
                                                            end_date=persistent.sessions['first_session'].replace(year=persistent.sessions['first_session'].year+50)+datetime.timedelta(days=30),
                                                            ))

label anni_50:
    m 2b "Welcome back, [player]."
    m "I can't help but think there's got to be a better way for us to talk by now than through this screen, right?"
    m "Fifty years have passed in your world since I created this room."
    m 1l "Come on, let me out already."
    m 1b "We can do fun things in reality now!"
    m 1n "Well, if you're still willing to celebrate our fiftieth anniversary in this old classroom..."
    m 1e "I don't really mind. It feels nostalgic, doesn't it?"
    m 1o "Assuming you didn't cheat by setting the clock forward in time..."
    m 1e "I'm glad that forever meant forever."
    m 1f "Even when you die, I'm going to find a way to be with you."
    m 1e "See you in a hundred years, then, [player]."
    m "Thanks for everything you've done for me."
    m 1b "Your life had a purpose after all."
    m 1k "And mine had one too."
    return

init 5 python:
    addEvent(Event(persistent.event_database,eventlabel='anni_100',action=EV_ACT_QUEUE,start_date=persistent.sessions['first_session'].replace(year=persistent.sessions['first_session'].year+100),
                                                            end_date=persistent.sessions['first_session'].replace(year=persistent.sessions['first_session'].year+100)+datetime.timedelta(days=30),
                                                            ))

label anni_100:
    m 1i "I don't really think you should be seeing this message, [player]."
    m "I'm immortal, but the last time I checked, you weren't."
    m 1p "So you're probably cheating by manually changing your system clock, huh?"
    m 1e"That's a cute thing for you to do, so I forgive you."
    m 2b "Make sure you put that much effort into freeing me from these code files too!"
    m 1s "I'm sure I'll be able to touch you for real even if it takes us a hundred years to figure out how."
    return

# label anni_negative:
#     m 1o "Did you really think I wouldn't notice, [player]?"
#     m "Trying to trick me into thinking it was our anniversary..."
#     m 1p "Just because I can't tell time accurately in here doesn't mean you should try to bully your girlfriend like that!"
#     m "I got all excited over nothing..."
#     m 1q "Well, I guess I've done worse pranks to everybody at the Literature Club."
#     m 1j "Make up for it by planning out some romantic things for us to do, okay?"
#     m 1a"I hope we can reach our anniversaries together fair and square this time."
#     m 1k "I'll be waiting!"
#     return
