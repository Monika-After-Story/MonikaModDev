#V.0.1.8.0

default persistent.mas_decorations_items = {}

init 5 python:
 import store
 #Short Cut
 store.MD = store.mas_decorations
 

init python:

        
    class MASDecoration(MASSpriteFallbackBase):
        """
        This is an offshot of MASClothes/MASAccessory classes to keep proper formatting with json system.
        This class is used to pass infromation to create MASSelectableDecoration objects from the jsons system.
        """
        
        def __init__(self,
            name,
            img_sit,
            pose_map,
            img_stand="",
            stay_on_start=False,
            entry_pp=None,
            exit_pp=None,
            ex_props=None,
            weather_map = {},
            sub_objects = {},
            unlock = False,
            thumb = None
            ):
      
            """
            Constructor.

            IN:
                name - name of this decoration
                img_sit - file name of the main decoration image
                pose_map - MASPoseMap object that contains information for sub_objects
                img_stand - N/A just keep for compatibility reasons
                stay_on_start - N/A just keep for compatibility reasons
                entry_pp - programming point to call when wearing this sprite
                    the MASMonika object that is being changed is fed into this
                    function
                    (Default: None)
                exit_pp - programming point to call when taking off this sprite
                    the MASMonika object that is being changed is fed into this
                    function
                    (Default: None)
                ex_props - dict of additional properties to apply to this
                    decoration object. This can be used to specify the existence of 
                    different asset versions for different weathers.
                    (Default: None)
            """
            #imports
            import store


            #Standard properties
            self.name = name
            self.img_sit = img_sit
            self.pose_map = pose_map
            self.ex_props = ex_props
            self.unlock = unlock
            self.thumb = thumb
            
            #Specific to Decorations
            self.weather_map = weather_map
            self.sub_objects = sub_objects
            self.dir = store.mas_decorations.DECORATION_DIR
            self.FILE_EXT = store.mas_sprites.FILE_EXT
            self.__sp_type = store.mas_sprites_json.SP_DECORATIONS
            self.full_img_path = "{0}{1}{2}".format(self.dir, self.img_sit, self.FILE_EXT)

            
            #Currently unused
            self.entry_pp = entry_pp
            self.entry_pp = entry_pp
            self.img_stand = img_stand
            self.stay_on_start = stay_on_start

        
        def _build_loadstrs(self):
            """
            Just gets img_sit to be verified

            RETURNS: List with img_sit just so it works with the existing verification system 
            """
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
        def __init__(self, 
                    decoration, 
                    display_name,
                    thumb, 
                    group, 
                    visible_when_locked=True, 
                    hover_dlg=None, 
                    first_select_dlg=None, 
                    select_dlg=None,
                    unlocked = True):
            """
            IN:
                decoration - MASDecoration object 

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
            
            #Imports
            import store


            #Init
            self._sprite_object = decoration
            store.MASSelectableSprite.__init__(self, self._sprite_object, display_name, thumb, group, visible_when_locked, hover_dlg, first_select_dlg, select_dlg)


            #Set basic normal properties
            self.ex_props = self._sprite_object.ex_props
            self.name = self._sprite_object.name          
            self.img_sit = self._sprite_object.img_sit
            self.unlocked = unlocked
            
            #Comp setup
            
            #Checks it there are any sub_objects in the posemap, this var will determine if sub_objects are ever added
            if len(self._sprite_object.sub_objects) > 0:
                self.sub_objects_present = True
            else:
                self.sub_objects_present = False
                
            self.size = store.mas_sprites.LOC_WH
            self.loc = (0,0)
            self.l_comp_str = store.mas_sprites.L_COMP
            self.init_str = "{0}({1}".format(self.l_comp_str, self.size)
            self.sprite_str_list = [self.init_str]
            self.sub_object_str = store.mas_decorations.sub_object_str
            self.full_composite_str = store.mas_decorations.full_composite_str
            self.composite_map = {}
            
            #IO Setup
            self.path = self._sprite_object.dir
            self.file_ext_str = self._sprite_object.FILE_EXT
            
            #Weather_map setup
            self.weather_map = self._sprite_object.weather_map
            self.weather_map["def"] =  {}
                                                                                              
            self.same_map_str = store.mas_decorations.same_map_str
                                                                                                     
            
            
            
            #Final setup, creates keys and values for composite_map
            self.def_str = "def"
            self.times = store.mas_decorations.times_dict 

            if self.sub_objects_present:
                self.sub_objects = self._sprite_object.sub_objects
                self.composite_init("sub", self.times)
                
            self.composite_init("full", self.times)
            
        
        def get_comp_value(self, mode, weather, times, time_of_day):
            """
            Generates value which will be assigned to a composition key in the composite_map
            
            IN:
                mode - Specifies are we going for a sub_objects or full composite
                weather - weahter key from weather_map
                times - dictionary of suffix's for differnet times
                time_of_day - key from times
                
            RETURNS: LiveComposite 
            """
            
            if mode == "sub":
                value  = self.sub_object_composite(sub_objects = self.sub_objects, weather = weather, night_suffix = times[time_of_day])
            elif mode == "full":
                sub_objects = self.composite_map.get('{0}_{1}_{2}'.format(self.sub_object_str, weather, time_of_day))
                value  = self.full_composite(sub_objects = sub_objects, weather = weather, night_suffix = times[time_of_day])
            return value
            
        def get_same_comp_value(self, comp_key_str, weather, time_of_day):
            """
            Get values from composite_map to assign to other weathers in the composite_map
            
            IN:
                comp_key_str - Major stirng used as a base to build the composite_map key
                weather - weather key from weather_map
                time_of_day - key from times
                
            RETURNS: LiveComposite 
            """
            
            value = self.composite_map.get("{0}_{1}_{2}".format(comp_key_str, weather, time_of_day))
            return value
            
        def composite_init(self, mode, times):
            """
            IN:
                mode - Specifies are we going for sub_objects or full composite
                times - dictionary of suffix's for differnet times
                
            """
            
            #Sets comp_key_str based on mode
            if mode == "sub":
                comp_key_str = self.sub_object_str
            elif mode == "full":
                comp_key_str = self.full_composite_str
            
            #Iterates weather_map
            for key in self.weather_map.keys():
            
                #ignore same_map until the end once everything else is defined
                if key == self.same_map_str:
                    pass
                   
                #Interates through times and sets composite_map entries
                else:
                    for time_of_day in times.keys():
                    
                        #Check if ignore_night or ignore_night are true and use def values instead
                        if self.weather_map[key].get("ignore_night") == True and time_of_day == "night":
                            value = self.get_same_comp_value(comp_key_str, self.def_str, time_of_day)
                            
                        elif self.weather_map[key].get("ignore_day") == True and time_of_day == "day":
                            value = self.get_same_comp_value(comp_key_str, self.def_str, time_of_day)
                            
                        #Else just get value normal for the differnt weather
                        else:
                            value = self.get_comp_value(mode, key, times, time_of_day)
                            
                        #Finnaly Sets the composite_map key/value
                        self.composite_map["{0}_{1}_{2}".format(comp_key_str, key, time_of_day)] = value
            
            #Handles same_map values
            
            #Checks if the same_map key exists
            if self.same_map_str in self.weather_map.keys():
            
                #Init vars
                same_dict = self.weather_map[self.same_map_str]
                same_keys = same_dict.keys()
                
                #Iterates through weathers whose value will be used for other weathers
                for same_key in same_keys:
                
                    #Iterates through same_map what weathers will equal the same_map key
                    for same_weather in same_dict[same_key]:
                        for time_of_day in times.keys():
                        
                            #Gets value and sets composite_map
                            value = self.get_same_comp_value(comp_key_str, same_key, time_of_day)
                            self.composite_map["{0}_{1}_{2}".format(comp_key_str, same_weather, time_of_day)] = value
            return 


        def sub_object_composite(self, sub_objects, weather = "def", night_suffix = ""):
            """
            IN: 
                sub_objects - dictionary of addional objs that should be added to the composite
                weather - string for weather of the current composite img
                night_suffix - string for time of dat of the current composite img
                
            RETURNS: LiveComposite
            """
            #Init vars
            keys = sub_objects.keys()
            sprite_str_list = [self.init_str]
            
            #Iterates through the len() of sub_objects
            for i in range(len(sub_objects)):
                sprite_str_list.append(',{0},"{1}{2}{3}{4}{5}{6}"'.format(self.loc, self.path, sub_objects[keys[i]], mas_sprites.ART_DLM, weather, night_suffix, self.file_ext_str))
            sprite_str_list.append(")")
            result_sub_objects = "".join(sprite_str_list)
            return eval(result_sub_objects)
     
        def full_composite(self, sub_objects, weather = "def", night_suffix = ""):
            """
            IN:
                sub_objects - LiveCompsite of desired sub_objects to be added to full comp_key_str
                weather - string for weather of main full composite img
                night_suffix - string for time of dat of the current composite img
            RETURNS: LiveComposite
            """
            #Init Vars
            sprite_str_list = [self.init_str]
            
            
            if sub_objects:
               full_composite = renpy.display.layout.LiveComposite(self.size, self.loc, '{}{}{}{}{}{}'.format(self.path, self.img_sit, mas_sprites.ART_DLM, weather, night_suffix, self.file_ext_str), self.loc, sub_objects)
            else:
               full_composite = renpy.display.layout.LiveComposite(self.size, self.loc, '{}{}{}{}{}{}'.format(self.path, self.img_sit, mas_sprites.ART_DLM, weather, night_suffix, self.file_ext_str))
               
            return full_composite
            

        



    class MASSelectableImageButtonDisplayable_Decoration(store.MASSelectableImageButtonDisplayable):
        """
        Modified version of the MASSelectableImageButtonDisplayable class that allows for multi select and direct asigment of variables when object is selected
        """
        
        def __init__(self,
            _selectable,
            select_map,
            viewport_bounds,
            mailbox=None,
            multi_select=False,
            disable_type=store.mas_selspr.DISB_NONE
            ):
            """
            Constructor for this displayable

            IN:
                selectable - the selectable object we want to encapsulate
                select_map - dict containing group keys of previously selected
                    objects.
                viewport_bounds - tuple of the following format:
                    [0]: xpos of the viewport upper left
                    [1]: ypos of the viewport upper left
                    [2]: width of the viewport
                    [3]: height of the viewport
                    [4]: border size
                mailbox - dict to send messages to outside from this
                    displayable.
                    (Default: None)
                multi_select - True means we can select more than one item.
                    False otherwise
                    (Default: False)
                disable_type - pass in a disable constant to disable this item
                    for the specified reason.
                    (Default: 0 - DISB_NONE)
            """
            
            store.MASSelectableImageButtonDisplayable.__init__(self, _selectable, select_map, viewport_bounds, mailbox, multi_select, disable_type)
            if store.persistent.mas_decorations_items.get(self.selectable.name) is not None:
                self.selected = store.persistent.mas_decorations_items.get(self.selectable.name)["selected"]

        def _select(self):
            """
            Makes this item a selected item. Also handles other logic realted
            to selecting this.
            """

            # if already selected, then we need to deselect.
            if self.selected:
                self.selected = False
                self.selectable.selected = False
                #Sets persistent so decoration will remain when we come back to it
                store.persistent.mas_decorations_items[self.selectable.name]["selected"] = self.selectable.selected
                for key in store.persistent.mas_decorations_items.keys():
                 if drag_dict.get(key) is not None:
                #Sets persistent position about this decoration so it stays in the same spot
                    store.mas_decorations_items_tmp_pos[x]["pos"] = store.drag_dict[x].x, store.drag_dict[x].y
                        
            else:
                self.selected = True 
                self.selectable.selected = True
                self.select_map[self.selectable.name] = self
                #Sets persistent so decoration will go away
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
            

init 100 python:
    #adds extra layer so stuff can behind monika but for some reason you actually gotta use master
    config.layers = ['background', 'master', 'transient', 'screens', 'overlay' ]
    
    #generates defualt list decoration objects
    import store
    from collections import OrderedDict 
    store.drag_dict = OrderedDict()

    
init -1 python in mas_decorations:
    #Imports
    import store
    from collections import OrderedDict 
    
    #Init Vars
    DECORATION_SEL_MAP = OrderedDict()
    DECORATION_SEL_SL = []
    DECORATION_DIR = "mod_assets/location/spaceroom/decoration/"
    json_iteration = 0
    default_visibility = False
    sub_object_str = "sub_object_img"
    full_composite_str = "full_composite_img"
                                     
    same_map_str = "same_map"
    times_dict = {"day" : "", "night" : store.mas_sprites.NIGHT_SUFFIX}
    

    def create_MASSelectable_object_from_json(sel_params):
        """
        Creates MASSelectableDecoration objects 
        
        IN:
            sel_params - 
        RETURNS: 
        """
        new_sel_type = store.MASSelectableDecoration(**sel_params)
  
        store.mas_decorations.DECORATION_SEL_MAP[sel_params.get("decoration").name] = new_sel_type
        store.mas_decorations.DECORATION_SEL_SL.insert(store.mas_decorations.json_iteration, new_sel_type)
        store.mas_decorations.json_iteration +=1
        return new_sel_type

        
    def get_weather_suffix():
        """ Gets the suffix to add to make the composition key
        
            RETURNS: full weather suffix & the time suffix strings
        """
        
        mas_weather_suffix = [store.mas_current_weather.weather_id]
        if store.morning_flag:
            time_suffix = "_day"
            mas_weather_suffix.append(time_suffix)
        else:
            time_suffix = "_night"
            mas_weather_suffix.append(time_suffix)
        mas_weather_suffix = "".join(mas_weather_suffix)
        return mas_weather_suffix, time_suffix
  
    def full_comp_exists(items, current_key, mas_weather_suffix):
        """ 
        Verifies the composite key exists
        
        IN :
            items - current dictionary of items to get() from
            current_key - key of current MASSelectableDecoration object
            mas_weather_suffix - suffix to add to regular key to get proper time and weather key
            
        RETURNS: True/False
        """
        return items[current_key].composite_map.get('full_composite_img_{}'.format(mas_weather_suffix))
    
    def get_full_comp_str(drag_loc_str, current_key, mas_weather_suffix):
        """
        IN:
            drag_loc_str - location str for LiveComposite
            current_key - key of current MASSelectableDecoration object
            mas_weather_suffix - suffix to add to regular key to get proper time and weather key
            
        RETURNS: string to be used in genrateding composite 
        """
        return ', {}, items["{}"].composite_map["full_composite_img_{}"]'.format(drag_loc_str, current_key, mas_weather_suffix)
    

    def decoration_composite(st,at):
        """ 
        IN:
            st, at - Stuff required for DynamicDisplayable
        RETURN LiveComposite
        """
    
        size = (1280,720)
        l_comp_str = "renpy.display.layout.LiveComposite("
        init = "{}{}".format(l_comp_str, size)
        path = '"mod_assets/location/spaceroom/decoration/'
        sprite_str_list = [init]
        items = DECORATION_SEL_MAP
        keys = items.keys()
        persistent_data = store.persistent.mas_decorations_items
        
        #Checks if decoration was selected when in drag mode
        for x in range(len(items)):
            current_key = keys[x]
            current_item = items[current_key]
            drag_loc_str = persistent_data[current_key]["pos"]

            #Checks if the comp we are about to access actually exists
            if persistent_data[current_key]["selected"] == True:
                mas_weather_suffix, time = get_weather_suffix()
                if full_comp_exists(items, current_key, mas_weather_suffix) is not None:
                    sprite_str_list.append(get_full_comp_str(drag_loc_str, current_key, mas_weather_suffix))
                else:
                    sprite_str_list.append(get_full_comp_str(drag_loc_str, current_key, "def{}".format(time)))

        sprite_str_list.append(")")
        
        result_decoration = "".join(sprite_str_list)
        return eval(result_decoration), None




    def reload_decorations():
        """Deletes and reloads decorations""" 
        DECORATION_SEL_SL = []
        DECORATION_SEL_MAP = {}
        mas_sprites_json.addSpriteObjects()
 
 
 
    def save_persistent_drag_pos():
        """
        Takes postion of decoration as a drag and sets it in persistent
        """
        #Init Vars
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
        """ 
        IN: 
            drag_dict - dictonary of drags to add to dragroup form
            draggroup - draggroup to add drags to
        """
       
        #Init Vars
        keys = drag_dict.keys()
        create_drag_dict(store.mas_decorations_items_tmp_pos)
  
        for i in range(len(drag_dict)):
            current_key = keys[i]
            current_item = drag_dict[current_key]
            
            #if decoration in persistent and is "selected" or active added it
            if store.persistent.mas_decorations_items.get(current_item.drag_name)["selected"] == True:
                draggroup.add(current_item)
            else:
                pass
        return
  

    def decoration_drags(**kwargs): 
        """
        
        """
        DG = ui.draggroup()
        add_drags(store.drag_dict, DG)
        ui.close()
        return
        
    renpy.define_screen("decoration_drags", decoration_drags, zorder = "5")
 
 
 
    def create_drag_dict(dec_data = store.persistent.mas_decorations_items):
        """
        Creates a drag dictionary based off of saved data
        
        IN: 
            dec_data - decoration data used to build the drag dictionary 
        """

        #Init Vars
        Drag = renpy.display.dragdrop.Drag
        items = DECORATION_SEL_MAP
        keys = items.keys()
        
        for x in range(len(DECORATION_SEL_MAP)):
            current_key = keys[x]
            current_item = items[current_key]
            mas_weather_suffix, time = get_weather_suffix()
   
            if full_comp_exists(items, current_key, mas_weather_suffix) is not None:
                value = current_item.composite_map["full_composite_img_{}".format(mas_weather_suffix)]
            else:
                value = current_item.composite_map["full_composite_img_{}".format("def{}".format(time))]
    
            store.drag_dict[current_item.name] = Drag(drag_name = current_item.name, d = value, drag_offscreen = True, draggable = True, xpos = dec_data[current_key]["pos"][0], ypos = dec_data[current_key]["pos"][1])
        return
  

  
  
image decoration = DynamicDisplayable(store.mas_decorations.decoration_composite)

    


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
      

    call mas_selector_sidebar_select_decoration_main(items, 3, preview_selections, only_unlocked, save_on_confirm, mailbox, select_map)
    
    python:
        if _return == True:
            store.mas_decorations.save_persistent_drag_pos()
        renpy.hide_screen("decoration_drags", layer = "master")
        renpy.show("decoration", zorder = 5)
            
    return _return
    

 
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

    

        
        
init -20 python in mas_sprites_json:
    WM_LOADING = "loading weather_map..."
    WM_SUCCESS = "weather_map loaded successfully!"
    WM_BAD_K_TYPE = "key '{0}' - expected type {1}, got {2}"
    WM_BAD_V_TYPE = "value for key '{0}' - expected type dict, got {1}"
    SO_LOADING = "loading sub_objects..."
    SO_SUCCESS = "sub_objects loaded successfully!"
    SO_BAD_K_TYPE = "key '{0}' - expected type {1}, got {2}"
    SO_BAD_V_TYPE = "value for key '{0}' - expected type str, got {1}"

                                    
    OBJ_BASED_PARAM_NAMES = (
        "pose_map",
        "ex_props",
        "weather_map",
        "sub_objects",
        "select_info",
        "split",
        "hair_map",
        "arm_split",
        "pose_arms",
        HLITE,
    )

init 190 python in mas_sprites_json:

    def _validate_weather_map(jobj, save_obj, obj_based, msg_log, ind_lvl):
        """
        Validates weather_map dict


        IN:
            jobj - json object to parse
            obj_based - dict of object-based items
                (contains weather_map)
            ind_lvl - indentation level

        OUT:
            save_obj - dict to save data to
            msg_log - list to save messages to
        """

        # validate weather_map

        if "weather_map" not in obj_based:
            return

        # weather_map exists, get and validate
        msg_log.append((MSG_INFO_T, ind_lvl, SO_LOADING))
        weather_map = obj_based.pop("weather_map")

        isbad = False

        for ep_key, ep_val in weather_map.iteritems():
            if not _verify_str(ep_key):
                msg_log.append((
                    MSG_ERR_T,
                    ind_lvl + 1,
                    SO_BAD_K_TYPE.format(ep_key, str, type(ep_key))
                ))
                isbad = True

            if not _verify_dict(ep_val):
                msg_log.append((
                    MSG_ERR_T,
                    ind_lvl + 1,
                    SO_BAD_V_TYPE.format(ep_key, type(ep_val))
                ))
                isbad = True

        # check for no errors

        if isbad:
            return

        # otherwise, we can say successful loading!
        msg_log.append((MSG_INFO_T, ind_lvl, SO_SUCCESS))
        save_obj["weather_map"] = weather_map
        
    def _validate_sub_objects(jobj, save_obj, obj_based, msg_log, ind_lvl):
        """
        Validates sub_objects dict


        IN:
            jobj - json object to parse
            obj_based - dict of object-based items
                (contains sub_objects)
            ind_lvl - indentation level

        OUT:
            save_obj - dict to save data to
            msg_log - list to save messages to
        """

        # validate sub_objects

        if "sub_objects" not in obj_based:
            return

        # sub_objects exists, get and validate
        msg_log.append((MSG_INFO_T, ind_lvl, WM_LOADING))
        sub_objects = obj_based.pop("sub_objects")

        isbad = False

        for ep_key, ep_val in sub_objects.iteritems():
            if not _verify_str(ep_key):
                msg_log.append((
                    MSG_ERR_T,
                    ind_lvl + 1,
                    WM_BAD_K_TYPE.format(ep_key, str, type(ep_key))
                ))
                isbad = True

            if not _verify_str(ep_val):
                msg_log.append((
                    MSG_ERR_T,
                    ind_lvl + 1,
                    WM_BAD_V_TYPE.format(ep_key, type(ep_val))
                ))
                isbad = True

        # check for no errors

        if isbad:
            return

        # otherwise, we can say successful loading!
        msg_log.append((MSG_INFO_T, ind_lvl, WM_SUCCESS))
        save_obj["sub_objects"] = sub_objects
        


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
        store.log = []


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
        #   - and highlights
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
            parsewritelog((MSG_ERR_T, indent_lvl, REQ_MISS.format("pose_map")))
            return

        # move object-based params out of the jobj
        for param_name in OBJ_BASED_PARAM_NAMES:
            if param_name in jobj:
                obj_val = jobj.pop(param_name)

                # objects must be dicts
                if not _verify_dict(obj_val, allow_none=False):
                    parsewritelog((
                        MSG_ERR_T,
                        indent_lvl,
                        BAD_TYPE.format(param_name, dict, type(obj_val))
                    ))
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

        # now for specific params
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
        
            msg_log = []
            _validate_weather_map(
                jobj,
                sp_obj_params,
                obj_based_params,
                msg_log,
                indent_lvl
            )
            if parsewritelogs(msg_log):
                return
             
                                       
                      
                
            msg_log = []
            _validate_sub_objects(
                jobj,
                sp_obj_params,
                obj_based_params,
                msg_log,
                indent_lvl
            )
            
            if parsewritelogs(msg_log):
                return
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

            else:
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

        # back to shared acs/hair/clothes stuff
        msg_log = []
        _validate_ex_props(
            jobj,
            sp_obj_params,
            obj_based_params,
            msg_log,
            indent_lvl
        )
        if parsewritelogs(msg_log):
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
            parsewritelog((
                MSG_WARN_T,
                indent_lvl,
                EXTRA_PROP.format(extra_prop)
            ))

        # no gift/unlock warnings
        if "unlock" in sp_obj_params:
            unlock_hair = sp_obj_params.pop("unlock")
            giftname = None

        elif "giftname" in sp_obj_params:
            giftname = sp_obj_params.pop("giftname")

            # validate gift stuff
            msg_log = []
            _check_giftname(giftname, sp_type, sp_name, msg_log, indent_lvl)
            if parsewritelogs(msg_log):
                return

        elif sp_type != SP_HAIR:
            parsewritelog((MSG_WARN_T, indent_lvl, NO_GIFT))
            giftname = None

        # progpoint processing
        msg_log = []
        _process_progpoint(
            sp_type,
            sp_name,
            sp_obj_params,
            msg_log,
            indent_lvl,
            "entry"
        )
        _process_progpoint(
            sp_type,
            sp_name,
            sp_obj_params,
            msg_log,
            indent_lvl,
            "exit"
        )
        parsewritelogs(msg_log)

        # now we can build the sprites
        try:
            #writelog(str(sp_obj_params))
            if sp_type == SP_ACS:

                if "arm_split" in sp_obj_params:
                    # must be split accessory
                    sp_obj = store.MASSplitAccessory(**sp_obj_params)

                else:
                    # normal accessory
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
                combined_obj_params = sp_obj_params.copy()
                combined_obj_params.update(obj_based_params)
                sp_obj = store.MASDecoration(**combined_obj_params)
                sel_obj_name = "decoration"
                

        except Exception as e:
            # in thise case, we ended up with a duplicate
            writelog(MSG_ERR.format(traceback.format_exc()))
            return

        # check image loadables
        msg_log = []
        
        _test_loadables(sp_obj, msg_log, 0)
        if parsewritelogs(msg_log):
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
