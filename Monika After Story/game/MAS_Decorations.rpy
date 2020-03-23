default persistent.mas_decorations_items = {}

init python:
 import store
 class MASDecoration(MASSpriteFallbackBase):
    def __init__(self,
            name,
            img_sit,
            pose_map,
            img_stand="",
            stay_on_start=False,
            entry_pp=None,
            exit_pp=None,
            ex_props=None,
            unlock = False,
            thumb = None
        ):
        import store
        self.name = name
        self.img_sit = img_sit
        self.stay_on_start = stay_on_start
        self.__sp_type = store.mas_sprites_json.SP_DECORATIONS
        self.pose_map = pose_map
        self.entry_pp = entry_pp
        self.ex_props = ex_props
        self.unlock = unlock
        self.thumb = thumb
        self.dir = store.mas_decorations.DECORATION_DIR
        self.FILE_EXT = store.mas_sprites.FILE_EXT
        self.full_img_path = "{}{}{}".format(self.dir, self.img_sit, self.FILE_EXT)
        
    def _build_loadstrs(self):
        to_verify = []
        to_verify.append(self.full_img_path)

        return to_verify
            
    def gettype(self):
        """
        Gets the type of this sprite object

       RETURNS: type of this sprite object
        """
        return self.__sp_type
        
 class MASSelectableDecoration(store.MASSelectableSprite):
        """
        Wrappare around MASDecoration sprite objects

        PROPERTIES:
            (no additional)

        SEE MASSelectableSprite for inherited properties
        """
        def __init__(self,
                decoration,
                display_name,
                thumb,
                group,
                visible_when_locked=True,
                hover_dlg=None,
                first_select_dlg=None,
                select_dlg=None
            ):

            self._sprite_object = decoration
            self.name = self._sprite_object.name
            store.MASSelectableSprite.__init__(self, self._sprite_object, display_name, thumb, group, visible_when_locked, hover_dlg, first_select_dlg, select_dlg)      
            self.data = self._sprite_object 
            self.img_sit = self._sprite_object.img_sit
            if len(self.data.pose_map) > 0:
                self.sub_objects_present = True
            else:
                self.sub_objects_present = False
            
            self.size = (1280,720)
            self.loc_str = (0,0)
            self.l_comp_str = "renpy.display.layout.LiveComposite("
            self.init_str = "{}{}".format(self.l_comp_str, self.size)
            self.path = 'mod_assets/location/spaceroom/decoration/'
            self.img_end_str = ".png"
            self.sprite_str_list = [self.init_str]
            self.sub_object_img = None
            self.full_composite_img = None  
            if self.sub_objects_present:
                self.sub_objects = self.data.pose_map
                if self.sub_object_img:
                    pass
                else:
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
                sprite_str_list.append(',{},"{}{}{}"'.format(self.loc_str, self.path, sub_objects[keys[x]], self.img_end_str))
            sprite_str_list.append(")")
            result_sub_objects = "".join(sprite_str_list)
            return eval(result_sub_objects)
            
        def full_composite(self):
            sprite_str_list = [self.init_str]
            if self.sub_object_img:
               full_composite = renpy.display.layout.LiveComposite(self.size, self.loc_str, '{}{}{}'.format(self.path, self.img_sit, self.img_end_str), self.loc_str, self.sub_object_img)
            else:
               full_composite = renpy.display.layout.LiveComposite(self.size, self.loc_str, self.sub_object_img)
            return full_composite

 class MASSelectableImageButtonDisplayable_Decoration(store.MASSelectableImageButtonDisplayable):
    def __init__(self,
        _selectable,
        select_map,
        viewport_bounds,
        mailbox=None,
        multi_select=False,
        disable_type=store.mas_selspr.DISB_NONE
        ):
        
        store.MASSelectableImageButtonDisplayable.__init__(self, _selectable, select_map, viewport_bounds, mailbox, multi_select, disable_type)
        if store.persistent.mas_decorations_items.get(self.selectable.name) is not None:
            self.selected = store.persistent.mas_decorations_items.get(self.selectable.name)["selected"]

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
                store.persistent.mas_decorations_items[self.selectable.name]["selected"] = self.selectable.selected
                for x in store.persistent.mas_decorations_items.keys():
                 store.mas_decorations_items_tmp_pos[x]["pos"] = store.drag_dict[x].x, store.drag_dict[x].y
            else:
                self.selected = True 
                self.selectable.selected = True
                self.select_map[self.selectable.name] = self
                store.persistent.mas_decorations_items[self.selectable.name]["selected"] = self.selectable.selected

                    
            # the appropriate dialogue
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
 from collections import OrderedDict 
 DECORATION_SEL_MAP = OrderedDict()
 DECORATION_SEL_SL = []
 json_iteration = 0
 default_visibility = False
 DECORATION_DIR = "mod_assets/location/spaceroom/decoration/"

 def create_MASSelectable_object_from_json(sel_params):
        """Creates MASSelectableDecoration objects """
        new_sel_type = store.MASSelectableDecoration(**sel_params)
        #Should ge this param from json
        new_sel_type.unlocked = True
        #Set external
        store.mas_decorations.DECORATION_SEL_MAP[sel_params.get("decoration").name] = new_sel_type
        #store.mas_insertSort(store.mas_decorations.DECORATION_SEL_SL, new_sel_type, store.mas_selspr.selectable_key)
        store.mas_decorations.DECORATION_SEL_SL.insert(store.mas_decorations.json_iteration, new_sel_type)
        store.mas_decorations.json_iteration +=1
        return new_sel_type

        
