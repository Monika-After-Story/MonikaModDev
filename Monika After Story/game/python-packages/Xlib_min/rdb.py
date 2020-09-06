_F='*font'
_E='*foreground'
_D='*background'
_C='\n'
_B='.display'
_A='\\'
import re,sys
from .support import lock
comment_re=re.compile('^\\s*!')
resource_spec_re=re.compile('^\\s*([-_a-zA-Z0-9?.*]+)\\s*:\\s*(.*)$')
value_escape_re=re.compile('\\\\([ \tn\\\\]|[0-7]{3,3})')
resource_parts_re=re.compile('([.*]+)')
NAME_MATCH=0
CLASS_MATCH=2
WILD_MATCH=4
MATCH_SKIP=6
class OptionError(Exception):0
class ResourceDB(object):
	def __init__(A,file=None,string=None,resources=None):
		C=resources;B=string;A.db={};A.lock=lock.allocate_lock()
		if file is not None:A.insert_file(file)
		if B is not None:A.insert_string(B)
		if C is not None:A.insert_resources(C)
	def insert_file(A,file):
		'insert_file(file)\n\n        Load resources entries from FILE, and insert them into the\n        database.  FILE can be a filename (a string)or a file object.\n\n        '
		if type(file)is bytes:file=open(file,'r')
		A.insert_string(file.read())
	def insert_string(H,data):
		'insert_string(data)\n\n        Insert the resources entries in the string DATA into the\n        database.\n\n        ';C=data.split(_C)
		while C:
			A=C[0];del C[0]
			if not A:continue
			if comment_re.match(A):continue
			while A[-1]==_A:
				if C:A=A[:-1]+C[0];del C[0]
				else:A=A[:-1];break
			G=resource_spec_re.match(A)
			if not G:continue
			I,D=G.group(1,2);B=value_escape_re.split(D)
			for E in range(1,len(B),2):
				F=B[E]
				if len(F)==3:B[E]=chr(int(F,8))
				elif F=='n':B[E]=_C
			B[-1]=B[-1].rstrip();D=''.join(B);H.insert(I,D)
	def insert_resources(A,resources):
		'insert_resources(resources)\n\n        Insert all resources entries in the list RESOURCES into the\n        database.  Each element in RESOURCES should be a tuple:\n\n          (resource, value)\n\n        Where RESOURCE is a string and VALUE can be any Python value.\n\n        '
		for (B,C) in resources:A.insert(B,C)
	def insert(D,resource,value):
		'insert(resource, value)\n\n        Insert a resource entry into the database.  RESOURCE is a\n        string and VALUE can be any Python value.\n\n        ';E=value;A=resource_parts_re.split(resource)
		if A[-1]=='':return
		D.lock.acquire();B=D.db
		for C in range(1,len(A),2):
			if A[C-1]not in B:B[A[C-1]]={},{}
			if'*'in A[C]:B=B[A[C-1]][1]
			else:B=B[A[C-1]][0]
		if A[-1]in B:B[A[-1]]=B[A[-1]][:2]+(E,)
		else:B[A[-1]]={},{},E
		D.lock.release()
	def __getitem__(B,keys_tuple):
		'db[name, class]\n\n        Return the value matching the resource identified by NAME and\n        CLASS.  If no match is found, KeyError is raised.\n        ';K='?';F,G=keys_tuple;E=F.split('.');H=G.split('.')
		if len(E)!=len(H):raise ValueError('Different number of parts in resource name/class: %s/%s'%(F,G))
		I=len(E);A=[];B.lock.acquire()
		try:
			if E[0]in B.db:bin_insert(A,_Match((NAME_MATCH,),B.db[E[0]]))
			if H[0]in B.db:bin_insert(A,_Match((CLASS_MATCH,),B.db[H[0]]))
			if K in B.db:bin_insert(A,_Match((WILD_MATCH,),B.db[K]))
			if I==1 and A:
				D=A[0]
				if D.final(I):return D.value()
				else:raise KeyError((F,G))
			if''in B.db:bin_insert(A,_Match((),B.db[''][1]))
			while A:
				D=A[0];del A[0];J=D.match_length()
				for (L,M) in ((E[J],NAME_MATCH),(H[J],CLASS_MATCH),(K,WILD_MATCH)):
					C=D.match(L,M)
					if C:
						if C.final(I):return C.value()
						else:bin_insert(A,C)
					C=D.skip_match(I)
					if C:bin_insert(A,C)
			raise KeyError((F,G))
		finally:B.lock.release()
	def get(A,res,cls,default=None):
		"get(name, class [, default])\n\n        Return the value matching the resource identified by NAME and\n        CLASS.  If no match is found, DEFAULT is returned, or None if\n        DEFAULT isn't specified.\n\n        "
		try:return A[(res,cls)]
		except KeyError:return default
	def update(A,db):'update(db)\n\n        Update this database with all resources entries in the resource\n        database DB.\n\n        ';A.lock.acquire();update_db(A.db,db.db);A.lock.release()
	def output(A):'output()\n\n        Return the resource database in text representation.\n        ';A.lock.acquire();B=output_db('',A.db);A.lock.release();return B
	def getopt(B,name,argv,opts):
		'getopt(name, argv, opts)\n\n        Parse X command line options, inserting the recognised options\n        into the resource database.\n\n        NAME is the application name, and will be prepended to all\n        specifiers.  ARGV is the list of command line arguments,\n        typically sys.argv[1:].\n\n        OPTS is a mapping of options to resource specifiers.  The key is\n        the option flag (with leading -), and the value is an instance of\n        some Option subclass:\n\n        NoArg(specifier, value): set resource to value.\n        IsArg(specifier):        set resource to option itself\n        SepArg(specifier):       value is next argument\n        ResArg:                  resource and value in next argument\n        SkipArg:                 ignore this option and next argument\n        SkipLine:                ignore rest of arguments\n        SkipNArgs(count):        ignore this option and count arguments\n\n        The remaining, non-option, oparguments is returned.\n\n        rdb.OptionError is raised if there is an error in the argument list.\n        ';A=argv
		while A and A[0]and A[0][0]=='-':
			try:A=opts[A[0]].parse(name,B,A)
			except KeyError:raise OptionError('unknown option: %s'%A[0])
			except IndexError:raise OptionError('missing argument to option: %s'%A[0])
		return A
