init python:
 import store

 class MASSelectableDecoration(store.MASSelectableSprite):
        """
        Wrappare around MASDecoration sprite objects

        PROPERTIES:
            (no additional)

        SEE MASSelectableSprite for inherited properties
        """
        def __init__(self,
                _sprite_data,
                display_name,
                thumb,
                group,
                visible_when_locked=True,
                hover_dlg=None,
                first_select_dlg=None,
                select_dlg=None
            ):
                           
            #Original
            self.name = display_name
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
            self.data = _sprite_data
            self.visible = self.data[0]
            self.img_name = self.data[1]
            self.sub_objects_present = self.data[3]

            self.size = (1280, 720)
            self.loc_str = (0,0)
            self.l_comp_str = "renpy.display.layout.LiveComposite("
            self.init_str = "{}{}".format(self.l_comp_str, self.size)
            self.path = 'mod_assets/location/spaceroom/decoration/'
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

 class MASSelectableImageButtonDisplayable_Decoration(store.MASSelectableImageButtonDisplayable):
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
                store.mas_decorations.items[self.selectable.name][0] = self.selectable.selected
            else:
                self.selected = True 
                self.selectable.selected = True
                self.select_map[self.selectable.name] = self
                store.mas_decorations.items[self.selectable.name][0] = self.selectable.selected
                
            renpy.play(gui.activate_sound, channel="sound")
            renpy.redraw(self, 0)
            self.end_interaction = True
            return
            


init python:
 import store
 #Short Cut
 store.MD = store.mas_decorations

init python in mas_decorations:
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
 DECORATION_SEL_MAP = OrderedDict()
 DECORATION_SEL_SL = []  
 mailbox = store.mas_selspr.MASSelectableSpriteMailbox()
 viewport_bounds = (store.mas_selspr.SB_VIEWPORT_BOUNDS_X, store.mas_selspr.SB_VIEWPORT_BOUNDS_Y, store.mas_selspr.SB_VIEWPORT_BOUNDS_W, mailbox.read_frame_vsize(), store.mas_selspr.SB_VIEWPORT_BOUNDS_BS)

 
 class Decoration_Init:
   
  def run_init(self):
   """ """

   #Resets Decoration_list
   store.mas_decorations.DECORATION_SEL_SL = []
   #Vars
   
   #Creates MASSelectableDecoration objects in the DECORATION_SEL_MAP
   self.create_MASSelectable_Obj_list(store.mas_decorations.items)
 
   #Process MASSelectableDecoration's
   for x in range(len(store.mas_decorations.DECORATION_SEL_SL)):
   
    #Adds and Sets all MASSelectableDecoration unlocked attirbute to true
    store.mas_decorations.DECORATION_SEL_SL[x].unlocked = True
    
    #Generates thumbnail for MASSelectableDecoration

    store.mas_decorations.DECORATION_SEL_SL[x].thumb = self.get_thumbnail(store.mas_decorations.DECORATION_SEL_SL[x].name)

  def get_disp_items(self, items, select_map = {}):
   """ Takes MASSelectableDecoration Objects and returns MASSelectableImageButtonDisplayable_Decoration objects"""
   disp_items = [store.MASSelectableImageButtonDisplayable_Decoration(item, select_map , viewport_bounds, mailbox) for item in items]
   return disp_items
   
  def create_MASSelectable_Obj_list(self, items):
   """Passes MASDecoration Obj to create_MASSelectable_object which creates MASSelectableDecoration objects
   IN:
   items dict of info for MASSelectableDecoration
   list of Decoration_Obj's
   """
   keys = items.keys()
   for x in range(len(keys)):
    self.create_MASSelectable_object(keys[x], items[keys[x]], x)

   
  def create_MASSelectable_object(self, key, value, iteration):
        """Creates MASSelectableDecoration objects """

        #Vars
        display_name = key
        data = value
        thumb = "remove"
        group = "decoration"
        data = value
        new_sel_type = store.MASSelectableDecoration(data, display_name, thumb, group, select_dlg = data[2])
        
        #Set external
        store.mas_decorations.DECORATION_SEL_MAP[display_name] = new_sel_type
        #store.mas_insertSort(store.mas_decorations.DECORATION_SEL_SL, new_sel_type, store.mas_selspr.selectable_key)
        store.mas_decorations.DECORATION_SEL_SL.insert(iteration, new_sel_type)

  def get_thumbnail(self, name):
   #Returns static image atm
   return "acs-ribbon_def.png"

 
 decoration_init = Decoration_Init()
init python in mas_decorations:
  
 def decoration_composite(st,at):

  size = (1280, 720)
  loc_str = (0,0)
  l_comp_str = "renpy.display.layout.LiveComposite("
  init = "{}{}".format(l_comp_str, size)
  path = '"mod_assets/location/spaceroom/decoration/'
  end = ".png"
  sprite_str_list = [init]
  MD_items = store.MD.items
  keys = MD_items.keys()  
  
  sprite_str_list = [init]
  for x in range(len(MD_items)):
   if MD_items[keys[x]][0]:
    sprite_str_list.append(',{},{}{}{}"'.format(loc_str, path, store.MD.DECORATION_SEL_MAP[keys[x]].img_name, end))
    if store.MD.DECORATION_SEL_MAP[keys[x]].sub_objects_present:
     sprite_str_list.append(',{}, store.MD.DECORATION_SEL_MAP["{}"].sub_object_img'.format(loc_str, keys[x]))
  sprite_str_list.append(")")
  
  result_decoration = "".join(sprite_str_list)
  store.tmp5 = result_decoration
  return eval(result_decoration),None
  