init python in mas_decorations:
  
 def decoration_composite(st,at):
  size = (1280,720)
  loc_str = ",(0,0),"
  l_comp_str = "renpy.display.layout.LiveComposite("
  init = "{}{}".format(l_comp_str, size)
  path = '"mod_assets/location/spaceroom/decoration/'
  sprite_str_list = [init]
  MD_items = DECORATION_SEL_MAP
  keys = MD_items.keys()
  persistent_data = store.persistent.mas_decorations_items
  
  for x in range(len(MD_items)):
   current_key = keys[x]
   current_item = MD_items[current_key]

   drag_loc_str = persistent_data[current_key]["pos"]
   
   if persistent_data[current_key]["selected"] == True:
    sprite_str_list.append(', {}, MD_items.get("{}").full_composite_img'.format(drag_loc_str, current_key))

  sprite_str_list.append(")")
  
  result_decoration = "".join(sprite_str_list)
  store.tmp5 = result_decoration
  return eval(result_decoration), None
  

image decoration = DynamicDisplayable(store.mas_decorations.decoration_composite)

init python in mas_decorations:
 import store 
 
 def save_persistent_drag_pos():
  items = store.persistent.mas_decorations_items
  keys = items.keys()
  drag_dict = store.drag_dict
  
  for x in range(len(items)):
   current_key = keys[x]
   current_item = drag_dict[current_key]
   if drag_dict.get(current_key) is not None:
    x_pos = drag_dict.get(current_key).x
    y_pos = drag_dict.get(current_key).y
    drag_loc_str = (x_pos, y_pos)
   else:
    drag_loc_str = (0,0)
   items[current_key]["pos"] = drag_loc_str
  
 def add_drags(drag_dict, draggroup):
  persistent_data = store.persistent.mas_decorations_items
  keys = drag_dict.keys()
  create_drag_dict(store.mas_decorations_items_tmp_pos)
  
  for x in range(len(drag_dict)):
   current_key = keys[x]
   current_item = drag_dict[current_key]
   if store.persistent.mas_decorations_items.get(current_item.drag_name)["selected"] == True:

    draggroup.add(current_item)
   else:
    pass
  return

 def decoration_drags(**kwargs): 
  DG = ui.draggroup()
  add_drags(store.drag_dict, DG)
  ui.close()
  return
 renpy.define_screen("decoration_drags", decoration_drags, zorder = "5")
 
 def create_drag_dict(persistent_data = store.persistent.mas_decorations_items):
  Drag = renpy.display.dragdrop.Drag
  items = DECORATION_SEL_MAP
  keys = items.keys()
  for x in range(len(DECORATION_SEL_MAP)):
   current_key = keys[x]
   current_item = items[current_key]
   store.drag_dict[current_item.name] = Drag(drag_name = current_item.name, d = current_item.full_composite_img, drag_offscreen = True, draggable = True, xpos = persistent_data[current_key]["pos"][0], ypos = persistent_data[current_key]["pos"][1])
  return
  
