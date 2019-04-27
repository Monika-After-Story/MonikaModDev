init 4 python in mas_gtod:
    # to simplify unlocking, lets use a special function to unlock tips
    import datetime
    import store.evhand as evhand

    M_GTOD = "monika_gtod_tip{:0>3d}"

    def has_day_past_tip(tip_num):
        """
        Checks if the tip with the given number has already been seen and
        a day has past since it was unlocked.
        NOTE: by day, we mean date has changd, not 24 hours

        IN:
            tip_num - number of the tip to check

        RETURNS:
            true if the tip has been seen and a day has past since it was
            unlocked, False otherwise
        """

        tip_ev = evhand.event_database.get(
            M_GTOD.format(tip_num),
            None
        )

        if tip_ev is None:
            return False

        # otherwise, unlocked date is our key
        if tip_ev.unlock_date is None or tip_ev.shown_count == 0:
            return False

        # now check the actual day
        return (
            datetime.date.today() - tip_ev.unlock_date.date() 
            >= datetime.timedelta(days=1)
        )

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip000",
            category=["grammar tips"],
            prompt="Can you teach me about grammar?",
            pool=True
        )
    )

label monika_gtod_tip000:
    m "Of course I'll teach you about grammar, [player]!"
    m "It makes me really happy your want to better your writing skills."
    m "I've actually been reviewing some books on writing, and I think there are some interesting things we can talk about!"
    m "I'll admit...{w=0.5}it kind of sounds strange to discuss something as specific as grammar."
    m "I know it's not the most exciting thing that comes up in people's minds."
    m "...Maybe images of strict teachers, or stuck-up editors..."
    m "But I think that there's a certain beauty in mastering how you write, as well as eloquently delivering your message."
    m "So...starting today, I'll be sharing Monika's Grammar Tip of the Day!"
    m "Let's improve our writing together, my love~"
    m "We'll start with clauses, the basic building blocks of sentences!"

    $ hideEventLabel("monika_gtod_tip000", depool=True)

    # enable tip 1
    $ import datetime
    $ tip_ev = mas_getEV("monika_gtod_tip001")
    $ tip_ev.pool = True
    $ tip_ev.unlocked = True
    $ tip_ev.unlock_date = datetime.datetime.now()
    $ tip_ev.shown_count = 1

    jump monika_gtod_tip001

##############################################################################
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip001",
            category=["grammar tips"],
            prompt="Clauses"
        )
    )

label monika_gtod_tip001:
    m "You probably know this already, but a clause is a group of words that has a subject and an action, or predicate."
    m "For the most part, clauses can be sorted into either independent or dependent clauses."
    m "Independent clauses can stand on their own as sentences, such as in the sentence '{b}I wrote that.{/b}'"
    m "Dependent clauses, on the other hand, can't stand on their own and usually appear as parts of longer sentences."
    m "An an example of one could be '{b}who saved her.{/b}'"
    m "There is a subject, '{b}who{/b},' and an action, '{b}saved her{/b},' but of course, the clause can't be a sentence by itself."
    m "...I think you know how to finish that sentence, [player]~"
    m "That's all for today's lesson, thanks for listening!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip002",
            category=["grammar tips"],
            prompt="Comma Splices/Run-ons",
            conditional="store.mas_gtod.has_day_past_tip(1)",
            action=EV_ACT_POOL
        )
    )

label monika_gtod_tip002:
    m "Do you remember when we talked about clauses, [player]?"
    m "There's actually a very common mistake that many writers fall into when joining them."
    m "When you join two independent clauses together, this is called a comma splice."
    m "Here's an example: '{b}I visited the park, I looked at the sky, I saw many stars.{/b}"
    m "This doesn't seem like a problem at first, but you could imagine adding more and more clauses to that sentence. The result would be a mess!"
    m "'{b}I visited the park, I looked at the sky, I saw many stars, I saw some constellations, one of them looked like a crab...{/b}' It could go on and on."
    m "The best way to avoid this mistake is to separate independent clauses with periods, conjunctions, or semicolons."
    m "A conjunction is basically a word that you use to connect two clauses or phrases together."
    m "They're a pretty interesting topic on their own, so we can go over them in a future tip!"
    m "Anyways, taking that example we had earlier, let's add a conjunction and a period to make our sentence flow better: '{b}I visited the park, and I looked at the sky. I saw many stars.{/b}'"
    m "Much better, don't you think?"
    m "That's all I have for today, [player]."
    m "Thanks for listening!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip003",
            category=["grammar tips"],
            prompt="Conjunctions",
            conditional="store.mas_gtod.has_day_past_tip(2)",
            action=EV_ACT_POOL
        )
    )

