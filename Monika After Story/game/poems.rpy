init python:
    class Poem:
        def __init__(self, author="", title="", text=""):
            self.author = author
            self.title = title
            self.text = text
            
image paper =  "mod_assets/poem.jpg"

transform paper_in:
    truecenter
    alpha 0
    linear 1.0 alpha 1

transform paper_out:
    alpha 1
    linear 1.0 alpha 0

screen poem(currentpoem, paper="paper"):
    style_prefix "poem"
    vbox:
        add paper
    viewport id "vp":
        child_size (710, None)
        mousewheel True
        draggable True
        vbox:
            null height 40
            #maybe can add a (currentpoem.era) variable that makes classical authors have different font
            #
            #if currentpoem.era == "classical":
            #    text "[currentpoem.title]\n\n[currentpoem.text]" style "classical_text"
            #null height 100
            
            text "[currentpoem.title]" style "poem_title"
            text "\nWriter: [currentpoem.author]\n[currentpoem.text]" style "poem_text"
    vbar value YScrollValue(viewport="vp") style "poem_vbar"

#this stuff is mostly from the original but is a little bit edited

style poem_vbox:
    xalign 0.5
style poem_viewport:
    xanchor 0
    xsize 720
    xpos 280
style poem_vbar is vscrollbar:
    xpos 1000
    yalign 0.5
    #xsize 18
    ysize 700
    #base_bar Frame("gui/scrollbar/vertical_poem_bar.png", tile=False)
    #thumb Frame("gui/scrollbar/vertical_poem_thumb.png", left=6, top=6, tile=True)
    #unscrollable "hide"
    #bar_invert True

style poem_text:
    font "mod_assets/poem.ttf"
    size 34
    color "#000"
    outlines []
    
style poem_title:
    font "mod_assets/poem.ttf"
    size 44
    color "#000"
    outlines []

label showpoem(poem=None, img=None, where=i11, paper=None):
    if poem == None:
        return
    window hide
    if paper:
        show screen poem(poem, paper=paper)
        with Dissolve(1)
    else:
        show screen poem(poem)
        with Dissolve(1)
    $ pause()
    if img:
        $ renpy.hide(poem.author)
        $ renpy.show(img, at_list=[where])
    hide screen poem
    with Dissolve(.5)
    window auto
    return