class _Match(object):
	def __init__(A,path,dbs):
		B=dbs;A.path=path
		if type(B)is tuple:A.skip=0;A.group=B
		else:A.skip=1;A.db=B
	def __lt__(A,other):return A.path<other.path
	def __gt__(A,other):return A.path>other.path
	def __eq__(A,other):return A.path==other.path
	def match_length(A):return len(A.path)
	def match(A,part,score):
		C=score;B=part
		if A.skip:
			if B in A.db:return _Match(A.path+(C,),A.db[B])
			else:return None
		elif B in A.group[0]:return _Match(A.path+(C,),A.group[0][B])
		elif B in A.group[1]:return _Match(A.path+(C+1,),A.group[1][B])
		else:return None
	def skip_match(A,complen):
		if len(A.path)+1>=complen:return None
		if A.skip:
			if A.db:return _Match(A.path+(MATCH_SKIP,),A.db)
			else:return None
		elif A.group[1]:return _Match(A.path+(MATCH_SKIP,),A.group[1])
		else:return None
	def final(A,complen):
		if not A.skip and len(A.path)==complen and len(A.group)>2:return 1
		else:return 0
	def value(A):return A.group[2]
def bin_insert(list,element):
	'bin_insert(list, element)\n\n    Insert ELEMENT into LIST.  LIST must be sorted, and ELEMENT will\n    be inserted to that LIST remains sorted.  If LIST already contains\n    ELEMENT, it will not be duplicated.\n\n    ';A=element
	if not list:list.append(A);return
	D=0;B=len(list)-1
	while D<=B:
		C=(D+B)//2
		if A<list[C]:B=C-1
		elif A>list[C]:D=C+1
		elif A==list[C]:return
	if A<list[B]:list.insert(B,A)
	elif A>list[B]:list.insert(B+1,A)