init 100 python:
    #adds extra layer so stuff can behind monika but for some reason you actually gotta use master
    config.layers = ['background', 'master', 'transient', 'screens', 'overlay' ]
    
    #generates defualt list decoration objects
    import store
    from collections import OrderedDict
    store.drag_dict = OrderedDict()
    
init 999 python:
 import store
 def variables_screen(**kwargs): 
  try:
   couch_pos = store.drag_dict.get("couch").x, store.drag_dict.get("couch").y
   table_pos = store.drag_dict.get("table").x, store.drag_dict.get("table").y

  except:
   couch_pos = None
   table_pos = None

  try:
   couch_xypos = store.drag_dict.get("couch").xpos, store.drag_dict.get("couch").ypos
   table_xypos = store.drag_dict.get("table").xpos, store.drag_dict.get("table").ypos
   
  except: 
   couch_xypos = None
   table_xypos = None
  
  persistent_couch = store.persistent.mas_decorations_items["couch"]["pos"]
  persistent_table = store.persistent.mas_decorations_items["table"]["pos"]
  
  ui.text("Couch x_y {}, Table x_y {}".format(couch_pos, table_pos), ypos = 0)
  ui.text("Persistent Couch {}, Persistent Table {}".format(persistent_couch, persistent_table), ypos = 20)
  ui.text("Couch x_ypos {}, Table x_ypos {}".format(couch_xypos, table_xypos), ypos = 40)
  
  return
 #renpy.define_screen("variables", variables_screen, zorder = "10")

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
    python:
     renpy.hide("decoration")
     store.mas_decorations.create_drag_dict()
     renpy.show_screen("decoration_drags", _layer = "master")
     store.mas_decorations_items_backup = store.persistent.mas_decorations_items.copy()
     store.mas_decorations_items_tmp_pos = {}
     for x in store.persistent.mas_decorations_items.keys():
      store.mas_decorations_items_tmp_pos[x] = {}
      store.mas_decorations_items_tmp_pos[x]["pos"] = store.persistent.mas_decorations_items[x]["pos"]
      
     #renpy.show_screen("variables", _layer = "master")
    call mas_selector_sidebar_select_decoration_main(items, 3, preview_selections, only_unlocked, save_on_confirm, mailbox, select_map)
    python:
     if _return == True:
      store.mas_decorations.save_persistent_drag_pos()
     renpy.hide_screen("decoration_drags", layer = "master")
     renpy.show("decoration", zorder = 5)
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
        store.mas_decorations.create_drag_dict(store.mas_decorations_items_backup)
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
        store.mas_decorations.create_drag_dict(store.mas_decorations_items_backup)
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

            
            
init python in mas_sprites:
 DECORATION_MAP = {}       
           
init -20 python in mas_sprites_json:
    SP_DECORATIONS = 3
    SP_CONSTS = (
        SP_ACS,
        SP_HAIR,
        SP_CLOTHES,
        SP_DECORATIONS,
    )
    SP_STR[SP_DECORATIONS] = "DECORATION"
    SP_UF_STR[SP_DECORATIONS] = "decoration"
    SP_PP[SP_DECORATIONS] = "store.mas_sprites._clothes_{0}_{1}"
    SP_RL[SP_DECORATIONS] = "mas_reaction_gift_clothes_{0}"


            
