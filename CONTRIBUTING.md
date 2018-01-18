init 5 python:
    for key in ['absurd', 'absurdism', 'french', 'pointless', 'reason']:
        monika_topics.setdefault(key,[])
        monika_topics[key].append('monika_absurd') 
    

label monika_absurd:
    m 4a "That reminds me of a theory that I read about recently."
    m "It's called Absurdism..."
    m 2a "It was brought about by a French philosopher named Albert Camus."
    m "He said that humans would constantly search for meaning, but they'd never find it."
    m "Like reading all day, scolling on social media, or playing video games."
    m "Camus claimed that humans were wasting their lives seeking for answeres that did not exist."
    m 2d "Isn't that sad?"
    m "Imagine living your whole life knowing that none of your work matters."
    m "I acctually did...that is...until you saved me, [player]."
    m "Have you ever felt like that?"
    m 4a "If so, I'm always here."
    m "..."
    m 4d "He also said that people should accept the world for how it is, and try to make their own purposes in life."
    m 2m "I don't have my life that figured out."
    m 2j "How about you?"
    m 4e "Do you have any life goals?"
    show monika 5a at t11 zorder 2 with dissolve
    m 5a "Of course, there is one thing that gives my life some color..."
    m "Three guesses what?"
    m 4 "Literature! Of course!"
    m 5a "Ahaha..."
    m "What were you expecting?"
    m 4 "Something like, 'Your the meaning to my universe, [player]! I want to be with you forever!'?"
    m 2m "Well..maybe."
    return
    
    init 5 python:
      
    addEvent(Event(eventlabel="monika_seizure",category=['light'],prompt="Did you know?",random=True))

label monika_seizure:
    m 3a "Did you know that one in every five people had, have, or will have some form of Epilepsy?."
    m "That is, cronic seizures, but not really."
    m "It can go away as randomly as it occurs."
    m "People have been known to contract this illness at varying ages."
    m "It seems pretty tought. If you know someone like that, don't forget to brighten up their day."
    m 4 "But not too much!"
    return
    
    
    