label monika_gtod_tip003:
    m "Okay, [player]! I think it's time we talk about...{w=0.5}conjunctions!"
    m "Like I said before, conjunctions are words or phrases that bring two idea together."
    m "When you think about it, that's a big category! There are so many words we use to accomplish that."
    m "Just imagine speaking without conjunctions..."
    m "It would be dull. You would sound choppy. These ideas all relate. We should connect them."
    m "Now compare this to using conjunctions: '{b}It would be dull, and you would sound choppy. Since these ideas all relate, we should connect them.{/b}"
    m "Not only do conjunctions combine ideas, but they also make your writing sound more fluid and more similar to how we actually talk."
    m "Anyways, there are three types of conjunctions: coordinating, correlative, and subordinating."
    m "Their names may sound a little daunting, but I promise they'll make more sense as we go through them. I'll give you examples as we go along, too!"
    m "Coordinating clauses bridge two words, phrases, or clauses of the same 'rank' together. This just means that they have to be of the same type...words with words, or clauses with clauses."
    m "Some common examples are '{b}and, or, but, so, yet{/b}...'"
    m "You can connect independent clauses, {i}and{/i} you can avoid comma splices!"
    m "Correlative conjuctions are pairs of conjunctions used to connect ideas."
    m "A few common pairs are: '{b}either{/b}' and '{b}or{/b},' '{b}both{/b}' and '{b}and{/b},' and '{b}whether{/b}' and '{b}or{/b}.'"
    m "{i}Whether{/i} you realize it {i}or{/i} not, we use them all the time...like in this sentence!"
    m "Lastly, subordinating conjunctions bring together independent and dependent clauses. As you can imagine, there are many ways we can do that!"
    m "Examples include: '{b}although{/b},' '{b}until{/b},' '{b}since{/b},' '{b}while{/b},' and '{b}as long as{/b}.'"
    m "{i}Since{/i} there are so many, this category of conjunctions is the widest!"
    m "Oh, another note! A pretty common misconception is that you shouldn't begin sentences with conjunctions."
    m "As I just showed you with the last two examples, you definitely can, ahaha!"
    m "But just avoid going overboard with them. Or else you sound a little forced."
    m "I think that's enough for today, [player]."
    m "Thanks for listening!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip004",
            category=["grammar tips"],
            prompt="Semicolons",
            conditional="store.mas_gtod.has_day_past_tip(3)",
            action=EV_ACT_POOL
        )
    )

label monika_gtod_tip004:
    m "Today we will talk abot a rarely used and commonly misunderstood punctuation mark..."
    m "The semicolon!"
    m "Some interesting things have been written about semicolons, includin, this from the author Lewis Thomas..."
    m "{i}Sometimes you get a glimpse of a semicolon coming /[...], and it is like climbing a steep path through woods and seeing a wooden bench just at a bend in the road ahead, a place where you can expect to sit for a moment, catching your breath.{/i}"
    m "I appreciate how he eloquently describes something as simple as a punctuation mark!"
    m "Some people think you can use a semicolon as a substitute for a colon, while others treat it as a period..."
    m "If you recall out talk on clauses, the semicolon is actually meant to connect two independent clauses."
    m "For example, if I wanted to keep two ideas together, such as '{b}You're here{/b}' and '{b}I'm happy{/b},' I could write them as..."
    m "'{b}You're here; I'm happy{/b}' intead of '{b}You're here, and I'm happy{/b}' or '{b}You're here. I'm happy{/b}.'"
    m "All three sentences convey the same message, but...{w=0.5}in comparison, '{b}You're here; I'm happy{/b}' connects the two clauses at a happy medium."
    m "In the end, this always depends on the ideas you want to connect, but...{=0.5}I think that Thomas puts it well when you compare them to periods or commas..."
    m "Unlike a period, which opens up to a completely different sentence, or a comma, which shows you there is more to come in the same one..."
    m "A semicolon really is that in-between, or, as Thomas says, '{i}a place where you can expect to sit for a moment and catch youre breath.{/i}'"
    m "At least this gives you a whole other option; hopefully, you can now make better use of the semicolon when you're writing..."
    m "Ehehe."
    m "Okay, that's enough for today, [player]."
    m "Thanks for listening!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip005",
            category=["grammar tips"],
            prompt="Subjects and Objects",
            conditional="store.mas_gtod.has_day_past_tip(4)",
            action=EV_ACT_POOL
        )
    )

