_G='min_width'
_F='max_width'
_E='min_height'
_D='height_inc'
_C='max_height'
_B='width_inc'
_A='flags'
from Xlib import X,Xutil
from Xlib.protocol import rq
Aspect=rq.Struct(rq.Int32('num'),rq.Int32('denum'))
WMNormalHints=rq.Struct(rq.Card32(_A),rq.Pad(16),rq.Int32(_G,default=0),rq.Int32(_E,default=0),rq.Int32(_F,default=0),rq.Int32(_C,default=0),rq.Int32(_B,default=0),rq.Int32(_D,default=0),rq.Object('min_aspect',Aspect,default=(0,0)),rq.Object('max_aspect',Aspect,default=(0,0)),rq.Int32('base_width',default=0),rq.Int32('base_height',default=0),rq.Int32('win_gravity',default=0))
WMHints=rq.Struct(rq.Card32(_A),rq.Card32('input',default=0),rq.Set('initial_state',4,(Xutil.WithdrawnState,Xutil.NormalState,Xutil.IconicState),default=Xutil.NormalState),rq.Pixmap('icon_pixmap',default=0),rq.Window('icon_window',default=0),rq.Int32('icon_x',default=0),rq.Int32('icon_y',default=0),rq.Pixmap('icon_mask',default=0),rq.Window('window_group',default=0))
WMState=rq.Struct(rq.Set('state',4,(Xutil.WithdrawnState,Xutil.NormalState,Xutil.IconicState)),rq.Window('icon',(X.NONE,)))
WMIconSize=rq.Struct(rq.Card32(_G),rq.Card32(_E),rq.Card32(_F),rq.Card32(_C),rq.Card32(_B),rq.Card32(_D))