def update_db(dest,src):
	A=dest
	for (B,C) in src.items():
		if B in A:
			update_db(A[B][0],C[0]);update_db(A[B][1],C[1])
			if len(C)>2:A[B]=A[B][:2]+C[2:]
		else:A[B]=copy_group(C)
def copy_group(group):A=group;return(copy_db(A[0]),copy_db(A[1]))+A[2:]
def copy_db(db):
	A={}
	for (B,C) in db.items():A[B]=copy_group(C)
	return A
def output_db(prefix,db):
	C=prefix;A=''
	for (D,B) in db.items():
		if len(B)>2:A=A+'%s%s: %s\n'%(C,D,output_escape(B[2]))
		A=A+output_db(C+D+'.',B[0]);A=A+output_db(C+D+'*',B[1])
	return A
def output_escape(value):
	D=' \t';A=value;A=str(A)
	if not A:return A
	for (B,C) in ((_A,'\\\\'),('\x00','\\000'),(_C,'\\n')):A=A.replace(B,C)
	if A[0]in D:A=_A+A
	if A[-1]in D and A[-2:-1]!=_A:A=A[:-1]+_A+A[-1]
	return A
class Option(object):
	def __init__(A):0
	def parse(A,name,db,args):0
class NoArg(Option):
	'Value is provided to constructor.'
	def __init__(A,specifier,value):A.specifier=specifier;A.value=value
	def parse(A,name,db,args):db.insert(name+A.specifier,A.value);return args[1:]
class IsArg(Option):
	'Value is the option string itself.'
	def __init__(A,specifier):A.specifier=specifier
	def parse(A,name,db,args):db.insert(name+A.specifier,args[0]);return args[1:]
class SepArg(Option):
	'Value is the next argument.'
	def __init__(A,specifier):A.specifier=specifier
	def parse(A,name,db,args):db.insert(name+A.specifier,args[1]);return args[2:]
class ResArgClass(Option):
	'Resource and value in the next argument.'
	def parse(A,name,db,args):db.insert_string(args[1]);return args[2:]
ResArg=ResArgClass()
class SkipArgClass(Option):
	'Ignore this option and next argument.'
	def parse(A,name,db,args):return args[2:]
SkipArg=SkipArgClass()
class SkipLineClass(Option):
	'Ignore rest of the arguments.'
	def parse(A,name,db,args):return[]
SkipLine=SkipLineClass()
class SkipNArgs(Option):
	'Ignore this option and the next COUNT arguments.'
	def __init__(A,count):A.count=count
	def parse(A,name,db,args):return args[1+A.count:]
def get_display_opts(options,argv=sys.argv):
	'display, name, db, args = get_display_opts(options, [argv])\n\n    Parse X OPTIONS from ARGV (or sys.argv if not provided).\n\n    Connect to the display specified by a *.display resource if one is\n    set, or to the default X display otherwise.  Extract the\n    RESOURCE_MANAGER property and insert all resources from ARGV.\n\n    The four return values are:\n      DISPLAY -- the display object\n      NAME    -- the application name (the filname of ARGV[0])\n      DB      -- the created resource database\n      ARGS    -- any remaining arguments\n    ';from Xlib import display as H,Xatom as C;import os;A=os.path.splitext(os.path.basename(argv[0]))[0];B=ResourceDB();I=B.getopt(A,argv[1:],options);J=B.get(A+_B,A+'.Display',None);D=H.Display(J);E=D.screen(0).root.get_full_property(C.RESOURCE_MANAGER,C.STRING)
	if E:F=E.value
	else:F=None
	G=ResourceDB(string=F);G.update(B);return D,A,G,I
stdopts={'-bg':SepArg(_D),'-background':SepArg(_D),'-fg':SepArg(_E),'-foreground':SepArg(_E),'-fn':SepArg(_F),'-font':SepArg(_F),'-name':SepArg('.name'),'-title':SepArg('.title'),'-synchronous':NoArg('*synchronous','on'),'-xrm':ResArg,'-display':SepArg(_B),'-d':SepArg(_B)}