init python:
 store.tmp2 = []
 store.tmp3 = []
 store.tmp4 = []
 class MASSelectableImageButtonDisplayable_Furniture(MASSelectableImageButtonDisplayable):
  def _select(self):
            """
            Makes this item a selected item. Also handles other logic realted
            to selecting this.
            """
            store.tmp4.append((self.selectable.name,select_map))
            store.tmp2.append(self.selected)
            # if already selected, then we need to deselect.
            if self.selected:
                renpy.play(gui.activate_sound, channel="sound")
                self.selected = False
                self.selectable.selected = False
                store.mas_furniture.items[self.selectable.name][0] = self.selectable.selected
                #del self.select_map[self.selectable.name]
                renpy.redraw(self, 0)
                self.end_interaction = True
                return

            else:
             self.selected = True

            # TODO: should be moved to the top when deselect can happen
            # play the select sound
            renpy.play(gui.activate_sound, channel="sound")

            # otherwise select self
            """
            if not self.multi_select:
                # must clean select map
                for item in self.select_map.itervalues():
                    store.tmp4.append(1)
                    # setting to False will queue for removal of item
                    # NOTE: the caller must handle teh removal
                    item.selected = False
                    renpy.redraw(item, 0)
            """
            # add this item to the select map

            self.selectable.selected = True
            self.select_map[self.selectable.name] = self
            store.mas_furniture.items[self.selectable.name][0] = self.selectable.selected
            #renpy.redraw(item, 0)
            # the appropriate dialogue
            """
            if self.been_selected:
                if self.selectable.select_dlg is not None:
                    # this should be first as it allows us to override
                    # remover dialogue
                    self._send_select_text()

                elif self.selectable.remover:
                    self.mailbox.send_disp_fast()

                else:
                    self._send_generic_select_text()

            else:
                # not been selected before
                self.been_selected = True
                if self.selectable.first_select_dlg is not None:
                    self._send_first_select_text()

                elif self.selectable.select_dlg is not None:
                    self._send_select_text()

                elif self.selectable.remover:
                    self._send_msg_disp_text(None)
                    self.mailbox.send_disp_fast()

                else:
                    self._send_generic_select_text()

            # always reset interaction if something has been selected
            """
            
            self.end_interaction = True
            #return

init python:
 import store
 store.MF = store.mas_furniture

init python:
 class MASSelectableFurniture(store.MASSelectableSprite):
        """
        Wrappare around MASFurniture sprite objects

        PROPERTIES:
            (no additional)

        SEE MASSelectableSprite for inherited properties
        """


        def __init__(self,
                _sprite_object,
                display_name,
                thumb,
                group,
                visible_when_locked=True,
                hover_dlg=None,
                first_select_dlg=None,
                select_dlg=None
            ):
            """
            MASSelectableClothes constructor

            IN:
                _sprite_object - MASSelectableFurniture object to build this selectable
                    sprite object with.
                display_name - name to show on the selectable screen
                thumb - thumbnail to use on the select screen
                group - group id to group related selectable sprites.
                visible_when_locked - True if this item should be visible in
                    the screen when locked, False otherwise
                    (Default: True)
                hover_dlg - list of text to display when hovering over the
                    object
                    (Default: None)
                first_select_dlg - text to display the first time you select
                    this sprite
                    (Default: None)
                select_dlg - list of text to display everytime you select this
                    sprite
                    (after the first time)
                    (Default: None)
            """
            #if type(_sprite_object) != MASFurniture:
            #   raise Exception("not a furniture: {0}".format(group))

            super(store.MASSelectableFurniture, self).__init__(
                _sprite_object,
                display_name,
                thumb,
                group,
                visible_when_locked,
                hover_dlg,
                first_select_dlg,
                select_dlg,
            )
