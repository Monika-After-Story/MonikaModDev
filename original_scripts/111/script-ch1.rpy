

label ch1_main:
    scene bg club_day
    with dissolve_scene_half
    play music t2
    show monika 5 zorder 2 at t11

    m "Hi again, [player]!"
    m "Glad to see you didn't run away on us. Hahaha!"
    mc "Nah, don't worry."
    mc "This might be a little strange for me, but I at least keep my word."
    show monika zorder 1 at thide
    hide monika
    "Well, I'm back at the Literature Club."
    "I was the last to come in, so everyone else is already hanging out."
    show yuri 1a zorder 2 at t32
    y "Thanks for keeping your promise, [player]."
    y "I hope this isn't too overwhelming of a commitment for you."
    y 1u "Making you dive headfirst into literature when you're not accustomed to it..."
    show natsuki 4e zorder 2 at t33
    n "Oh, come on! Like he deserves any slack."
    n "Sayori told me you didn't even want to join any clubs this year."
    n "And last year, too!"
    n 4c "I don't know if you plan to just come here and hang out, or what..."
    n "But if you don't take us seriously, then you won't see the end of it."
    show monika 2b at l41
    m "Natsuki, you certainly have a big mouth for someone who keeps her manga collection in the clubroom."
    n 4o "M-M-M...!!"
    show monika at lhide
    hide monika
    "Natsuki finds herself stuck between saying \"Monika\" and \"Manga\"."
    show natsuki at h33
    n 1v "Manga is literature!!"
    show natsuki zorder 1 at thide
    hide natsuki
    "Swiftly defeated, Natsuki plops back into her seat."
    show yuri zorder 2 at t22
    show sayori 2x zorder 3 at f21
    s "Don't worry, guys~"
    s "[player] always gives it his best as long as he's having fun."
    s "He helps me with busywork without me even asking."
    s "Like cooking, cleaning my room..."
    show sayori 2a zorder 2 at t21
    show yuri zorder 3 at f22
    y 2m "How dependable..."
    show yuri zorder 2 at t22
    mc "Sayori, that's because your room is so messy it's distracting."
    mc "And you almost set your house on fire once."
    show sayori at s21
    s 5 "Is that so... Ehehe..."
    show yuri zorder 3 at f22
    y 1s "You two are really good friends, aren't you?"
    y "I might be a little jealous..."
    show yuri zorder 2 at t22
    show sayori zorder 3 at f21
    s 1 "How come? You and [player] can become good friends too!"
    show sayori zorder 2 at t21
    show yuri zorder 3 at f22
    y 4b "U-Um..."
    show yuri zorder 2 at t22
    mc "S-Sayori--"
    show sayori zorder 3 at f21
    s "Hmm?"
    show sayori zorder 2 at t21
    mc "..."
    "As usual, Sayori seems oblivious to the weird situation she just put me into."
    show sayori zorder 3 at f21
    s 4x "Oh, oh! Yuri even brought you something today, you know~"
    show sayori zorder 2 at t21
    show yuri zorder 3 at f22
    y 3n "W-Wait! Sayori..."
    show yuri zorder 2 at t22
    mc "Eh? Me?"
    show yuri zorder 3 at f22
    y 3o "Um... Not really..."
    show yuri zorder 2 at t22
    show sayori zorder 3 at f21
    s 4r "Don't be shy~"
    show sayori zorder 2 at t21
    show yuri zorder 3 at f22
    y "It's really nothing..."
    show yuri zorder 2 at t22
    mc "What is it?"
    show yuri zorder 3 at f22
    y 4c "N-Never mind!"
    y "Sayori made it sound like a big deal when it's really not..."
    y "Uuuuh, what do I do..."
    show yuri zorder 2 at t22
    show sayori zorder 3 at f21
    s 1g "Eh? I'm sorry, Yuri, I wasn't thinking..."
    show sayori zorder 1 at thide
    hide sayori
    show yuri zorder 2 at t11
    "I guess that means it's up to me to rescue this situation..."
    mc "Hey, don't worry about it."
    mc "First of all, I wasn't expecting anything in the first place."
    mc "So any nice gesture from you is a pleasant surprise."
    mc "It'll make me happy no matter what."
    y 3v "I-Is that so..."
    mc "Yeah. I won't make it a big deal if you don't want it to be."
    y "Alright..."
    y 1a "Well, here."
    "Yuri reaches into her bag and pulls out a book."
    y "I didn't want you to feel left out..."
    y "So I picked out a book that I thought you might enjoy."
    y "It's a short read, so it should keep your attention, even if you don't usually read."
    y "And we could, you know..."
    show yuri at sink
    y 4b "Discuss it...if you wanted..."
    "Th-This is..."
    "How is this girl accidentally being so cute?"
    "She even picked out a book she thinks I'll like, despite me not reading much..."
    mc "Yuri, thank you! I'll definitely read this!"
    "I enthusiastically take the book."
    show yuri 2m zorder 2 at t11
    y "Phew..."
    y 2a "Well, you can read it at your own pace."
    y "I look forward to hearing what you think."
    show yuri zorder 1 at thide
    hide yuri


    "Now that everyone's settled in, I expected Monika to kick off some scheduled activities for the club."
    "But that doesn't seem to be the case."
    "Sayori and Monika are having a cheery conversation in the corner."
    "Yuri's face is already buried in a book."
    "I can't help but notice her intense expression, like she was waiting for this chance."
    "Meanwhile, Natsuki is rummaging around in the closet."


    $ nextscene = poemwinner[0] + "_exclusive_" + str(eval(poemwinner[0][0] + "_appeal"))
    call expression nextscene


    show monika 1 zorder 2 at t21
    hide sayori
    hide natsuki
    hide yuri
    m "By the way, did you remember to write a poem last night?"
    mc "Y-Yeah..."
    "My relaxation ends."
    "I can't believe I agreed to do something so embarrassing."
    "I couldn't really find much inspiration, since I've never really done this before."
    m "Well, now that everyone's ready, why don't you find someone to share with?"
    show sayori 4q zorder 2 at t22
    s "I can't wait~!"
    show sayori zorder 1 at thide
    show monika zorder 1 at thide
    hide sayori
    hide monika
    "Sayori and Monika enthusiastically pull out their poems."
    "Sayori's is on a wrinkled sheet of loose leaf torn from a spiral notebook."
    "On the other hand, Monika wrote hers in a composition notebook."
    "I can already see Monika's pristine handwriting from where I sit."
    "Natsuki and Yuri reluctantly comply as well, reaching into their bags."
    "I do the same, myself."

    return


