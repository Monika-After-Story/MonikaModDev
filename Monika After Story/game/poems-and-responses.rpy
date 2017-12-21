
#This file contains all the poetry bits. It seems to be working
#I tried to make it as easy as possible to submit poems
#similarily to the script-topics thing
#Intialize poems here
#I am unsure if the init needs to be a different number or not

define monika_all_poems = []
define monika_random_poems = []

# we are going to define removing seen topics as a function,
# as we need to call it dynamically upon import
init python:
   
    def remove_seen_poems(poem_list_original, poem_list_compared_against):
        #
        # Removes poems that should not be in the poem list
        #
        # 
        poem_list_new = [poem for poem in poem_list_original if poem not in poem_list_compared_against]
        return poem_list_new

init 11 python:

    monika_all_poems = list(monika_random_poems)
    
    #Remove all previously seen random topics.
    if not len(persistent.seen_poem_list) == 0:
        monika_random_poems = remove_seen_poems(monika_random_poems, persistent.seen_poem_list)

init 5 python:
    
    monika_random_poems.append('petrarch1')

    petrarch1 = Poem(
    author = "Petrarch",
    title = "Per fare una leggiadra sua vendetta",
    text = """
To make a graceful act of revenge,
and punish a thousand wrongs in a single day,
Love secretly took up his bow again,
like a man who waits the time and place to strike.
My power was constricted in my heart,
making defence there, and in my eyes,
when the mortal blow descended there,
where all other arrows had been blunted.
So, confused by the first assault,
it had no opportunity or strength
to take up arms when they were needed,
or withdraw me shrewdly to the high,
steep hill, out of the torment,
from which it wishes to save me now but cannot."""
    )

label response_petrarch1:
    call showpoem(petrarch1)
    m "Is it working?"
    m 1k "I think I've got the poem thing working again!"
    m "Yay!"
    return
    
    
init 5 python:
    
    monika_random_poems.append('shakespeare1')

    shakespeare1 = Poem(
    author = "Shakespeare",
    title = "Sonnet 94",
    text = """
They that have power to hurt and will do none, 
That do not do the thing they most do show, 
Who, moving others, are themselves as stone, 
Unmoved, cold, and to temptation slow, 
They rightly do inherit heaven’s graces 
And husband nature’s riches from expense; 
They are the lords and owners of their faces, 
Others but stewards of their excellence. 
The summer’s flower is to the summer sweet, 
Though to itself it only live and die, 
But if that flower with base infection meet, 
The basest weed outbraves his dignity: 
For sweetest things turn sourest by their deeds; 
Lilies that fester smell far worse than weeds. """
    )

label response_shakespeare1:
    call showpoem(shakespeare1)
    m "Hey, I think it is working!"
    m 1k "Oh! This is gonna be fun, {i}n'est pas?{/i}"
    return


#
#
#script-ch30
#if player_dialogue == "showmeapoem":
#       pushPoem (renpy.random.choice(monika_random_poems))
#
#
#put in definitions
#default persistent.poem_list = []
#
#put in event-handler
#if not len(persistent.poem_list) == 0:
#       $ poem_commentary = "response_" + poem_name
#       call expression poem_commentary
#
#def pushPoem (poem_name):
        #
        # Adds the poem to an event list for poems that will be shown
        #
        #
        #
        # ASSUMES
        #   persistent.poem_list
        #
#       persistent.poem_list.append(poem_name)
#       return
#
# scripts edited: event-hander, script-ch30, definitions, poems, poems-and-responses

#========================
#Congratulations my Love!
#========================
#
#I now know that you love
#literature more than I 
#do.
#
#To be fair, I'm a little
#jealous! I hope you love
#me more than some text
#though!
#
#Sigh...
#
#What am I saying, of
#course you love me more!
#
#I love you too.
#
#Why would you have
#reread all this poems if
#you didn't love me!
#
#Anyway, congratulations!