init python in mas_furniture:
 import store
 keys = ["Couch", "Table"]
 values = [[False, "couch"], [False, "table"]]
 from collections import OrderedDict 
 def init_items(keys, values):
  from collections import OrderedDict 
  items = OrderedDict()
  for x in range(len(keys)):
   items[keys[x]] = values[x]
  return items
   
 #been_selected_status = {}
 items = init_items(keys, values)
 enabled_items = []
 FURNITURE_SEL_MAP = OrderedDict()
 FURNITURE_SEL_SL = []  
 mailbox = store.mas_selspr.MASSelectableSpriteMailbox()
 viewport_bounds = (store.mas_selspr.SB_VIEWPORT_BOUNDS_X, store.mas_selspr.SB_VIEWPORT_BOUNDS_Y, store.mas_selspr.SB_VIEWPORT_BOUNDS_W, mailbox.read_frame_vsize(), store.mas_selspr.SB_VIEWPORT_BOUNDS_BS)
 class MASFurniture:
   """ makes a class with the basic info for a Furniture Obj"""
   def __init__(self, key, value):
    self.name = key
    self.thumb = "remove"
    self.group = "furniture"
    self.display_name = self.name
    self.data = value
 
 class Furniture_Init:
   
  def run_init(self):
   """ """

   #Resets Furniture_list
   store.mas_furniture.FURNITURE_SEL_SL = []
   #Vars
   
   #Creates MASSelectableFurniture objects in the FURNITURE_SEL_MAP
   self.get_MASSelectable_Obj_list(self.get_Type_Obj_list())
 
   #Process MASSelectableFurniture's
   for x in range(len(store.mas_furniture.FURNITURE_SEL_SL)):
   
    #Adds and Sets all MASSelectableFurniture unlocked attirbute to true
    store.mas_furniture.FURNITURE_SEL_SL[x].unlocked = True
    
    #Generates thumbnail for MASSelectableFurniture

    store.mas_furniture.FURNITURE_SEL_SL[x].thumb = self.get_thumbnail(store.mas_furniture.FURNITURE_SEL_SL[x].name)

   
   #Set vars
   #Gets MASSelectableImageButtonDisplayable_Furniture objects
   items = store.mas_furniture.FURNITURE_SEL_SL
   disp_items =  self.get_disp_items(items)
   
   return disp_items
   
  def get_disp_items(self, items, select_map = {}):
   """ Takes MASSelectableFurniture Objects and returns MASSelectableImageButtonDisplayable_Furniture objects"""
   disp_items = [store.MASSelectableImageButtonDisplayable_Furniture(item, select_map , viewport_bounds, mailbox) for item in items]
   return disp_items
   
  def get_MASSelectable_Obj_list(self, obj_list):
   """Passes MASFurniture Obj to create_MASSelectable_object which creates MASSelectableFurniture objects
   IN:
   obj_list: list
   list of Furniture_Obj's
   """
   i = 0
   for x in obj_list:
    self.create_MASSelectable_object(x, i)
    i += 1
    
  def get_Type_Obj_list(self):
   """ makes list of Furniture objects"""
   #Vars
   obj_list = []
   type = store.mas_furniture.items
   
   #Main
   for x in type.keys():

    obj_list.append(store.mas_furniture.MASFurniture(x, type[x]))
   return obj_list 
   
  def create_MASSelectable_object(self, type, iteration):
        """Creates MASSelectableFurniture objects """
        # no duplicates
        #if clothes.name in CLOTH_SEL_MAP:
        #    raise Exception(
        #        "Clothes already is selectable: {0}".format(clothes.name)
        #    )
        
        #Vars
        display_name = type.display_name
        thumb = type.thumb
        group = type.group
        new_sel_type = store.MASSelectableFurniture(type, display_name, thumb, group,)
        
        #Set external
        store.mas_furniture.FURNITURE_SEL_MAP[type.name] = new_sel_type
        #store.mas_insertSort(store.mas_furniture.FURNITURE_SEL_SL, new_sel_type, store.mas_selspr.selectable_key)
        store.mas_furniture.FURNITURE_SEL_SL.insert(iteration, new_sel_type)



  def get_thumbnail(self, name):
   return "acs-ribbon_def.png" #"{}.png".format(store.mas_furniture.items[name])

  
 furniture_init = Furniture_Init()
init 10 python:
 store.mas_furniture.furniture_init.run_init()

init python in mas_selspr:
    def _adjust_furniture(
            moni_chr,
            old_map,
            new_map,
            select_type = 3,
            use_old=False
        ):
        store.tmp = new_map, old_map
        # determine which map to change to
        if use_old:
            select_map = old_map
        else:
            select_map = new_map
            
        """
        for item in select_map.itervalues():

                try:
                    store.MF.items[new_map.keys()[0]][0] =  new_map.values()[0].selected
                except Exception as e:
                    pass
                try:
                    store.MF.items[old_map.keys()[0]][0] =  old_map.values()[0].selected
                except Exception as e:
                    pass
                return # quit early since you can only have 1 clothes
        """