label ch1_end:
    stop music fadeout 1.0
    scene bg club_day
    with wipeleft_scene
    play music t3
    mc "Phew..."
    "I guess that's everyone."
    "I glance around the room."
    "That was a little more stressful than I anticipated."
    "It's as if everyone is judging me for my mediocre writing abilities..."
    "Even if they're just being nice, there's no way my poems can stand up to theirs."
    "This is a literature club, after all."
    "I sigh."
    "I guess that's what I ended up getting myself into."
    "Across the room, Sayori and Monika are happily chatting."
    "My eyes land on Yuri and Natsuki."
    show yuri 2g zorder 2 at t21
    show natsuki 1g zorder 2 at t22
    "They gingerly exchange sheets of paper, sharing their respective poems."
    show yuri 2i at t21
    "As they read in tandem, I watch each of their expressions change."
    "Natsuki's eyebrows furrow in frustration."
    "Meanwhile, Yuri smiles sadly."
    show natsuki zorder 3 at f22
    n 1q "{i}(What's with this language...?){/i}"
    show natsuki zorder 2 at t22
    show yuri zorder 3 at f21
    y 2f "Eh?"
    y "Um...did you say something?"
    show yuri zorder 2 at t21
    show natsuki zorder 3 at f22
    n 2c "Oh, it's nothing."
    "Natsuki dismissively returns the poem to the desk with one hand."
    n "I guess you could say it's fancy."
    show natsuki zorder 2 at t22
    show yuri zorder 3 at f21
    y 2i "Ah-- Thanks..."
    y "Yours is...cute..."
    show yuri zorder 2 at t21
    show natsuki zorder 3 at f22
    n 2h "Cute?"
    n 1h "Did you completely miss the symbolism or something?"
    n "It's clearly about the feeling of giving up."
    n "How can that be cute?"
    show natsuki zorder 2 at t22
    show yuri zorder 3 at f21
    y 3f "I-I know that!"
    y "I just meant..."
    y 3h "The language, I guess..."
    y "I was trying to say something nice..."
    show yuri zorder 2 at t21
    show natsuki zorder 3 at f22
    n "Eh?"
    n 4w "You mean you have to try that hard to come up with something nice to say?"
    n "Thanks, but it really didn't come out nice at all!"
    show natsuki zorder 2 at t22
    show yuri zorder 3 at f21
    y 1i "Um..."
    y "Well, I do have a couple suggestions..."
    show yuri zorder 2 at t21
    show natsuki zorder 3 at f22
    n 5x "Hmph."
    n "If I was looking for suggestions, I would have asked someone who actually liked it."
    n "Which people {i}did{/i}, by the way."
    n 5e "Sayori liked it."
    n "And [player] did, too!"
    n "So based on that, I'll gladly give you some suggestions of my own."
    n "First of all--"
    show natsuki zorder 2 at t22
    show yuri zorder 3 at f21
    y 2l "Excuse me..."
    y "I appreciate the offer, but I've spent a long time establishing my writing style."
    y 2h "I don't expect it to change anytime soon, unless of course I come across something particularly inspiring."
    y "Which I haven't yet."
    show yuri zorder 2 at t21
    show natsuki zorder 3 at f22
    n 1o "Nn...!"
    show natsuki zorder 2 at t22
    show yuri zorder 3 at f21
    y 1k "And [player] liked my poem too, you know."
    y "He even told me he was impressed by it."
    stop music fadeout 1.0
    "Natsuki suddenly stands up."
    show yuri zorder 2 at t21
    show natsuki zorder 3 at f22
    n 4y "Oh?"
    n "I didn't realize you were so invested in trying to impress our new member, Yuri."
    play music t7
    show natsuki zorder 2 at t22
    show yuri zorder 3 at f21
    y 1n "E-Eh?!"
    y "That's not what I...!"
    y 1o "Uu..."
    y "You...You're just..."
    "Yuri stands up as well."
    y 2r "Maybe you're just jealous that [player] appreciates my advice more than he appreciated yours!"
    show yuri zorder 2 at t21
    show natsuki zorder 3 at f22
    n 1e "Huh! And how do you know he didn't appreciate {i}my{/i} advice more?"
    n "Are you that full of yourself?"
    show natsuki zorder 2 at t22
    show yuri zorder 3 at f21
    y 3h "I...!"
    y "No..."
    y "If I was full of myself..."
    y 1r "...I would deliberately go out of my way to make everything I do overly cutesy!"
    show yuri zorder 2 at t21
    show natsuki zorder 3 at f22
    n 1o "Uuuuuu...!"
    show sayori 2l behind yuri, natsuki at l41
    show yuri zorder 2 at t32
    show natsuki zorder 2 at t33
    s "U-Um!!"
    s "Is everyone okay...?"
    show sayori 2 at lhide
    hide sayori
    show natsuki zorder 3 at f33
    n 1f "Well, you know what?!"
    n "I wasn't the one whose boobs magically grew a size bigger as soon as [player] started showing up!!"
    show yuri 3p at h32
    show natsuki zorder 2 at t33
    y "N-Natsuki!!"
    show monika 3l behind yuri, natsuki at l41
    m "Um, Natsuki, that's a little--"
    show monika at h41
    show yuri 3p zorder 3 at f32
    show natsuki 1e zorder 3 at f33
    ny "This doesn't involve you!"
    show monika at lhide
    hide monika
    show yuri zorder 2 at t32
    show natsuki zorder 2 at t33
    show sayori 4p behind yuri, natsuki at l41
    s "I-I don't like fighting, guys...!"
    show sayori at lhide
    hide sayori
    show yuri zorder 2 at t21
    show natsuki 1g zorder 2 at t22
    "Suddenly, both girls turn towards me, as if they just noticed I was standing there."
    show yuri zorder 3 at f21
    y 2n "[player]...!"
    y "She-- She's just trying to make me look bad...!"
    show yuri zorder 2 at t21
    show natsuki zorder 3 at f22
    n 4w "That's not true!"
    n "She started it!"
    n 4e "If she could get over herself and learn to appreciate that {i}simple{/i} writing is more effective..."
    n "Then this wouldn't have happened in the first place!"
    n "What's the point in making your poems all convoluted for no reason?"
    n "The meaning should jump out at the reader, not force them to have to figure it out."
    n 1f "Help me explain that to her, [player]!"
    show natsuki zorder 2 at t22
    show yuri zorder 3 at f21
    y 3o "W-Wait!"
    y "There's a reason we have so many deep and expressive words in our language!"
    y 3w "It's the only way to convey complex feelings and meaning the most effectively."
    y "Avoiding them is not only unnecessarily limiting yourself...it's also a waste!"
    y 1t "You understand that, right, [player]?"
    show yuri zorder 2 at t21
    mc "Um...!"
    show yuri 1t zorder 3 at f21
    show natsuki 1e zorder 3 at f22
    ny "Well??"
    mc "..."
    show yuri zorder 2 at t21
    show natsuki 1g zorder 2 at t22
    "How did I get dragged into this in the first place?!"
    "It's not like I know anything about writing..."
    "But whomever I agree with, they'll probably think more highly of me!"
    menu:
        "So, of course that's going to be...!"
        "Natsuki.":
            call ch1_end_natsuki
        "Yuri.":
            call ch1_end_yuri
        "Help me, Sayori!!":
            call ch1_end_sayori

    scene bg club_day
    show monika 4b zorder 2 at t11
    with wipeleft_scene
    m "Okay, everyone!"
    m "It's just about time for us to leave."
    m "How did you all feel about sharing poems?"
    show monika 4a
    show sayori 4x zorder 2 at t31
    s "It was a lot of fun!"
    show sayori behind yuri at thide
    show yuri 1i zorder 2 at t31
    hide sayori
    y "Well, I'd say it was worth it."
    show yuri behind natsuki at thide
    show natsuki 4q zorder 2 at t31
    hide yuri
    n "It was alright. Well, mostly."
    show natsuki zorder 1 at thide
    hide natsuki
    m 1a "[player], how about you?"
    mc "...Yeah, I'd say the same."
    mc "It was a neat thing to talk about with everyone."
    m 1j "Awesome!"
    m 1a "In that case, we'll do the same thing tomorrow."
    m "And maybe you learned something from your friends, too."
    m 3b "So your poems will turn out even better!"
    mc "..."
    show monika zorder 1 at thide
    hide monika
    "I think to myself."
    "I did learn a little more about the kinds of poems everyone likes."
    "With any luck, that means I can at least do a better job impressing those I want to impress."
    "I nod to myself with newfound determination."
    show sayori 1x zorder 2 at t11
    s "[player]!"
    s "Ready to walk home?"
    mc "Sure, let's go."
    s 4q "Ehehe~"
    "Sayori beams at me."
    "It truly has been a while since Sayori and I have spent this much time together."
    "I can't really say I'm not enjoying it, either."
    scene bg residential_day
    show sayori 1a zorder 2 at t11
    with wipeleft_scene
    mc "Sayori..."
    mc "About what happened earlier..."
    s 1b "Eh? What do you mean?"
    mc "You know, between Yuri and Natsuki."
    mc "Does that kind of thing happen often?"
    s 4j "No, no, no!"
    s "That's really the first time I've seen them fight like that..."
    s "I promise they're both wonderful people."
    show sayori at s11
    s 1g "You don't... You don't hate them, do you??"
    mc "No, I don't hate them!"
    mc "I just wanted your opinion, that's all."
    mc "I can see why they'd make good friends with you."
    show sayori zorder 2 at t11
    s 1d "Phew..."
    s "You know, [player]..."
    s "It's nice that I get to spend time with you in the club."
    s "But I think seeing you get along with everyone is what makes me the happiest."
    s 1x "And I think everyone really likes you, too!"
    mc "That's--!"
    s 4q "Ehehe~"
    s "Every day is going to be so much fun~"
    mc "Sigh..."
    "It looks like Sayori still hasn't caught onto the kind of situation I'm in."
    "Sure, being friends with everyone is nice, but..."
    "...Does it really need to stop there?"
    mc "We'll just have to see what the future holds, Sayori."
    "I pat Sayori on the shoulder."
    "I said that more to myself than to her, but it's easy to use Sayori as an internal monologue sometimes."
    show sayori at h11
    s 1x "Okay~!"
    "Yeah..."
    "Let's do this!"
    return