image decoration = DynamicDisplayable(store.mas_decorations.decoration_composite)

init python in mas_decorations:
 import store 
 def add_drags(drags, draggroup):
  for x in range(len(drags)):
   current_drag_name = drags[x].drag_name
   if store.mas_decorations.items.get(current_drag_name)[0] == True:
    draggroup.add(drags[x])
   else:
    pass
  return
 
 def decoration_drags(**kwargs): 
  DG = ui.draggroup()
  add_drags(store.drag_list, DG)
  ui.close()
  return
 renpy.define_screen("decoration_drags", decoration_drags, zorder = "5")


init 100 python:
    #adds extra layer so stuff can behind monika but for some reason you actually gotta use master
    config.layers = ['background', 'master', 'transient', 'screens', 'overlay' ]
    #generates defualt list decoration objects
    store.mas_decorations.decoration_init.run_init()
    store.drag_list = [Drag(drag_name = MD.DECORATION_SEL_SL[0].name, d = MD.DECORATION_SEL_SL[0].full_composite_img, drag_offscreen =True, draggable = True),Drag(drag_name = MD.DECORATION_SEL_SL[1].name, d = MD.DECORATION_SEL_SL[1].full_composite_img, drag_offscreen =True, draggable = True)]

### Start lables and actual menu items
init 5 python:
    """Init to add decoration selector list to apperance game menu"""
    store.mas_selspr.PROMPT_MAP["decoration"] = {"_ev": "monika_decoration_select", "change": "Can you change your decoration?",}
                                            
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_decoration_select",
            category=["appearance"],
            prompt=store.mas_selspr.get_prompt("decoration", "change"),
            pool=True,
            unlocked=True,
            aff_range=(mas_aff.HAPPY, None)
        ),
        restartBlacklist=True
    )
       

label monika_decoration_select:
 #Creates the decoration objects and calls the selector with decoration list made at run_init
 call mas_selector_sidebar_select_decoration(store.mas_decorations.DECORATION_SEL_SL)
 return

label mas_selector_sidebar_select_decoration(items, preview_selections=True, only_unlocked=True, save_on_confirm=True, mailbox=None, select_map={}):
    #Calls the selector for the decoration items = decoration objects
    $store.MD.decoration_init.run_init()
    #show decoration zorder 5
    $renpy.show_screen("decoration_drags", _layer = "master")
    call mas_selector_sidebar_select_decoration_main(items, 3, preview_selections, only_unlocked, save_on_confirm, mailbox, select_map)
    return _return

#Copies of original functions
 
label mas_selector_sidebar_select_decoration_main(items, select_type, preview_selections=True, only_unlocked=True, save_on_confirm=True, mailbox=None, select_map={}):

    python:
        # setup the mailbox
        if mailbox is None:
            mailbox = store.mas_selspr.MASSelectableSpriteMailbox()

        viewport_bounds = (
            store.mas_selspr.SB_VIEWPORT_BOUNDS_X,
            store.mas_selspr.SB_VIEWPORT_BOUNDS_Y,
            store.mas_selspr.SB_VIEWPORT_BOUNDS_W,
            mailbox.read_frame_vsize(),
            store.mas_selspr.SB_VIEWPORT_BOUNDS_BS
        )

    # sanity check to avoid crashes
    if len(items) < 1:
        return False

    python:

        # only show unlock
        if only_unlocked:
            disp_items = [
                MASSelectableImageButtonDisplayable_Decoration(
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
                MASSelectableImageButtonDisplayable_Decoration(
                    item,
                    select_map,
                    viewport_bounds,
                    mailbox,
                    False, # TODO: multi-select
                    item.disable_type
                )
                for item in items
            ]

        # disable menu interactions to prevent bugs
        disable_esc()

        # store current auto forward mode state
        afm_state = _preferences.afm_enable

        # and disable it
        _preferences.afm_enable = False

        # setup prev line
        prev_line = ""

    show screen mas_selector_sidebar_decoration(disp_items, mailbox, "mas_selector_sidebar_select_confirm_decoration", "mas_selector_sidebar_select_cancel_decoration", "mas_selector_sidebar_select_restore_decoration")


label mas_selector_sidebar_select_midloop_decoration:

    python:
        mailbox.send_conf_enable(True)
        mailbox.send_restore_enable(True)

        # display text parsing
        disp_text = mailbox.get_disp_text()
        disp_fast = mailbox.get_disp_fast()

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

label mas_selector_sidebar_select_restore_decoration:

    python:
        #Clear repeated lines
        if prev_line != disp_text:
            _history_list.pop()
            #Using this to clear relevant entries from history
            prev_line = disp_text

        # make next display fast
        mailbox.send_disp_fast()

    # jump back to mid loop
    jump mas_selector_sidebar_select_midloop_decoration

label mas_selector_sidebar_select_confirm_decoration:
    hide screen mas_selector_sidebar_decoration
    python:
        # re-enable the menu and restore afm
        _preferences.afm_enable = afm_state
        enable_esc()
        renpy.save_persistent()

    return True

label mas_selector_sidebar_select_cancel_decoration:
    hide screen mas_selector_sidebar_decoration
    python:
        # re-enable the menu and restore afm
        _preferences.afm_enable = afm_state
        enable_esc()

    return False
    
screen mas_selector_sidebar_decoration(items, mailbox, confirm, cancel, restore):
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