### Start lables and actual menu items
init 5 python:
    """Init to add furniture selector list to apperance game menu"""
    store.mas_selspr.PROMPT_MAP["furniture"] = {"_ev": "monika_furniture_select", "change": "Can you change your furniture?",}
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_furniture_select",
            category=["appearance"],
            prompt=store.mas_selspr.get_prompt("furniture", "change"),
            pool=True,
            unlocked=True,
            aff_range=(mas_aff.HAPPY, None)
        ),
        restartBlacklist=True
    )
### End

### Start

label monika_furniture_select:
 #Creates the furniture objects and calls the selector with furniture list made at run_init
 call mas_selector_sidebar_select_furniture(store.mas_furniture.FURNITURE_SEL_SL)
 return
 
label mas_selector_sidebar_select_furniture(items, preview_selections=True, only_unlocked=True, save_on_confirm=True, mailbox=None, select_map={}, add_remover=False, remover_name=None):
    #Calls the selector for the furniture items = furniture objects
    python:
     return_check = store.MF.furniture_init.run_init()
     while len(return_check) != len(store.MF.items):
      pass
    show furniture zorder 5
    call mas_selector_sidebar_select_furniture_main(items, 3, preview_selections, only_unlocked, save_on_confirm, mailbox, select_map, add_remover, remover_name)

    return _return
#End 


#Copies of original functions
 
label mas_selector_sidebar_select_furniture_main(items, select_type, preview_selections=True, only_unlocked=True, save_on_confirm=True, mailbox=None, select_map={}, add_remover=False, remover_name=None):

    python:
        """
        if not store.mas_selspr.valid_select_type(select_type):
            raise Exception(
                "invalid selection constant: {0}".format(select_type)
            )
        """
        # otherwise, quickly setup the flags for what mode we are in.
#        selecting_acs = select_type == store.mas_selspr.SELECT_ACS
#        selecting_hair = select_type == store.mas_selspr.SELECT_HAIR
#        selecting_clothes = select_type == store.mas_selspr.SELECT_CLOTH

        # setup the mailbox
        if mailbox is None:
            mailbox = store.mas_selspr.MASSelectableSpriteMailbox()
        
        # save state
        #prev_moni_state = monika_chr.save_state(True, True, True)
        #mailbox.send_prev_state(prev_moni_state)

        # initalize vsize
        #if mailbox.read_outfit_checkbox_visible():
       #     mailbox.send_frame_vsize(
       #         store.mas_selspr.SB_VIEWPORT_BOUNDS_H1
       #     )

        # pull out the remover selectable for special use, if found
        remover_item = store.mas_selspr._rm_remover(items)
        remover_disp_item = None

        viewport_bounds = (
            store.mas_selspr.SB_VIEWPORT_BOUNDS_X,
            store.mas_selspr.SB_VIEWPORT_BOUNDS_Y,
            store.mas_selspr.SB_VIEWPORT_BOUNDS_W,
            mailbox.read_frame_vsize(),
            store.mas_selspr.SB_VIEWPORT_BOUNDS_BS
        )

        # if in outfit mode, apply the outfit before launching
        #if mailbox.read_outfit_checkbox_checked():
       #     monika_chr.change_clothes(
       #         monika_chr.clothes,
       #         by_user=True,
        #        outfit_mode=True
        #    )

    # sanity check to avoid crashes
    if len(items) < 1:
        return False

    python:

        # however, we only want to actually create a remover if we were
        # asked to do so
        if add_remover:
            if remover_item is None:
                sample_sel = items[0]
                sample_obj = sample_sel.get_sprobj()

                # create generic remover item
                remover_item = store.mas_selspr.create_selectable_remover(
                    sample_obj.acs_type,
                    sample_sel.group,
                    remover_name
                )

            # unlock the remover
            remover_item.unlocked = True

            # create the displayable
            remover_disp_item = MASSelectableImageButtonDisplayable_Furniture(
                remover_item,
                select_map,
                viewport_bounds,
                mailbox
            )

        # only show unlock
        if only_unlocked:
            disp_items = [
                MASSelectableImageButtonDisplayable_Furniture(
                    item,
                    select_map,
                    viewport_bounds,
                    mailbox,
                    False, # TODO: multi-select
                    item.disable_type
                )
                for item in items
                if item.unlocked
            ]

        else:
            disp_items = [
                MASSelectableImageButtonDisplayable_Furniture(
                    item,
                    select_map,
                    viewport_bounds,
                    mailbox,
                    False, # TODO: multi-select
                    item.disable_type
                )
                for item in items
            ]

        # fill select map
        item_found = store.mas_selspr._fill_select_map_and_set_remover(
            monika_chr,
            select_type,
            disp_items,
            select_map,
            remover_disp_item=remover_disp_item
        )

        # make copy of old select map
        
        old_select_map = dict(select_map)

        # also create views that we use for comparisons
        old_view = old_select_map.viewkeys()
        new_view = select_map.viewkeys()

        # disable menu interactions to prevent bugs
        disable_esc()

        # store current auto forward mode state
        afm_state = _preferences.afm_enable

        # and disable it
        _preferences.afm_enable = False

        # setup prev line
        prev_line = ""

    show screen mas_selector_sidebar_furniture(disp_items, mailbox, "mas_selector_sidebar_select_confirm_furniture", "mas_selector_sidebar_select_cancel_furniture", "mas_selector_sidebar_select_restore_furniture", remover=remover_disp_item)