label ch1_end_natsuki:
    $ ch1_choice = "natsuki"
    stop music fadeout 1.0
    mc "Um..."
    mc "Yuri!"
    mc "You're really talented."
    show yuri 4a at s21
    y "Eh? W-Well..."
    play music t8
    mc "But Natsuki has a point!"
    mc "I think that..."
    show yuri zorder 2 at t21
    "I wrack my brain in an attempt to back myself up."
    mc "I think that conveying feelings with few words..."
    mc "Can be just as impressive as well!"
    mc "It lets the reader's imagination take over."
    mc "And Natsuki's poem did a really good job at that!"
    show natsuki zorder 3 at f22
    n 5y "...Yeah!!"
    n "It did, didn't it?!"
    n "Ahah!"
    n "Shows how much {i}you{/i} know!"
    show natsuki zorder 2 at t22
    show yuri zorder 3 at f21
    y 4b "T-That's not..."
    show yuri zorder 2 at t21
    mc "Natsuki..."
    mc "I think that's enough."
    show natsuki zorder 3 at f22
    n 1m "Huh?"
    n "Me?"
    n "But she was so mean to me...!"
    "Natsuki's voice whines."
    show natsuki zorder 2 at t22
    mc "Look..."
    mc "What we talked about yesterday was right."
    mc "Writing is a really personal thing."
    mc "And sharing it can definitely be hard."
    mc "It looks like we learned that today."
    mc "Even small criticism can lead to something pretty heated."
    "I glance over my shoulder."
    "Sayori is nodding vigorously."
    mc "Yeah, so..."
    mc "You don't need to feel threatened."
    mc "You're a great writer, Natsuki."
    show natsuki zorder 3 at f22
    n 1h "Ah--"
    "Natsuki's voice gets caught in surprise."
    n 1q "...Thanks for noticing."
    "She finally mutters that, barely audible."
    show natsuki zorder 2 at t22
    mc "Yuri..."
    show yuri zorder 3 at f21
    y 4a "...?"
    "Yuri looks at me dejectedly."
    "With a face like that, I can't help but feel bad for her as well."
    show yuri zorder 2 at t21
    mc "I'm sure that Natsuki didn't mean everything she said."
    mc "So you don't need to feel threatened, either."
    show yuri zorder 3 at f21
    y 2v "Well..."
    y "If you say so..."
    show yuri zorder 2 at t21
    show natsuki zorder 3 at f22
    n 1g "Hey...!"
    n "It's not like you need to apologize {i}for{/i} me, [player]."
    n 1w "Sheesh."
    "Natsuki takes a breath."
    n 1q "I..."
    n "The thing about..."
    n "Uu..."
    "Natsuki glances around the room."
    show natsuki zorder 3 at hf22
    n 1x "{i}Would everyone stop staring at me??{/i}"
    "Unsurprisingly, Natsuki has a harder time with it than she boasted."
    "Sayori and Monika look away."
    show natsuki zorder 3 at f22
    n 1i "Hmph."
    n "Anyway...!"
    n 1q "The thing about your boobs. I didn't mean it, okay?"
    n "That's all."
    "Natsuki looks away, avoiding eye contact with anyone."
    show natsuki zorder 2 at t22
    show sayori 4x behind yuri at l41
    s "Yeah! You're naturally beautiful, Yuri!!"
    mc "Sayori?!"
    show yuri 4c zorder 3 at f21
    y "..."
    y "I-I'll go make some tea..."
    show yuri at lhide
    hide yuri
    show sayori zorder 3 at f41
    s 4h "Ehh?"
    s "I was just trying to help!"
    show sayori zorder 2 at t41
    mc "I'm sure she appreciated it, Sayori."
    "I pat Sayori on the shoulder."
    show sayori zorder 1 at thide
    show natsuki zorder 1 at thide
    show monika 4m zorder 2 at t11
    hide sayori
    hide natsuki
    m "Well, now that we're past that..."
    m 4b "Everyone's read each other's poems, right?"
    m "I hope that it was worthwhile for everyone!"
    m 5 "Especially you, [player]!"
    m "And to be honest..."
    m "It's a nice change of pace from the lazing around we got a little too used to."
    m "Ahahaha!"
    mc "Ah, so my joining the club was responsible for ruining the atmosphere..."
    m 1d "No, not at all, not at all!"
    m "There's still time before we go home."
    m 1a "So we'll all relax for a bit."
    m "Of course, besides chatting, we do literature-related things in the clubroom..."
    m "So maybe you can take the chance to pick up a book, or do some writing."
    m 1b "After all, that's what the club is for!"
    show sayori 2j zorder 3 at f31
    s "I disagree, Monika!"
    show sayori zorder 2 at t31
    show monika zorder 3 at f32
    m 1d "Eh? About what?"
    show monika zorder 2 at t32
    show sayori zorder 3 at f31
    s 2i "That's not the most important thing about the literature club!"
    s "The most important thing..."
    show sayori 4r zorder 3 at hf31
    s "Is having fun!"
    show sayori zorder 2 at t31
    show monika zorder 3 at f32
    m 2l "Ahaha, of course..."
    m 2a "Well, I guess that's why you're the Vice President, Sayori."
    show monika zorder 2 at t32
    show sayori zorder 3 at f31
    s 4q "Ehehe..."
    hide sayori
    hide monika
    with wipeleft
    "In the end, though, Monika's right."
    "Being in the Literature Club probably means I can't spend all my time doing nothing."
    "But in the end..."
    "...I guess it's been worth it so far."
    return

