
# Every line containing the character '#' will be discarded
# use them for commentary

## THIS TEXT HAS A SPECIAL SYNTAX, IT'S NOT A PYTHON ARCHIVE ##
## Every movie must start with the keyword "movie" followed by the name
## [DESCRIPTION]
## if "description" is the first word, the line will be used for Monika's description
## of the film
## The line MUST contain an image for her to display

## example:
## description 1o "This film talks about AI"
## description 1o "It could be fun"


## [MOVIE REACTIONS]
## if "m" is the first word, the line will be used for Monika's reactions.
## The line can or can not contain a reaction from the cheatsheet (like 1b)
## The line must contain the exact second where that reaction will be reproduced
## with the format [HH:MM:SS]
## The line must contain a message even if it's nothing, example: ""
## There must be a gap between lines of 10 seconds. The line will be automatically
## hide waiting for the next reaction

## example:
## m 1k [00:32:52] "I hate this jumpscares!"
## m [00:33:05] "But they're also fun"
## m 4f [01:12:05] ""

## [CLOSURE]
## if "closure" is the first word, the line will be used for Monika's closure
## after the word closure add the event label which we'll push once the movie
## ends

## example:
## closure monika_difficulty

movie Doki Doki Trailer
description 3b "So the trailer for the game, huh?"
description 1j "Let's watch it together, then [player]!"
m 1lksdla [00:00:04] "I wonder why they'd put a warning there."
m 1hub [00:00:20] "Ahaha, I remember those poems you tried to make."
m 1dsd [00:00:35] "If only they just introduced me instead of including the others..."
# TODO replace with an actual label for it
closure monika_difficulty