label mas_selector_sidebar_select_loop_furniture:
    python:

        # select map parsing
        store.mas_selspr._clean_select_map(
            select_map,
            select_type,
            preview_selections,
            monika_chr
        )
        """
        if preview_selections:

            store.mas_selspr._adjust_furniture(
                monika_chr,
                old_select_map,
                select_map,
                select_type,
            )
            
            old_select_map = dict(select_map)
            #store.tmp3.append(old_select_map)
        """

label mas_selector_sidebar_select_midloop_furniture:

    python:
        # once select map is cleaned, check if diff
        has_diff = not store.mas_selspr.is_same(old_view, new_view)
        #has_diff = not monika_chr.same_state(prev_moni_state)
        mailbox.send_conf_enable(True)
        mailbox.send_restore_enable(True)

        # display text parsing
        disp_text = mailbox.get_disp_text()
        disp_fast = mailbox.get_disp_fast()
        disp_text = "I love you!"
        disp_fast = disp_text
        if disp_text is None:
            disp_text = mailbox.read_def_disp_text()

        if disp_fast:
            disp_text += "{fast}"
    
        # force this to execute in this python block (no prediction)
        renpy.say(m, disp_text)

        #Clear repeated lines
        if prev_line != disp_text:
            _history_list.pop()
            #Using this to clear relevant entries from history
            prev_line = disp_text

    jump mas_selector_sidebar_select_loop_furniture

label mas_selector_sidebar_select_restore_furniture:

    python:
        # clean the selections
        store.mas_selspr._clean_select_map(
            select_map,
            select_type,
            False,
            monika_chr,
            force=True
        )
    
        # restore monika back to previous
        #monika_chr.restore(prev_moni_state)

        # refill selections
        store.mas_selspr._fill_select_map_and_set_remover(
            monika_chr,
            select_type,
            disp_items,
            select_map,
            remover_disp_item=remover_disp_item
        )

        #Clear repeated lines
        if prev_line != disp_text:
            _history_list.pop()
            #Using this to clear relevant entries from history
            prev_line = disp_text

        # make next display fast
        mailbox.send_disp_fast()

    # jump back to mid loop
    jump mas_selector_sidebar_select_midloop_furniture

label mas_selector_sidebar_select_confirm_furniture:
    hide screen mas_selector_sidebar_furniture

    # re-enable the menu and restore afm
    $ _preferences.afm_enable = afm_state
    $ enable_esc()

    python:
        if not save_on_confirm:
            store.mas_selspr._clean_select_map(
                select_map,
                select_type,
                preview_selections,
                monika_chr
            )

#            store.mas_selspr._adjust_furniture(
#                monika_chr,
#                old_select_map,
#                select_map,
#                select_type,
#                True
#            )

            # reload state
            #monika_chr.restore(prev_moni_state)

        # If monika is wearing a remover ACS, remove it.
        #for item_name in select_map.keys():
         #   sel_obj = select_map[item_name].selectable
         #   if sel_obj.remover:
          #      spr_obj = sel_obj.get_sprobj()
          #      monika_chr.remove_acs(spr_obj)
          #      select_map.pop(item_name)

        # delete the remover if we used one
        if add_remover:
            store.mas_selspr.rm_selectable_remover(remover_item)

        # always save confirming
        #monika_chr.save()
        renpy.save_persistent()

    return True