init 190 python in mas_sprites_json:
    def addSpriteObject(filepath):
        """ 
        Adds a sprite object, given its json filepath

        NOTE: most exceptions logged
        NOTE: may raise exceptions

        IN:
            filepath - filepath to the JSON we want to load
        """
        dry_run = False
        jobj = None
        msgs_err = []
        msgs_warn = []
        msgs_info = []
        msgs_exprop = []
        obj_based_params = {}
        sp_obj_params = {}
        sel_params = {}
        unlock_hair = True
        giftname = None
        indent_lvl = 0
        writelog("\n" + MSG_INFO.format(READING_FILE.format(filepath)))
        
        # can we read file
        with open(filepath, "r") as jsonfile:
            jobj = json.load(jsonfile)

        # is file json
        if jobj is None:
            writelog(MSG_ERR.format(JSON_LOAD_FAILED.format(filepath)))
            return

        if DRY_RUN in jobj:
            jobj.pop(DRY_RUN)
            dry_run = True

        # get rid of __keys
        for jkey in jobj.keys():
            if jkey.startswith("__"):
                jobj.pop(jkey)

        # determine version. Versions must match SP_JSON_VER. 
        if VERSION_TXT not in jobj:
            # must be version 1 (aka the initial release).
            # or just missing.
            writelog(MSG_ERR.format(VER_NOT_FOUND))
            return

        # version text exists, check it
        version = jobj.pop(VERSION_TXT)

        # check type
        if not _verify_int(version, allow_none=False):
            # not valid version type, err this
            writelog(MSG_ERR.format(VER_BAD.format(SP_JSON_VER, version)))
            return

        # check version match
        if version != SP_JSON_VER:
            writelog(MSG_ERR.format(VER_BAD.format(SP_JSON_VER, version)))
            return
        # otherwise we good version

        ## this happens in 3 steps:
        # 1. build sprite object according to the json
        #   - this includes PoseMaps
        # 2. build selectable (if provided)
        # 3. Init everything
        #
        # Everything should be wrapped in try/excepts. All exceptions should
        #   be logged, but we include the warning in the function comment
        #   in case.

        # determine type
        sp_type = _validate_type(jobj)
        if sp_type is None:
            return

        # check name and img_sit
        msg_log = []
        _validate_params(
            jobj,
            sp_obj_params,
            REQ_SHARED_PARAM_NAMES,
            True,
            msg_log,
            indent_lvl
        )
        if parsewritelogs(msg_log):
            return

        # save name for later
        sp_name = sp_obj_params["name"]

        # log out that we are loading the sprite object and name
        writelog(MSG_INFO.format(SP_LOADING.format(
            SP_STR.get(sp_type),
            sp_name
        )))
        indent_lvl = 1
        # check for existence of pose_map property. We will not validate until
        # later.
        if "pose_map" not in jobj:
            writelog(MSG_ERR_ID.format(REQ_MISS.format("pose_map")))
            return

        # move object-based params out of the jobj
        for param_name in OBJ_BASED_PARAM_NAMES:
            if param_name in jobj:
                obj_val = jobj.pop(param_name)

                # objects must be dicts
                if not _verify_dict(obj_val, allow_none=False):
                    writelog(MSG_ERR_ID.format(BAD_TYPE.format(
                        param_name,
                        dict,
                        type(obj_val)
                    )))
                    return

                obj_based_params[param_name] = obj_val

        # validate optional shared params
        msg_log = []
        _validate_params(
            jobj,
            sp_obj_params,
            OPT_SHARED_PARAM_NAMES,
            False,
            msg_log,
            indent_lvl
        )
        if parsewritelogs(msg_log):
            return

        if sp_type == SP_ACS:
            # ACS
            msg_log = []
            _validate_acs(
                jobj,
                sp_obj_params,
                obj_based_params,
                msg_log,
                indent_lvl
            )
            if parsewritelogs(msg_log):
                return  
        elif sp_type == SP_DECORATIONS:
            pass
            
        else:
            # hair / clothes
            msg_log = []
            _validate_fallbacks(
                jobj,
                sp_obj_params,
                obj_based_params,
                msg_log,
                indent_lvl
            )
            if parsewritelogs(msg_log):
                return

            if sp_type == SP_HAIR:
                msg_log = []
                _validate_hair(
                    jobj,
                    sp_obj_params,
                    obj_based_params,
                    msg_log,
                    indent_lvl
                )
                if parsewritelogs(msg_log):
                    return
            elif sp_type == SP_CLOTHES:
                # must be clothes
                msg_log = []
                _validate_clothes(
                    jobj,
                    sp_obj_params,
                    obj_based_params,
                    sp_name,
                    dry_run,
                    msg_log,
                    indent_lvl
                )
                if parsewritelogs(msg_log):
                    return

        # now for specific params

            
        # back to shared acs/hair/clothes stuff
        _validate_ex_props(
            jobj,
            sp_obj_params,
            obj_based_params,
            msgs_err,
            msgs_warn,
            msgs_info
        )
        if len(msgs_err) > 0:
            writelogs(msgs_warn)
            writelogs(msgs_err)
            return

        # select info if found
        if "select_info" in obj_based_params:
            msg_log = []
            _validate_selectable(
                jobj,
                sel_params,
                obj_based_params,
                msg_log,
                indent_lvl
            )
            if parsewritelogs(msg_log):
                return

        # time to check for warnings/recommendes

        # extra property warnings
        for extra_prop in jobj:
            writelog(MSG_WARN_ID.format(EXTRA_PROP.format(extra_prop)))

        # no gift/unlock warnings
        if "unlock" in sp_obj_params:
            unlock_hair = sp_obj_params.pop("unlock")
            giftname = None

        elif "giftname" in sp_obj_params:
            giftname = sp_obj_params.pop("giftname")

            # validate gift stuff
            _check_giftname(giftname, sp_type, sp_name, msgs_err, MSG_ERR_ID)
            if len(msgs_err) > 0:
                writelogs(msgs_err)
                return

        elif sp_type != SP_HAIR:
            writelog(MSG_WARN_ID.format(NO_GIFT))
            giftname = None
            
        # progpoint processing
        _process_progpoint(
            sp_type,
            sp_name,
            sp_obj_params,
            msgs_warn,
            msgs_info,
            "entry"
        )
        _process_progpoint(
            sp_type,
            sp_name,
            sp_obj_params,
            msgs_warn,
            msgs_info,
            "exit"
        )
        writelogs(msgs_info)
        writelogs(msgs_warn)
        # now we can build the sprites
        try:
            if sp_type == SP_ACS:
                sp_obj = store.MASAccessory(**sp_obj_params)
                sms.init_acs(sp_obj)
                sel_obj_name = "acs"

            elif sp_type == SP_HAIR:
                sp_obj = store.MASHair(**sp_obj_params)
                sms.init_hair(sp_obj)
                sel_obj_name = "hair"

            elif sp_type == SP_CLOTHES:
                # clothing
                sp_obj = store.MASClothes(**sp_obj_params)
                sms.init_clothes(sp_obj)
                sel_obj_name = "clothes"
            elif sp_type == SP_DECORATIONS:
                # clothing
                _validate_params(
                    jobj,
                    sp_obj_params,
                    OPT_HAIR_PARAM_NAMES,
                    True,
                    msg_log,
                    indent_lvl
                )
                new = sp_obj_params.copy()
                new.update(obj_based_params)
                new["thumb"] = sel_params.get("thumb")
                sp_obj = store.MASDecoration(**new)
                sel_obj_name = "decoration"

        except Exception as e:
            # in thise case, we ended up with a duplicate
            writelog(MSG_ERR.format(e.message))
            return
        # check image loadables
        _test_loadables(sp_obj, msgs_err)
        if len(msgs_err) > 0:
            writelogs(msgs_err)
            _reset_sp_obj(sp_obj)
            return
        # otherwise, we were successful in initializing this sprite
        # try initializing the selectable if we parsed it
        if len(sel_params) > 0:
            sel_params[sel_obj_name] = sp_obj

            try:
                if sp_type == SP_ACS:
                    sml.init_selectable_acs(**sel_params)

                elif sp_type == SP_HAIR:
                    sml.init_selectable_hair(**sel_params)
                    if unlock_hair:
                        sml.unlock_hair(sp_obj)

                elif sp_type == SP_CLOTHES:
                    # clothing
                    sml.init_selectable_clothes(**sel_params)
                    
                elif sp_type == SP_DECORATIONS:
                    store.sel_params_tmp = sel_params
                    obj = store.mas_decorations.create_MASSelectable_object_from_json(sel_params)
                    if store.persistent.mas_decorations_items.get(obj.name) is not None:
                        pass
                    else:
                        store.persistent.mas_decorations_items[obj.name] = {}
                        store.persistent.mas_decorations_items[obj.name]["selected"] = store.mas_decorations.default_visibility
                        store.persistent.mas_decorations_items[obj.name]["pos"] = (0,0)
                
            except Exception as e:
                # we probably ended up with a duplicate again
                writelog(MSG_ERR.format(e.message))

                # undo the sprite init
                _reset_sp_obj(sp_obj)
                return
        # giftname must be valid by here
        if giftname is not None and not dry_run:
            _init_giftname(giftname, sp_type, sp_name)

        # alright! we have built the sprite object!
        if dry_run:
            _reset_sp_obj(sp_obj)
            writelog(MSG_INFO.format(SP_SUCCESS_DRY.format(
                SP_STR.get(sp_type),
                sp_name
            )))

        else:
            sp_obj.is_custom = True
            writelog(MSG_INFO.format(SP_SUCCESS.format(
                SP_STR.get(sp_type),
                sp_name
            )))

