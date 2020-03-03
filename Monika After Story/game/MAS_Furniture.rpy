init python:
 import store
 
 class MASFurniture:
   """ makes a class with the basic info for a Furniture Obj"""
   def __init__(self, key, value):
    self.name = key
    self.thumb = "remove"
    self.group = "furniture"
    self.display_name = self.name
    self.data = value
     
    
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
                           
            #Original
            self.name = _sprite_object.name
            self.display_name = display_name
            self.thumb = thumb + ".png"
            self.group = group
            self.unlocked = False
            self.visible_when_locked = visible_when_locked
            self.hover_dlg = hover_dlg
            self.first_select_dlg = first_select_dlg
            self.select_dlg = select_dlg
            self.selected = False
            self.disable_type = store.mas_selspr.DISB_NONE

            # by default
            # NOTE: only ACS can override this
            self.remover = False
            
            #New vars
            self.data = _sprite_object.data
            self.visible = self.data[0]
            self.img_name = self.data[1]
            self.sub_objects_present = self.data[3]

            self.size = (1280, 720)
            self.loc_str = (0,0)
            self.l_comp_str = "renpy.display.layout.LiveComposite("
            self.init_str = "{}{}".format(self.l_comp_str, self.size)
            self.path = 'mod_assets/location/spaceroom/furniture/'
            self.img_end_str = ".png"
            sprite_str_list = [self.init_str]
            self.sub_object_img = None
            self.full_composite_img = None
            if self.sub_objects_present:
                if self.sub_object_img:
                    pass
                else:
                    self.sub_objects = self.data[4]
                    self.sub_object_img = self.sub_object_composite(self.sub_objects)
            #checks for img to not rerender
            if self.full_composite_img:
                pass
            else:
                self.full_composite_img = self.full_composite()
            
        def sub_object_composite(self, sub_objects):
            keys = sub_objects.keys()
            sprite_str_list = [self.init_str]
            for x in range(len(sub_objects)):
                sprite_str_list.append(',{},"{}{}{}"'.format(self.loc_str, self.path, self.sub_objects[keys[x]],self.img_end_str))
            sprite_str_list.append(")")
            result_sub_objects = "".join(sprite_str_list)
            return eval(result_sub_objects)
            
        def full_composite(self):
            sprite_str_list = [self.init_str]
            if self.sub_object_img:
               full_composite = renpy.display.layout.LiveComposite(self.size, self.loc_str, '{}{}{}'.format(self.path, self.img_name, self.img_end_str), self.loc_str, self.sub_object_img)
            else:
               full_composite = renpy.display.layout.LiveComposite(self.size, self.loc_str, self.sub_object_img)
            return full_composite
            
            """
            MASSelectableClothes constructor

            IN:
                _sprite_object - MASFurniture object to build this selectable
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
            #   raise Exception("not a outfit: {0}".format(group))


            
 class MASSelectableImageButtonDisplayable_Furniture(store.MASSelectableImageButtonDisplayable):
    """ Modified version of the MASSelectableImageButtonDisplayable class that allows for multi select and direct asigment of variables when object is selected"""
    def _select(self):
            """
            Makes this item a selected item. Also handles other logic realted
            to selecting this.
            """

            # if already selected, then we need to deselect.
            if self.selected:
                self.selected = False
                self.selectable.selected = False
                store.mas_furniture.items[self.selectable.name][0] = self.selectable.selected
            else:
                self.selected = True 
                self.selectable.selected = True
                self.select_map[self.selectable.name] = self
                store.mas_furniture.items[self.selectable.name][0] = self.selectable.selected
                
            renpy.play(gui.activate_sound, channel="sound")
            
            #Original code, gonnal leave for now but not needed
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

            
            renpy.redraw(self, 0)
            self.end_interaction = True
            return
            


init python:
 store.tmp2 = []
 store.tmp3 = []
 store.tmp4 = []
 import store
 #Short Cut
 store.MF = store.mas_furniture



init python in mas_furniture:
 import store
 keys = ["Couch", "Table"]
 #Format [   = False, img_name = string, select_dlg = []  Sub_object = False, Sub_object_data: [[Name, img_name]]
 values = [ [False, "Couch", ["Its a couch"], True, {"Left Pillow" : "Left_pillow", "Right Pillow": "Right_pillow"}] , [ False, "Table", ["Its a table"], True, {"Book" : "Book", "Magizines": "Magizines", "Pen": "Pen", "Reading_Glasses" : "Reading_Glasses"} ] ]
 from collections import OrderedDict 
 def init_items(keys, values):
  from collections import OrderedDict 
  items = OrderedDict()
  for x in range(len(keys)):
   items[keys[x]] = values[x]
  return items
   
 items = init_items(keys, values)
 FURNITURE_SEL_MAP = OrderedDict()
 FURNITURE_SEL_SL = []  
 mailbox = store.mas_selspr.MASSelectableSpriteMailbox()
 viewport_bounds = (store.mas_selspr.SB_VIEWPORT_BOUNDS_X, store.mas_selspr.SB_VIEWPORT_BOUNDS_Y, store.mas_selspr.SB_VIEWPORT_BOUNDS_W, mailbox.read_frame_vsize(), store.mas_selspr.SB_VIEWPORT_BOUNDS_BS)

 
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

    obj_list.append(store.MASFurniture(x, type[x]))
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
        data = type.data
        new_sel_type = store.MASSelectableFurniture(type, display_name, thumb, group, select_dlg = data[2])
        
        #Set external
        store.mas_furniture.FURNITURE_SEL_MAP[type.name] = new_sel_type
        #store.mas_insertSort(store.mas_furniture.FURNITURE_SEL_SL, new_sel_type, store.mas_selspr.selectable_key)
        store.mas_furniture.FURNITURE_SEL_SL.insert(iteration, new_sel_type)


                          
                                                  

  def get_thumbnail(self, name):
   return "acs-ribbon_def.png"

 
 furniture_init = Furniture_Init()
init 10 python:
 #generates defualt list furniture objects
 store.mas_furniture.furniture_init.run_init()

init python in mas_selspr:
    #May be unused
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
       

         



label monika_furniture_select:
 #Creates the furniture objects and calls the selector with furniture list made at run_init
 call mas_selector_sidebar_select_furniture(store.mas_furniture.FURNITURE_SEL_SL)
 return

 
label mas_selector_sidebar_select_furniture(items, preview_selections=True, only_unlocked=True, save_on_confirm=True, mailbox=None, select_map={}, add_remover=False, remover_name=None):
    #Calls the selector for the furniture items = furniture objects
    $store.MF.furniture_init.run_init()
    #show furniture zorder 5
    $renpy.show_screen("drag_test", _layer = "master")
    call mas_selector_sidebar_select_furniture_main(items, 3, preview_selections, only_unlocked, save_on_confirm, mailbox, select_map, add_remover, remover_name)

    return _return
     



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
        #disp_text = "I love you!"
       # disp_fast = disp_text
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
  mf_items = store.MF.items
  keys = mf_items.keys()  
  
  sprite_str_list = [init]
  for x in range(len(mf_items)):
   if mf_items[keys[x]][0]:
    sprite_str_list.append(',{},{}{}{}"'.format(loc_str, path, store.MF.FURNITURE_SEL_MAP[keys[x]].img_name, end))
    if store.MF.FURNITURE_SEL_MAP[keys[x]].sub_objects_present:
     sprite_str_list.append(',{}, store.MF.FURNITURE_SEL_MAP["{}"].sub_object_img'.format(loc_str, keys[x]))
  sprite_str_list.append(")")
  
  result_furniture = "".join(sprite_str_list)
  store.tmp5 = result_furniture
  return eval(result_furniture),None
  
#image couch = LiveComposite((1280,720), (0,0), "mod_assets/thumbs/Couch.png")
image furniture = DynamicDisplayable(store.mas_furniture.furniture_composite)


init 20 python:
 store.drag_list = [Drag(drag_name = MF.FURNITURE_SEL_SL[0].name, d = MF.FURNITURE_SEL_SL[0].full_composite_img, drag_offscreen =True, draggable = True),Drag(drag_name = MF.FURNITURE_SEL_SL[1].name, d = MF.FURNITURE_SEL_SL[1].full_composite_img, drag_offscreen =True, draggable = True)]


init python:

 def drag_change(drags, drop):
  store.tmp = drags
  #drag_child.positions[0] = tuple([drags[0].x, drags[0].y])
  return    
  
 def add_drags(drags, draggroup):
  for x in range(len(drags)):
   current_drag_name = drags[x].drag_name
   if store.mas_furniture.items.get(current_drag_name)[0] == True:
    draggroup.add(drags[x])
   else:
    pass
  return
 
 
 def drag_test (**kwargs): 
  import store
  #ui.text("{}".format(drag_list.child))
  DG = ui.draggroup()
  add_drags(store.drag_list, DG)
  ui.close()
  return
 renpy.define_screen("drag_test", drag_test, zorder = "5")
 
init 100 python:
    config.layers = ['background', 'master', 'transient', 'screens', 'overlay' ]