label monika_gtod_tip005:
    m "Today we'll talk about subjects and objects, [player]."
    m "Remember when I told you about clauses having an action and a verb?"
    m "The object is the person or thing that the subject acts on!"
    m "So, in the sentence '{b}We watched the fireworks together{/b},' the object would be...{w=0.5}the '{b}fireworks{/b}!'"
    m "Oh, it's important to note that the objects aren't necessary to form complete sentences..."
    m "The sentence could very well have been '{b}We watched.{/b}'"
    m "That's a complete sentence...althought it's an ambiguous one, ahaha!"
    m "There's also nothing that says that the object has to come last, but I'll discuss that in more detail another time."
    m "Just remember that the subject is doing the action and the object is acted upon."
    m "Thanks for listening, [player]! I love."
    m "...{w=1} ...{w=1}you!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip006",
            category=["grammar tips"],
            prompt="Active and Passive Voices",
            conditional="store.mas_gtod.has_day_past_tip(5)",
            action=EV_ACT_POOL
        )
    )

label monika_gtod_tip006:
    m "[player], do you know about voices in writing?"
    m "There's the active voice and the passive voice."
    m "If you remember our talk on subjects and objects, the big difference between the two voices is whether the suject or the object comes first."
    m "Let's say the subject is '{b}Sayori{/b}' and the object is a '{b}cupcake{/b}.'"
    m "Here's the sentence in an active voice: '{b}Sayori ate the last cupcake.{/b}'"
    m "Here it is again in a passive voice: '{b}The last cupcake was eaten.{/b}'"
    m "As you can see, you can use the passive voice to be secretive about the subject yet still have a complete sentence."
    m "You {i}can{/i} use the passive voice to be sneaky! It does have other uses too, though."
    m "For example, in some careers, people have to use the passive voice to be impersonal."
    m "Scientists describe experiments with '{b}the data were taken...{/b}' since the important part is their work and not who did it."
    m "Anyway, for the most part, stick with the active voice for readibility and, you know, to directly tell who's doing what."
    m "I think that's enough for today, [player], thanks for listening!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip007",
            category=["grammar tips"],
            prompt="Who vs. Whom",
            conditional="store.mas_gtod.has_day_past_tip(6)",
            action=EV_ACT_POOL
        )
    )

label monika_gtod_tip007:
    m "Today we will talk about the uses of '{b}who{/b}' and '{b}whom{/b}.'"
    m "Most of the time, it seems like people use '{b}who{/b}' without bothering to learn the difference, ahaha."
    m "The difference is that '{b}who{/b}' refers to a subject, and '{b}whom{/b}' refers to an object."
    m "It turns out that it's pretty easy to figure out when to use one or the other!"
    m "'{b}Who{/b}' corresponds to '{b}he/she/they{b}' while '{b}whom{/b}' corresponds to '{b}him/her/them{/b}.'"
    m "Simply replace the possible '{b}who{/b}' or '{b}whom{/b}' with '{b}he/she/they{b}' or '{b}him/her/them{/b}.'"
    m "Only one replacement should make sense, and that should tell you which one to use!"
    m "Let's take, for example, the title of my poem, {i}The Lady who Knows Everything{/i}."
    m "If we just look at the clause '{b}who knows everything{/b}' and replace the '{b}who{/b},' we get..."
    m "'{b}She knows everything{/b}' or '{b}her knows everything{/b}.'"
    m "Only '{b}she knows everything{/b}' makes sense, so the correct phrase is '{b}who knows everything{/b}.'"
    m "Who said writing was hard?"
    m "That's all I have for today, [player], thanks for listening!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip008",
            category=["grammar tips"],
            prompt="'And I' vs. 'And me'",
            conditional="store.mas_gtod.has_day_past_tip(7)",
            action=EV_ACT_POOL
        )
    )

