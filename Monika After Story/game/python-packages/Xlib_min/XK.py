_A='XK_'
from Xlib.X import NoSymbol
def string_to_keysym(keysym):"Return the (16 bit) numeric code of keysym.\n\n    Given the name of a keysym as a string, return its numeric code.\n    Don't include the 'XK_' prefix, just use the base, i.e. 'Delete'\n    instead of 'XK_Delete'.";return globals().get(_A+keysym,NoSymbol)
def load_keysym_group(group):
	"Load all the keysyms in group.\n\n    Given a group name such as 'latin1' or 'katakana' load the keysyms\n    defined in module 'Xlib.keysymdef.group-name' into this XK module."
	if'.'in group:raise ValueError('invalid keysym group name: %s'%group)
	G=globals();mod=__import__('Xlib.keysymdef.%s'%group,G,locals(),[group]);keysyms=[n for n in dir(mod)if n.startswith(_A)]
	for keysym in keysyms:G[keysym]=mod.__dict__[keysym]
	del mod
def _load_keysyms_into_XK(mod):'keysym definition modules need no longer call Xlib.XK._load_keysyms_into_XK().\n    You should remove any calls to that function from your keysym modules.'
load_keysym_group('miscellany')
load_keysym_group('latin1')
def keysym_to_string(keysym):
	'Translate a keysym (16 bit number) into a python string.\n\n    This will pass 0 to 0xff as well as XK_BackSpace, XK_Tab, XK_Clear,\n    XK_Return, XK_Pause, XK_Scroll_Lock, XK_Escape, XK_Delete. For other\n    values it returns None.'
	if keysym&65280==0:return chr(keysym&255)
	if keysym in[XK_BackSpace,XK_Tab,XK_Clear,XK_Return,XK_Pause,XK_Scroll_Lock,XK_Escape,XK_Delete]:return chr(keysym&255)
	return None