label mas_selector_sidebar_select_cancel_furniture:
    hide screen mas_selector_sidebar_furniture

    # re-enable the menu and restore afm
    $ _preferences.afm_enable = afm_state
    $ enable_esc()

    python:
        store.mas_selspr._clean_select_map(
            select_map,
            select_type,
            preview_selections,
            monika_chr
        )

#        store.mas_selspr._adjust_furniture(
#            monika_chr,
#            old_select_map,
#            select_map,
#            select_type,
#            True
#        )

        # delete the remover if we used one
        if add_remover:
            store.mas_selspr.rm_selectable_remover(remover_item)



    return False
    
screen mas_selector_sidebar_furniture(items, mailbox, confirm, cancel, restore, remover=None):
    zorder 50
#    modal True

    $ sel_frame_vsize = mailbox.read_frame_vsize()

    frame:
        area (1075, 5, 200, sel_frame_vsize)
        background Frame(store.mas_ui.sel_sb_frame, left=6, top=6, tile=True)

        vbox:
            xsize 200
            xalign 0.5
            viewport id "sidebar_scroll":
                mousewheel True
                arrowkeys True

                vbox:
                    xsize 200
                    spacing 10
                    null height 1

                    # add the remover
                    if remover is not None:
                        add remover:
                            xalign 0.5

                    for selectable in items:
                        add selectable:
#                            xoffset 5
                            xalign 0.5

                    null height 1

            null height 10

            if mailbox.read_outfit_checkbox_visible():
                $ ocb_checked = mailbox.read_outfit_checkbox_checked()
                textbutton _("Outfit Mode"):
                    style mas_ui.st_cbx_style
                    activate_sound gui.activate_sound
                    action [
                        ToggleField(persistent, "_mas_setting_ocb"),
                        Function(
                            mailbox.send_outfit_checkbox_checked,
                            not ocb_checked
                        )
                    ]
                    selected ocb_checked

            if mailbox.read_conf_enable():
                textbutton _("Confirm"):
                    style store.mas_ui.hkb_button_style
                    xalign 0.5
                    action Jump(confirm)
            else:
                frame:
                    ypadding 5
                    xsize 120
                    xalign 0.5

                    background Image(store.mas_ui.hkb_disabled_bg)
                    text "Confirm" style store.mas_ui.hkb_text_style

            if mailbox.read_restore_enable():
                textbutton _("Restore"):
                    style store.mas_ui.hkb_button_style
                    xalign 0.5
                    action Jump(restore)

            else:
                frame:
                    ypadding 5
                    xsize 120
                    xalign 0.5

                    background Image(store.mas_ui.hkb_disabled_bg)
                    text "Restore" style store.mas_ui.hkb_text_style

            textbutton _("Cancel"):
                style store.mas_ui.hkb_button_style
                xalign 0.5
                action Jump(cancel)
#                action Function(mailbox.mas_send_return, -1)

        vbar value YScrollValue("sidebar_scroll"):
            style "mas_selector_sidebar_vbar"
            xoffset -25




init python in mas_furniture:
 
 def furniture_composite(st,at):

  size = (1280, 720)
  loc_str = (0,0)
  l_comp_str = "renpy.display.layout.LiveComposite("
  init = "{}{}".format(l_comp_str, size)
  path = '"mod_assets/location/spaceroom/furniture/'
  end = ".png"
  sprite_str_list = [init]
  mf = store.MF.items
  keys = mf.keys()  
  
  sprite_str_list = [init]
  for x in range(len(mf)):
   if mf[keys[x]][0]:
    sprite_str_list.append(',{},{}{}{}"'.format(loc_str, path, mf[keys[x]][1],end))
  sprite_str_list.append(")")

  result_furniture = "".join(sprite_str_list)
  store.tmp5 = result_furniture
  return eval(result_furniture),None
  
#image couch = LiveComposite((1280,720), (0,0), "mod_assets/thumbs/Couch.png")
image furniture = DynamicDisplayable(store.mas_furniture.furniture_composite)