label ch1_end_yuri:
    $ ch1_choice = "yuri"
    stop music fadeout 1.0
    mc "Natsuki."
    mc "You're right that I liked your poem."
    show natsuki zorder 3 at f22
    n 1e "See??"
    show natsuki 1g zorder 2 at t22
    play music t8
    mc "Wait!"
    mc "That's not an excuse for you to be so mean!"
    mc "You shouldn't pick a fight just because someone's opinion is different."
    show natsuki zorder 3 at f22
    n 1m "That's not what happened at all!"
    n "Yuri wouldn't even take my poem seriously!"
    show natsuki zorder 2 at t22
    mc "Mm..."
    mc "I understand."
    mc "Yuri."
    show yuri zorder 3 at f21
    y 2t "Eh?"
    show yuri zorder 2 at t21
    mc "You're a seriously talented writer."
    mc "It's no secret that I was impressed."
    show yuri zorder 3 at f21
    y 2u "W-Well, that's..."
    show yuri zorder 2 at t21
    mc "But here's the thing."
    mc "No matter how simple or refined someone's writing style is..."
    mc "They're still putting feelings into it, and it becomes something really personal."
    mc "That's why Natsuki felt threatened when you said her poem was cute."
    show yuri zorder 3 at f21
    y 2v "I...see..."
    y "I didn't notice that I..."
    show yuri zorder 2 at t21
    y 2w "I-I'm sorry..."
    show yuri at s21
    y "Uuu..."
    show natsuki zorder 2 at t11
    show yuri zorder 1 at thide
    hide yuri
    mc "But Natsuki, you took it way too far!"
    mc "Yuri means well, and if you just told her how you felt..."
    mc "Then this wouldn't have happened in the first place."
    n 1e "Are you kidding?"
    n "That's exactly what I did!"
    n "It was {i}her{/i} that--"
    show natsuki zorder 2 at t22
    show monika 2i zorder 3 at f21
    m "Natsuki, I think that's enough."
    m "You both said some things that you didn't mean."
    m "Yuri apologized. Don't you think you should, too?"
    show monika zorder 2 at t21
    show natsuki zorder 3 at f22
    n 1x "Nnn...!"
    show natsuki zorder 2 at t22
    "Natsuki clenches her fists."
    "In the end, nobody has taken her side."
    "She's trapped, at this point being defiant only because she can't handle the pressure."
    "I end up even feeling bad for her."
    show monika zorder 2 at t32
    show natsuki zorder 2 at t33
    show sayori 2h at l41
    s "U-Um!"
    s "Sometimes when I'm hurt..."
    s "It helps to take a walk and clear my head!"
    show sayori zorder 2 at t41
    mc "Sayori, she doesn't need to--"
    show natsuki zorder 3 at f33
    n 2q "You know what?"
    n "I'm going to do that."
    n 2w "It'll spare me from having to look at all your faces right now."
    show natsuki zorder 1 at thide
    hide natsuki
    "Without warning, Natsuki snatches her own poem up from the desk and storms out."
    "On her way out, she crumples up the poem with her hands and throws it in the trash."
    show sayori zorder 3 at f41
    s 1k "Natsuki..."
    show sayori zorder 2 at t41
    show monika zorder 3 at f32
    m 1r "She really didn't need to do that..."
    show sayori zorder 1 at thide
    show monika zorder 1 at thide
    hide sayori
    hide monika
    "I look across the room."
    "Yuri has her chin buried in her hands while she stares down at her desk."
    "I gingerly approach her and sit in an adjacent chair."
    show yuri 4b zorder 2 at t11
    y "Sigh..."
    mc "Everything alright?"
    y "I'm so embarrassed..."
    y "I can't believe I acted like that."
    y "You probably hate me now..."
    mc "No--Yuri!"
    mc "How could anyone not have gotten frustrated after being treated like that?"
    mc "You handled it as well as anyone could."
    mc "I don't think any less of you."
    y 2v "Well..."
    y "...Alright, I believe you."
    y 2s "Thanks, [player]. You're too kind."
    y "I'm thankful to have you a part of this club now."
    mc "Er-- It's nothing."
    y 2v "One more thing..."
    y "Um, that one thing that Natsuki said..."
    y 4c "About...you know..."
    y "I would never do anything...so shameful..."
    y "So..."
    mc "...Eh?"
    mc "What thing did Natsuki say?"
    y 3n "--!"
    y "U-Um!"
    y 3q "Well, never mind that..."
    y "I-I'm going to go make some tea..."
    mc "Ah, good idea."
    mc "Make enough for more than one person, okay?"
    y "Y-Yeah."
    return