label monika_gtod_tip008:
    m "Last time we talked about the difference between '{b}who{/b}' and '{b}whom{/b}.'"
    m "Another couple of words that can be just as confusing to use are '{b}and I{/b}' and '{b}and me{/b}.'"
    m "Is it '{b}[player] and I went on a date{/b}' or {b}'[player] and me went on a date{/b}?'"
    m "Just like with '{b}who{/b}' and '{b}whom{/b},' the issue boils down to one of subjects and objects."
    m "And just like when we talked about '{b}who{/b}' versus '{b}whom{/b},' it turns out there's a simple way to figure out which one is right!"
    m "In our example, if you just take out '{b}[player] and{/b}' from the sentence, only one should make sense."
    m "Let's try it out..."
    m "The end result is: '{b}I went on a date{/b}' and '{b}me went on a date{/b}.'"
    m "Clearly, only the first one makes sense, so it's {b}[player] and I went on a date{/b}.'"
    m "Oh, sorry, [player], did it make you feel left out when I said only '{b}I went on a date{/b}?'"
    m "Ahaha! Don't worry, I'd never leave you behind."
    m "Anyways, that's all for today, [player]."
    m "Thanks for listening!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip009",
            category=["grammar tips"],
            prompt="Apostrophes",
            conditional="store.mas_gtod.has_day_past_tip(8)",
            action=EV_ACT_POOL
        )
    )

label monika_gtod_tip009:
    if player[-1].lower() == 's':
        $ tempname = player
    else:
        $ tempname = 'Alexis'

    m "Today we're going to talk about apostrophes. Pretty straight forward, right?"
    m "Add them to show possession: '{b}Sayori's fork, Natsuki's spoon, Yuri's knife...{/b}'"
    m "I guess the issue that can come up is when you have to add an apostrophe to a word that ends with an '{b}s{/b}."
    m "For plural words, this is simple; just add the apostrophe at the end: '{b}monkeys'{/b}.'"
    m "It's pretty clear that '{b}monkey's{/b},' which would indicate possession belonging to a single monkey, or '{b}monkeys's{/b}' would be wrong."
    m "The gray area that comes up is when we bring in people's names, like '{b}Sanders{/b}' or '{b}[tempname]{/b}.'"
    m "In some style guides I've read, it seems that we usually add an apostrophe and '{b}s{/b}' as usual, with the exception of historical names like '{b}Sophocles{/b}' or '{b}Zeus{/b}.'"
    m "Personally, I think all that matters here is consistency!"
    m "If your're going to go with '{b}[tempname]'{/b},' then it's fine as long as you use '{b}[tempname]'{/b}' for the entire text."
    m "That matters more than honoring some old Greeks to me."
    m "One interesting exception is the case of '{b}its{/b} versus {b}it's{/b}.'"
    m "You would think that for the possessive form of '{b}it{/b}' you would add an apostrophe, making it '{b}it's{/b},' right?"
    m "Normally this would be correct, but in this case the possessive form of '{b}it{/b}' is simply '{b}its{/b}.'"
    m "This is because '{b}it's{/b}' is reserved for the contracted form of '{b}it is{/b}.'"
    m "If you're wondering, a contracton is simply a shortened version of a word or words, with an apostrophe indicating where letters have been left out to make the contraction."
    m "Okay, [player], I think that's enough for today."
    m "Thanks for listening!"
    return

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_gtod_tip010",
            category=["grammar tips"],
            prompt="The Oxford Comma",
            conditional="store.mas_gtod.has_day_past_tip(9)",
            action=EV_ACT_POOL
        )
    )

label monika_gtod_tip010:
    m "Did you know there's actually a debate about the placement of a specific comma in a list of three items?"
    m "This is called the Oxford, or serial, comma, and it's been known to completely change the meaning of a sentence!"
    m "Let me show you what I mean..."
    m "With the Oxford comma, I would say '{b}I love [player], reading, and writing.{/b}'"
    m "Without the Oxford comma, I would say '{b}I love [player], reading and writing.{/b}'"
    m "The confusion lies in whether I'm referring to loving three serparate things, or if I'm referring to just loving you when you read and write."
    m "Of course, both of those meaning are true, so there's no confusion there for me, ahaha!"
    m "That's all I have for today, thanks for listening!"
    return