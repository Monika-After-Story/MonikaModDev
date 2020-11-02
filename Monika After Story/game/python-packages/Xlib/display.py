_I='resource'
_H='cursor'
_G='drawable'
_F='gc'
_E='fontable'
_D='colormap'
_C='pixmap'
_B='window'
_A='font'
import types
from six import create_unbound_method
from .  import error
from .  import ext
from .  import X
from .protocol import display as protocol_display
from .protocol import request,event,rq
from .xobject import resource
from .xobject import drawable
from .xobject import fontable
from .xobject import colormap
from .xobject import cursor
_resource_baseclasses={_I:resource.Resource,_G:drawable.Drawable,_B:drawable.Window,_C:drawable.Pixmap,_E:fontable.Fontable,_A:fontable.Font,_F:fontable.GC,_D:colormap.Colormap,_H:cursor.Cursor}
_resource_hierarchy={_I:(_G,_B,_C,_E,_A,_F,_D,_H),_G:(_B,_C),_E:(_A,_F)}
class _BaseDisplay(protocol_display.Display):
	def __init__(A,*B,**C):A.resource_classes=_resource_baseclasses.copy();protocol_display.Display.__init__(A,*B,**C);A._atom_cache={}
	def get_atom(A,atomname,only_if_exists=0):
		B=atomname
		if B in A._atom_cache:return A._atom_cache[B]
		C=request.InternAtom(display=A,name=B,only_if_exists=only_if_exists)
		if C.atom!=X.NONE:A._atom_cache[B]=C.atom
		return C.atom