label ch1_end_sayori:
    $ ch1_choice = "sayori"
    mc "N-Natsuki..."
    show natsuki 5f
    "Natsuki glares at me, drying up any words I had in my mouth."
    "So instead, I turn to Yuri."
    mc "Yuri..."
    y 4a "..."
    "But Yuri's expression is so defenseless that I can't bring myself to say anything to her."
    stop music fadeout 1.0
    mc "..."
    mc "...Sayori!"
    show sayori 4m behind yuri at l31
    show yuri zorder 2 at t32
    show natsuki zorder 2 at t33
    s "Eh?!"
    mc "...Yeah!"
    mc "Everyone's fighting is making Sayori uncomfortable."
    mc "How can the two of you keep fighting when you know you're making your friend feel like this?"
    show sayori zorder 3 at f31
    s 4d "[player]..."
    show sayori zorder 2 at t31
    show natsuki 4w zorder 3 at f33
    n "Well... That's her problem! This isn't about her."
    show natsuki zorder 2 at t33
    show yuri 2g zorder 3 at f32
    y "I-I agree..."
    y "It's unfair for others to interject their own feelings into our conflict."
    show yuri zorder 2 at t32
    show natsuki zorder 3 at f33
    n 4c "Yeah, unless Sayori wants to tell Yuri what a stuck-up jerk she's being."
    show natsuki zorder 2 at t33
    show yuri 3r zorder 3 at f32
    play music t7
    y "She would never...!"
    y "It's your immaturity that's made her upset in the first place!"
    show yuri zorder 2 at t32
    show natsuki 1e zorder 3 at f33
    n "{i}Excuse{/i} me?"
    n "Are you listening to yourself?"
    n 1x "This is exactly why..."
    n 1w "Exactly why nobody likes--"
    show natsuki zorder 2 at t33
    show sayori 4p at h31
    stop music
    s "{i}Stop!!{/i}"
    show yuri 3f zorder 3 at f32
    show natsuki 1o zorder 3 at f33
    ny "--"
    show yuri zorder 2 at t32
    show natsuki zorder 2 at t33
    show sayori zorder 3 at f31
    play music t8
    s 1h "Natsuki! Yuri!"
    s "You guys are my friends!"
    s 1v "I-I just want everyone to get along and be happy!"
    s "My friends are wonderful people..."
    s "And I love them because of their differences!"
    s 1g "Natsuki's poems..."
    s "They're amazing because they give you so many feelings with just a few words!"
    s "And Yuri's poems are amazing because they paint beautiful pictures in your head!"
    s 4k "Everyone's so talented..."
    s "...So why are we fighting...?"
    show sayori zorder 2 at t31
    show natsuki zorder 3 at f33
    n 1r "Be-Because..."
    show natsuki zorder 2 at t33
    show yuri 3v zorder 3 at f32
    y "Well..."
    show yuri zorder 2 at t32
    show sayori zorder 3 at f31
    s 1j "Also!"
    s "Natsuki's cute and there's nothing wrong with that!"
    s 1i "And Yuri's boobs are the same as they always were!"
    show sayori at hf31
    s 1j "Big and beautiful!!"
    show sayori 1i zorder 2 at t31
    show natsuki zorder 3 at f33
    n 1o "..."
    show natsuki zorder 2 at t33
    show yuri zorder 3 at f32
    y 3n "..."
    show yuri zorder 2 at t32
    mc "Sayori..."
    "Sayori stands triumphantly."
    "Monika stands behind her with a bewildered expression."
    show yuri at s32
    y 3q "I'll...make some tea..."
    show yuri behind sayori at lhide
    hide yuri
    "Yuri rushes off."
    show natsuki zorder 1 at thide
    hide natsuki
    "Natsuki sits down with a blank expression on her face, staring at nothing."
    show sayori zorder 1 at thide
    show monika 1i zorder 2 at t11
    hide sayori
    mc "So, this is why Sayori is Vice President..."
    "I whisper to Monika."
    "She nods in return."
    m 1d "To be honest..."
    m "I might come off as a good leader, and I can organize things..."
    m 3e "But I'm not very good with people..."
    m "I couldn't even bring myself to interject."
    m 1m "As President, that's kind of embarrassing of me."
    m 1l "Ahaha..."
    mc "Nah..."
    mc "It's not like I can blame you."
    mc "I wasn't able to say anything, either."
    m "Well..."
    m 2a "I guess that just means Sayori is amazing in her own ways, isn't she?"
    mc "You could say that."
    mc "She might be an airhead, but sometimes it's weirdly suspicious that she knows exactly what she's doing."
    m 5 "I see~"
    m "Take good care of her, okay?"
    m "I would hate to see her get herself hurt."
    mc "That makes two of us..."
    mc "You can count on me."
    "Monika smiles sweetly at me, causing my stomach to knot."
    "Such a genuine person really does make a good President, regardless of what she says."
    "If only I could get the chance to talk to her a little more..."
    return
# Decompiled by unrpyc: https://github.com/CensoredUsername/unrpyc
