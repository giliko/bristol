'''
bristol -- 20140304.01

+ rm_dcp() modification -- 20140203.01

i.gil@proyecson.com

Añadir gestión de contenidos mediante el parseo del CPL en lugar del PKL

'''

from lxml import etree
from os import path, walk, getcwd

import re, hashlib, base64, shutil, sys

#ASM_NS = "{'bri':'http://www.digicine.com/PROTO-ASDCP-AM-20040311#'}"
#PKL_NS = "{'bri':'http://www.digicine.com/PROTO-ASDCP-PKL-20040311#'}"
#CPL_NS = "{'bri':'http://www.digicine.com/PROTO-ASDCP-CPL-20040511#'}"

ASM_NS = ['http://www.digicine.com/PROTO-ASDCP-AM-20040311#', 'http://www.smpte-ra.org/schemas/429-9/2007/AM']
PKL_NS = ['http://www.digicine.com/PROTO-ASDCP-PKL-20040311#', 'http://www.smpte-ra.org/schemas/429-8/2007/PKL']
CPL_NS = ['http://www.digicine.com/PROTO-ASDCP-CPL-20040511#', 'http://www.smpte-ra.org/schemas/429-7/2006/CPL']
LIB_PATH = '/data/dcps'
LIB_PATH_TMP='/data/tmp'

def f__xml(e):
    l = e.split('.')
    if len(l) > 1:
        return (l[-1:][0].lower() == 'xml')

def hashfile(filepath):
    sha1 = hashlib.sha1()
    f = open(filepath, 'rb')
    try:
        sha1.update(f.readb())
    finally:
        f.close()
    return base64.b64encode(sha1.digest())

class xparser():
    
    def __init__(self, path, ns, tag):
        try:
            self.t = etree.parse(path)
        except:
            raise

	for n in ns:
	  self.h = self.t.xpath('//bri:%s' % tag, namespaces = {'bri':n})
	  if self.h:
	    break

    def first(self):
        if self.h:
            return self.h[0].text
        else:
            return []


class DCP():

    def __init__(self, p = getcwd(), log=None):
        self.root = p
        self.b = False
        self.set_assetmap()
        self.has_error=True
        self.error_message=''
        self.logger=log
        
        #self.logger.info('DCP')
        if hasattr(self, 'am_f'):
            try:
                x = xparser(path.join(self.root, self.am_f), ASM_NS, 'Path')
            
                self.files = [f.text.replace("file:///","") for f in x.h]
                self.xmls = filter(f__xml, self.files)
                self.set_pkl()
                self.set_cpl()
                self.set_title()
                self.set_uuid()
                x = xparser(path.join(self.root, self.pk_f), PKL_NS, 'Size')
                self.size = sum([int(f.text) for f in x.h])
                self.has_error=False
            except IOError as io:
                self.logger.error(str(io.message))
                #self.error_message=io.message
                
            except:
                self.logger.error(str(sys.exc_info()[0]))
                raise            
        else:
            #Can't find assetmap, so it is no error. It is a folder without assetmap.
            self.has_error=False
            
        
            

    def set_assetmap(self):
        am = path.join(self.root, 'ASSETMAP')
        if path.isfile(am):
            self.am_f = am
        else:
            am = am + '.xml'
            if path.isfile(am):
                self.am_f = am

    def set_pkl(self):
        def f__pkl(e):
            try:
                x = xparser(path.join(self.root, e), PKL_NS, 'PackingList')
            except IOError as io:
		self.logger.error(str(io.message))
                raise io
                    
            
            return x.h
        self.pk_f = filter(f__pkl, self.xmls)[0]

    def set_cpl(self):
        def f__cpl(e):
            try:
                x = xparser(path.join(self.root, e), CPL_NS, 'CompositionPlaylist') 
            except IOError as io:
		self.logger.error(str(io.message))
                raise io
            return x.h
        self.cp_f = [] 
        for c in filter(f__cpl, self.xmls):
            try:
                x = xparser(path.join(self.root, c), CPL_NS, 'ContentTitleText')
            except IOError as io:
		self.logger.error(str(io.message))
                raise io
            self.cp_f.append((c, x.first()))
            
    def set_title(self):
        try:
            x = xparser(path.join(self.root, self.pk_f), PKL_NS, 'AnnotationText')
        except IOError as io:
	    self.logger.error(str(io.message))
	    raise io
        self.title = x.first()
        
    def set_uuid(self):
        if not hasattr(self, 'pk_f'):
            self.set_pkl()
        try:
            x = xparser(path.join(self.root, self.pk_f), PKL_NS, 'Id')
        except IOError as io:
	    self.logger.error(str(io.message)) 
	    raise io
        self.uuid = x.first().split(':')[-1:][0]

    def cp_dcp(self, p = LIB_PATH):
        try:
#            shutil.copytree(self.root, path.join(p, self.uuid))
	    self.logger.info('cp_dcp:copying:'+self.uuid);
            shutil.copytree(self.root, path.join(LIB_PATH_TMP, self.uuid))
	    self.logger.info('cp_dcp:moving:'+self.uuid);
            shutil.move(path.join(LIB_PATH_TMP, self.uuid), path.join(p, self.uuid))
            self.logger.info('cp_dcp:ending:'+self.uuid);
            self.b = True
        except IOError as io:
                raise io

    def rm_dcp(self):
	   shutil.rmtree(self.root)
	   self.logger.info('rm_dcp: deleted DCP with title  %s uuid:[%s]' % (self.root, self.uuid));

'''
bristol -- 20140203.01

i.gil@proyecson.com

function rm_dcp() modified not to check if the content has been ingested via the bristol 
library itself i.e. path equals to content uuid

When DCP's are transfered via SmartJog directories non comforming to uuid directory name 
are created. Thus the remove function does nothing since the 'if' condition does not check
    def rm_dcp(self):
        s = path.split(self.root)[1]
        if s == self.uuid:
	    self.logger.info('rm_dcp:deleting:'+self.uuid);
            shutil.rmtree(self.root)
	    self.logger.info('rm_dcp:finishing:'+self.uuid);
	else:
	    self.logger.info('rm_dcp: could not delete %s [%s]' % (self.root, self.uuid));
'''
	
        
class DCPList():
    def __init__(self, p = getcwd(),log=None):
        self.root = p
        self.dirs = []
        self.dcps = []
        self.dcps_w_errors=[] # dcps with errors
        self.logger=log
        #self.logger.info('hola bristol')
        for r, d, f in walk(self.root):
            for name in d:
                dirname = path.join(r,name)
                self.dirs.append(dirname)
        for d in self.dirs:
            
           
            dcp = DCP(d,self.logger)
            if (hasattr(dcp, 'am_f') and dcp.has_error==False):
                                
                self.dcps.append((d, dcp))
                                    
            else:
                if(dcp!=None):  
                    if(dcp.has_error==False):
                        continue
                    pair=[]
                    if hasattr(self, 'title'):
                        pair.append(dcp.title)
                    else:
                        pair.append('No se ha podido conseguir titulo')
                    if hasattr(self, 'uuid'):
                        pair.append(dcp.uuid)
                    else:
                        pair.append('No se ha podido conseguir uuid')                        
                    pair.append(dcp.root)
                    pair.append(dcp.error_message)
                    self.dcps_w_errors.append(pair)                
             
            
                