class Display(object):
	def __init__(A,display=None):
		A.display=_BaseDisplay(display);A._keymap_codes=[()]*256;A._keymap_syms={};A._update_keymap(A.display.info.min_keycode,A.display.info.max_keycode-A.display.info.min_keycode+1);A.keysym_translations={};A.extensions=[];A.class_extension_dicts={};A.display_extension_methods={};A.extension_event=rq.DictWrapper({});H=A.list_extensions()
		for (B,D) in ext.__extensions__:
			if B in H:__import__('Xlib.ext.'+D);I=getattr(ext,D);E=A.query_extension(B);A.display.set_extension_major(B,E.major_opcode);I.init(A,E);A.extensions.append(B)
		for (F,J) in A.class_extension_dicts.items():G=A.display.resource_classes[F];A.display.resource_classes[F]=type(G.__name__,(G,),J)
		for C in A.display.info.roots:C.root=A.display.resource_classes[_B](A.display,C.root.id);C.default_colormap=A.display.resource_classes[_D](A.display,C.default_colormap.id)
	def get_display_name(A):'Returns the name used to connect to the server, either\n        provided when creating the Display object, or fetched from the\n        environmental variable $DISPLAY.';return A.display.get_display_name()
	def fileno(A):'Returns the file descriptor number of the underlying socket.\n        This method is provided to allow Display objects to be passed\n        select.select().';return A.display.fileno()
	def close(A):'Close the display, freeing the resources that it holds.';A.display.close()
	def set_error_handler(A,handler):'Set the default error handler which will be called for all\n        unhandled errors. handler should take two arguments as a normal\n        request error handler, but the second argument (the request) will\n        be None.  See section Error Handling.';A.display.set_error_handler(handler)
	def flush(A):'Flush the request queue, building and sending the queued\n        requests. This can be necessary in applications that never wait\n        for events, and in threaded applications.';A.display.flush()
	def sync(A):'Flush the queue and wait until the server has processed all\n        the queued requests. Use this e.g. when it is important that\n        errors caused by a certain request is trapped.';A.get_pointer_control()
	def next_event(A):'Return the next event. If there are no events queued, it will\n        block until the next event is fetched from the server.';return A.display.next_event()
	def pending_events(A):'Return the number of events queued, i.e. the number of times\n        that Display.next_event() can be called without blocking.';return A.display.pending_events()
	def has_extension(A,extension):'Check if both the server and the client library support the X\n        extension named extension.';return extension in A.extensions
	def create_resource_object(A,type,id):'Create a resource object of type for the integer id. type\n        should be one of the following strings:\n\n        resource\n        drawable\n        window\n        pixmap\n        fontable\n        font\n        gc\n        colormap\n        cursor\n\n        This function can be used when a resource ID has been fetched\n        e.g. from an resource or a command line argument. Resource\n        objects should never be created by instantiating the appropriate\n        class directly, since any X extensions dynamically added by the\n        library will not be available.\n        ';return A.display.resource_classes[type](A.display,id)
	def __getattr__(A,attr):
		try:B=A.display_extension_methods[attr];return types.MethodType(B,A)
		except KeyError:raise AttributeError(attr)
	def screen(A,sno=None):
		if sno is None:return A.display.info.roots[A.display.default_screen]
		else:return A.display.info.roots[sno]
	def screen_count(A):'Return the total number of screens on the display.';return len(A.display.info.roots)
	def get_default_screen(A):'Return the number of the default screen, extracted from the\n        display name.';return A.display.get_default_screen()
	def extension_add_method(B,object,name,function):
		"extension_add_method(object, name, function)\n\n        Add an X extension module method.  OBJECT is the type of\n        object to add the function to, a string from this list:\n\n            display\n            resource\n            drawable\n            window\n            pixmap\n            fontable\n            font\n            gc\n            colormap\n            cursor\n\n        NAME is the name of the method, a string.  FUNCTION is a\n        normal function whose first argument is a 'self'.\n        ";D=function;A=name
		if object=='display':
			if hasattr(B,A):raise AssertionError('attempting to replace display method: %s'%A)
			B.display_extension_methods[A]=D
		else:
			G=(object,)+_resource_hierarchy.get(object,())
			for C in G:
				E=_resource_baseclasses[C]
				if hasattr(E,A):raise AssertionError('attempting to replace %s method: %s'%(C,A))
				F=create_unbound_method(D,E)
				try:B.class_extension_dicts[C][A]=F
				except KeyError:B.class_extension_dicts[C]={A:F}
	def extension_add_event(D,code,evt,name=None):
		'extension_add_event(code, evt, [name])\n\n        Add an extension event.  CODE is the numeric code, and EVT is\n        the event class.  EVT will be cloned, and the attribute _code\n        of the new event class will be set to CODE.\n\n        If NAME is omitted, it will be set to the name of EVT.  This\n        name is used to insert an entry in the DictWrapper\n        extension_event.\n        ';C=name;B=code;A=evt;E=type(A.__name__,A.__bases__,A.__dict__.copy());E._code=B;D.display.add_extension_event(B,E)
		if C is None:C=A.__name__
		setattr(D.extension_event,C,B)
	def extension_add_subevent(D,code,subcode,evt,name=None):
		'extension_add_subevent(code, evt, [name])\n\n        Add an extension subevent.  CODE is the numeric code, subcode\n        is the sub-ID of this event that shares the code ID with other\n        sub-events and EVT is the event class.  EVT will be cloned, and\n        the attribute _code of the new event class will be set to CODE.\n\n        If NAME is omitted, it will be set to the name of EVT.  This\n        name is used to insert an entry in the DictWrapper\n        extension_event.\n        ';E=subcode;C=name;B=code;A=evt;F=type(A.__name__,A.__bases__,A.__dict__.copy());F._code=B;D.display.add_extension_event(B,F,E)
		if C is None:C=A.__name__
		setattr(D.extension_event,C,(B,E))
	def add_extension_error(A,code,err):'add_extension_error(code, err)\n\n        Add an extension error.  CODE is the numeric code, and ERR is\n        the error class.\n        ';A.display.add_extension_error(code,err)
	def keycode_to_keysym(A,keycode,index):
		'Convert a keycode to a keysym, looking in entry index.\n        Normally index 0 is unshifted, 1 is shifted, 2 is alt grid, and 3\n        is shift+alt grid. If that key entry is not bound, X.NoSymbol is\n        returned.'
		try:return A._keymap_codes[keycode][index]
		except IndexError:return X.NoSymbol
	def keysym_to_keycode(A,keysym):
		'Look up the primary keycode that is bound to keysym. If\n        several keycodes are found, the one with the lowest index and\n        lowest code is returned. If keysym is not bound to any key, 0 is\n        returned.'
		try:return A._keymap_syms[keysym][0][1]
		except (KeyError,IndexError):return 0
	def keysym_to_keycodes(A,keysym):
		'Look up all the keycodes that is bound to keysym. A list of\n        tuples (keycode, index) is returned, sorted primarily on the\n        lowest index and secondarily on the lowest keycode.'
		try:return map(lambda x:(x[1],x[0]),A._keymap_syms[keysym])
		except KeyError:return[]
	def refresh_keyboard_mapping(B,evt):
		'This method should be called once when a MappingNotify event\n        is received, to update the keymap cache. evt should be the event\n        object.';A=evt
		if isinstance(A,event.MappingNotify):
			if A.request==X.MappingKeyboard:B._update_keymap(A.first_keycode,A.count)
		else:raise TypeError('expected a MappingNotify event')
	def _update_keymap(B,first_keycode,count):
		'Internal function, called to refresh the keymap cache.\n        ';H=count;C=first_keycode;I=C+H
		for (M,G) in B._keymap_syms.items():
			D=0
			while D<len(G):
				A=G[D][1]
				if A>=C and A<I:del G[D]
				else:D=D+1
		J=B.get_keyboard_mapping(C,H);B._keymap_codes[C:I]=J;A=C
		for L in J:
			E=0
			for F in L:
				if F!=X.NoSymbol:
					if F in B._keymap_syms:K=B._keymap_syms[F];K.append((E,A));K.sort()
					else:B._keymap_syms[F]=[(E,A)]
				E=E+1
			A=A+1
	def lookup_string(C,keysym):
		'Return a string corresponding to KEYSYM, or None if no\n        reasonable translation is found.\n        ';A=keysym;B=C.keysym_translations.get(A)
		if B is not None:return B
		import Xlib.XK;return Xlib.XK.keysym_to_string(A)
	def rebind_string(A,keysym,newstring):
		'Change the translation of KEYSYM to NEWSTRING.\n        If NEWSTRING is None, remove old translation if any.\n        ';C=newstring;B=keysym
		if C is None:
			try:del A.keysym_translations[B]
			except KeyError:pass
		else:A.keysym_translations[B]=C
	def intern_atom(A,name,only_if_exists=0):'Intern the string name, returning its atom number. If\n        only_if_exists is true and the atom does not already exist, it\n        will not be created and X.NONE is returned.';B=request.InternAtom(display=A.display,name=name,only_if_exists=only_if_exists);return B.atom
	def get_atom(A,atom,only_if_exists=0):'Alias for intern_atom, using internal cache';return A.display.get_atom(atom,only_if_exists)
	def get_atom_name(A,atom):'Look up the name of atom, returning it as a string. Will raise\n        BadAtom if atom does not exist.';B=request.GetAtomName(display=A.display,atom=atom);return B.name
	def get_selection_owner(A,selection):'Return the window that owns selection (an atom), or X.NONE if\n        there is no owner for the selection. Can raise BadAtom.';B=request.GetSelectionOwner(display=A.display,selection=selection);return B.owner
	def send_event(A,destination,event,event_mask=0,propagate=0,onerror=None):'Send a synthetic event to the window destination which can be\n        a window object, or X.PointerWindow or X.InputFocus. event is the\n        event object to send, instantiated from one of the classes in\n        protocol.events. See XSendEvent(3X11) for details.\n\n        There is also a Window.send_event() method.';request.SendEvent(display=A.display,onerror=onerror,propagate=propagate,destination=destination,event_mask=event_mask,event=event)
	def ungrab_pointer(A,time,onerror=None):'Release a grabbed pointer and any queued events. See\n        XUngrabPointer(3X11).';request.UngrabPointer(display=A.display,onerror=onerror,time=time)
	def change_active_pointer_grab(A,event_mask,cursor,time,onerror=None):'Change the dynamic parameters of a pointer grab. See\n        XChangeActivePointerGrab(3X11).';request.ChangeActivePointerGrab(display=A.display,onerror=onerror,cursor=cursor,time=time,event_mask=event_mask)
	def ungrab_keyboard(A,time,onerror=None):'Ungrab a grabbed keyboard and any queued events. See\n        XUngrabKeyboard(3X11).';request.UngrabKeyboard(display=A.display,onerror=onerror,time=time)
	def allow_events(A,mode,time,onerror=None):'Release some queued events. mode should be one of\n        X.AsyncPointer, X.SyncPointer, X.AsyncKeyboard, X.SyncKeyboard,\n        X.ReplayPointer, X.ReplayKeyboard, X.AsyncBoth, or X.SyncBoth.\n        time should be a timestamp or X.CurrentTime.';request.AllowEvents(display=A.display,onerror=onerror,mode=mode,time=time)
	def grab_server(A,onerror=None):'Disable processing of requests on all other client connections\n        until the server is ungrabbed. Server grabbing should be avoided\n        as much as possible.';request.GrabServer(display=A.display,onerror=onerror)
	def ungrab_server(A,onerror=None):'Release the server if it was previously grabbed by this client.';request.UngrabServer(display=A.display,onerror=onerror)
	def warp_pointer(A,x,y,src_window=X.NONE,src_x=0,src_y=0,src_width=0,src_height=0,onerror=None):'Move the pointer relative its current position by the offsets\n        (x, y). However, if src_window is a window the pointer is only\n        moved if the specified rectangle in src_window contains it. If\n        src_width is 0 it will be replaced with the width of src_window -\n        src_x. src_height is treated in a similar way.\n\n        To move the pointer to absolute coordinates, use Window.warp_pointer().';request.WarpPointer(display=A.display,onerror=onerror,src_window=src_window,dst_window=X.NONE,src_x=src_x,src_y=src_y,src_width=src_width,src_height=src_height,dst_x=x,dst_y=y)
	def set_input_focus(A,focus,revert_to,time,onerror=None):'Set input focus to focus, which should be a window,\n        X.PointerRoot or X.NONE. revert_to specifies where the focus\n        reverts to if the focused window becomes not visible, and should\n        be X.RevertToParent, RevertToPointerRoot, or RevertToNone. See\n        XSetInputFocus(3X11) for details.\n\n        There is also a Window.set_input_focus().';request.SetInputFocus(display=A.display,onerror=onerror,revert_to=revert_to,focus=focus,time=time)
	def get_input_focus(A):'Return an object with the following attributes:\n\n        focus\n            The window which currently holds the input\n            focus, X.NONE or X.PointerRoot.\n        revert_to\n            Where the focus will revert, one of X.RevertToParent,\n            RevertToPointerRoot, or RevertToNone. ';return request.GetInputFocus(display=A.display)
	def query_keymap(A):'Return a bit vector for the logical state of the keyboard,\n        where each bit set to 1 indicates that the corresponding key is\n        currently pressed down. The vector is represented as a list of 32\n        integers. List item N contains the bits for keys 8N to 8N + 7\n        with the least significant bit in the byte representing key 8N.';B=request.QueryKeymap(display=A.display);return B.map
	def open_font(A,name):
		'Open the font identifed by the pattern name and return its\n        font object. If name does not match any font, None is returned.';B=A.display.allocate_resource_id();C=error.CatchError(error.BadName);request.OpenFont(display=A.display,onerror=C,fid=B,name=name);A.sync()
		if C.get_error():A.display.free_resource_id(B);return None
		else:D=A.display.get_resource_class(_A,fontable.Font);return D(A.display,B,owner=1)
	def list_fonts(A,pattern,max_names):'Return a list of font names matching pattern. No more than\n        max_names will be returned.';B=request.ListFonts(display=A.display,max_names=max_names,pattern=pattern);return B.fonts
	def list_fonts_with_info(A,pattern,max_names):'Return a list of fonts matching pattern. No more than\n        max_names will be returned. Each list item represents one font\n        and has the following properties:\n\n        name\n            The name of the font.\n        min_bounds\n        max_bounds\n        min_char_or_byte2\n        max_char_or_byte2\n        default_char\n        draw_direction\n        min_byte1\n        max_byte1\n        all_chars_exist\n        font_ascent\n        font_descent\n        replies_hint\n            See the description of XFontStruct in XGetFontProperty(3X11)\n            for details on these values.\n        properties\n            A list of properties. Each entry has two attributes:\n\n            name\n                The atom identifying this property.\n            value\n                A 32-bit unsigned value.\n        ';return request.ListFontsWithInfo(display=A.display,max_names=max_names,pattern=pattern)
	def set_font_path(A,path,onerror=None):'Set the font path to path, which should be a list of strings.\n        If path is empty, the default font path of the server will be\n        restored.';request.SetFontPath(display=A.display,onerror=onerror,path=path)
	def get_font_path(A):'Return the current font path as a list of strings.';B=request.GetFontPath(display=A.display);return B.paths
	def query_extension(B,name):
		'Ask the server if it supports the extension name. If it is\n        supported an object with the following attributes is returned:\n\n        major_opcode\n            The major opcode that the requests of this extension uses.\n        first_event\n            The base event code if the extension have additional events, or 0.\n        first_error\n            The base error code if the extension have additional errors, or 0.\n\n        If the extension is not supported, None is returned.';A=request.QueryExtension(display=B.display,name=name)
		if A.present:return A
		else:return None
	def list_extensions(A):'Return a list of all the extensions provided by the server.';B=request.ListExtensions(display=A.display);return B.names
	def change_keyboard_mapping(A,first_keycode,keysyms,onerror=None):'Modify the keyboard mapping, starting with first_keycode.\n        keysyms is a list of tuples of keysyms. keysyms[n][i] will be\n        assigned to keycode first_keycode+n at index i.';request.ChangeKeyboardMapping(display=A.display,onerror=onerror,first_keycode=first_keycode,keysyms=keysyms)
	def get_keyboard_mapping(A,first_keycode,count):'Return the current keyboard mapping as a list of tuples,\n        starting at first_keycount and no more than count.';B=request.GetKeyboardMapping(display=A.display,first_keycode=first_keycode,count=count);return B.keysyms
	def change_keyboard_control(B,onerror=None,**A):'Change the parameters provided as keyword arguments:\n\n        key_click_percent\n            The volume of key clicks between 0 (off) and 100 (load).\n            -1 will restore default setting.\n        bell_percent\n            The base volume of the bell, coded as above.\n        bell_pitch\n            The pitch of the bell in Hz, -1 restores the default.\n        bell_duration\n            The duration of the bell in milliseconds, -1 restores\n            the default.\n        led\n\n        led_mode\n            led_mode should be X.LedModeOff or X.LedModeOn. If led is\n            provided, it should be a 32-bit mask listing the LEDs that\n            should change. If led is not provided, all LEDs are changed.\n        key\n\n        auto_repeat_mode\n            auto_repeat_mode should be one of X.AutoRepeatModeOff,\n            X.AutoRepeatModeOn, or X.AutoRepeatModeDefault. If key is\n            provided, that key will be modified, otherwise the global\n            state for the entire keyboard will be modified.';request.ChangeKeyboardControl(display=B.display,onerror=onerror,attrs=A)
	def get_keyboard_control(A):'Return an object with the following attributes:\n\n        global_auto_repeat\n            X.AutoRepeatModeOn or X.AutoRepeatModeOff.\n\n        auto_repeats\n            A list of 32 integers. List item N contains the bits for keys\n            8N to 8N + 7 with the least significant bit in the byte\n            representing key 8N. If a bit is on, autorepeat is enabled\n            for the corresponding key.\n\n        led_mask\n            A 32-bit mask indicating which LEDs are on.\n\n        key_click_percent\n            The volume of key click, from 0 to 100.\n\n        bell_percent\n\n        bell_pitch\n\n        bell_duration\n            The volume, pitch and duration of the bell. ';return request.GetKeyboardControl(display=A.display)
	def bell(A,percent=0,onerror=None):'Ring the bell at the volume percent which is relative the base\n        volume. See XBell(3X11).';request.Bell(display=A.display,onerror=onerror,percent=percent)
	def change_pointer_control(G,accel=None,threshold=None,onerror=None):
		'To change the pointer acceleration, set accel to a tuple (num,\n        denum). The pointer will then move num/denum times the normal\n        speed if it moves beyond the threshold number of pixels at once.\n        To change the threshold, set it to the number of pixels. -1\n        restores the default.';B=threshold;A=accel
		if A is None:C=0;D=0;E=0
		else:C=1;D,E=A
		if B is None:F=0
		else:F=1
		request.ChangePointerControl(display=G.display,onerror=onerror,do_accel=C,do_thresh=F,accel_num=D,accel_denum=E,threshold=B)
	def get_pointer_control(A):'Return an object with the following attributes:\n\n        accel_num\n\n        accel_denom\n            The acceleration as numerator/denumerator.\n\n        threshold\n            The number of pixels the pointer must move before the\n            acceleration kicks in.';return request.GetPointerControl(display=A.display)
	def set_screen_saver(A,timeout,interval,prefer_blank,allow_exposures,onerror=None):'See XSetScreenSaver(3X11).';request.SetScreenSaver(display=A.display,onerror=onerror,timeout=timeout,interval=interval,prefer_blank=prefer_blank,allow_exposures=allow_exposures)
	def get_screen_saver(A):'Return an object with the attributes timeout, interval,\n        prefer_blanking, allow_exposures. See XGetScreenSaver(3X11) for\n        details.';return request.GetScreenSaver(display=A.display)
	def change_hosts(A,mode,host_family,host,onerror=None):'mode is either X.HostInsert or X.HostDelete. host_family is\n        one of X.FamilyInternet, X.FamilyDECnet or X.FamilyChaos.\n\n        host is a list of bytes. For the Internet family, it should be the\n        four bytes of an IPv4 address.';request.ChangeHosts(display=A.display,onerror=onerror,mode=mode,host_family=host_family,host=host)
	def list_hosts(A):'Return an object with the following attributes:\n\nmode\n    X.EnableAccess if the access control list is used, X.DisableAccess otherwise.\nhosts\n    The hosts on the access list. Each entry has the following attributes:\n\n    family\n        X.FamilyInternet, X.FamilyDECnet, or X.FamilyChaos.\n    name\n        A list of byte values, the coding depends on family. For the Internet family, it is the 4 bytes of an IPv4 address.\n\n';return request.ListHosts(display=A.display)
	def set_access_control(A,mode,onerror=None):'Enable use of access control lists at connection setup if mode\n        is X.EnableAccess, disable if it is X.DisableAccess.';request.SetAccessControl(display=A.display,onerror=onerror,mode=mode)
	def set_close_down_mode(A,mode,onerror=None):"Control what will happen with the client's resources at\n        connection close. The default is X.DestroyAll, the other values\n        are X.RetainPermanent and X.RetainTemporary.";request.SetCloseDownMode(display=A.display,onerror=onerror,mode=mode)
	def force_screen_saver(A,mode,onerror=None):'If mode is X.ScreenSaverActive the screen saver is activated.\n        If it is X.ScreenSaverReset, the screen saver is deactivated as\n        if device input had been received.';request.ForceScreenSaver(display=A.display,onerror=onerror,mode=mode)
	def set_pointer_mapping(A,map):'Set the mapping of the pointer buttons. map is a list of\n        logical button numbers. map must be of the same length as the\n        list returned by Display.get_pointer_mapping().\n\n        map[n] sets the\n        logical number for the physical button n+1. Logical number 0\n        disables the button. Two physical buttons cannot be mapped to the\n        same logical number.\n\n        If one of the buttons to be altered are\n        logically in the down state, X.MappingBusy is returned and the\n        mapping is not changed. Otherwise the mapping is changed and\n        X.MappingSuccess is returned.';B=request.SetPointerMapping(display=A.display,map=map);return B.status
	def get_pointer_mapping(A):'Return a list of the pointer button mappings. Entry N in the\n        list sets the logical button number for the physical button N+1.';B=request.GetPointerMapping(display=A.display);return B.map
	def set_modifier_mapping(A,keycodes):'Set the keycodes for the eight modifiers X.Shift, X.Lock,\n        X.Control, X.Mod1, X.Mod2, X.Mod3, X.Mod4 and X.Mod5. keycodes\n        should be a eight-element list where each entry is a list of the\n        keycodes that should be bound to that modifier.\n\n        If any changed\n        key is logically in the down state, X.MappingBusy is returned and\n        the mapping is not changed. If the mapping violates some server\n        restriction, X.MappingFailed is returned. Otherwise the mapping\n        is changed and X.MappingSuccess is returned.';B=request.SetModifierMapping(display=A.display,keycodes=keycodes);return B.status
	def get_modifier_mapping(A):'Return a list of eight lists, one for each modifier. The list\n        can be indexed using X.ShiftMapIndex, X.Mod1MapIndex, and so on.\n        The sublists list the keycodes bound to that modifier.';B=request.GetModifierMapping(display=A.display);return B.keycodes
	def no_operation(A,onerror=None):'Do nothing but send a request to the server.';request.NoOperation(display=A.display,onerror=onerror)