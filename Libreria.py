#!/usr/bin/env python

import wx
import os
import platform 
import ctypes
from datetime import datetime 
from math import pi
import sys
import logging
import argparse
import time
import operator
import shutil




import RemoveDCPDialog
import bristol
#----------------------------------------------------------------------
# Get Some Icon/Data
#----------------------------------------------------------------------

#LIB_PATH = '/home/bristol'
LIB_PATH_INGESTED = '/data/dcps'
LIB_PATH_INCOMING_TMP = '/data/tmp'
LIB_PATH_INCOMING = '/data/incoming/'
LIB_PATH_INCOMING_WIN = 'c:/virtual-experience'
LIB_PATH_INGESTED_WIN = 'e:/dcps'

from threading import Thread
from wx.lib.pubsub import Publisher
 
 
# determine if application is a script file or frozen exe 
if getattr(sys, 'frozen', False): 
    application_path = os.path.dirname(sys.executable) 
elif __file__: 
    application_path = os.path.dirname(__file__) 
 

    application_path_images=os.path.join(application_path,'images/')
 

########################################################################
class OverWriteDCPDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(400, 286))    
    #def __init__(self, *args, **kwds):
        # begin wxGlade: RemoveDCPDialog.__init__
        #kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        #wx.Dialog.__init__(self, *args, **kwds)
        self.listbox = wx.ListBox(self, -1, choices=[])
        self.label_1 = wx.StaticText(self, -1, "La siguiente lista de DCPS ya esta ingestada. Sobreescribir?")
        self.btSi = wx.Button(self, -1, "Si")
        self.btNo = wx.Button(self, -1, "No")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: RemoveDCPDialog.__set_properties
        self.SetTitle("dialog_1")
        #self.SetSize((400, 286))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: RemoveDCPDialog.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(self.listbox, 2, wx.ALL | wx.EXPAND, 10)
        sizer_1.Add(self.label_1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 3)
        sizer_2.Add(self.btSi, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_2.Add(self.btNo, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_1.Add(sizer_2,0,wx.LEFT | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 110)
        self.SetSizer(sizer_1)
        self.Layout()
        self.btSi.Bind(wx.EVT_BUTTON, self.OnButtonSi)
        self.btNo.Bind(wx.EVT_BUTTON, self.OnButtonNo)
        
    def OnButtonSi( self, event ) :
        
        btn = event.GetEventObject()
        self.EndModal(wx.ID_OK)
        return
    def OnButtonNo( self, event ) :
                
        btn = event.GetEventObject()
        self.EndModal(wx.ID_NO)
        return         
        
########################################################################
class RemoveCorrruptedDCPDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(600, 286))    
    #def __init__(self, *args, **kwds):
        # begin wxGlade: RemoveDCPDialog.__init__
        #kwds["style"] = wx.DEFAULT_DIALOG_STYLE
        #wx.Dialog.__init__(self, *args, **kwds)
        self.listbox = wx.ListBox(self, -1, choices=[])
        self.label_1 = wx.StaticText(self, -1, "La siguiente lista de DCPS parece corrupta. Eliminar?")
        self.btSi = wx.Button(self, -1, "Si")
        self.btNo = wx.Button(self, -1, "No")

        self.__set_properties()
        self.__do_layout()
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: RemoveDCPDialog.__set_properties
        self.SetTitle("DCPs Corruptos")
        #self.SetSize((400, 286))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: RemoveDCPDialog.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(self.listbox, 2, wx.ALL | wx.EXPAND, 10)
        sizer_1.Add(self.label_1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 3)
        sizer_2.Add(self.btSi, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_2.Add(self.btNo, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_1.Add(sizer_2,0,wx.LEFT | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL, 110)
        self.SetSizer(sizer_1)
        self.Layout()
        self.btSi.Bind(wx.EVT_BUTTON, self.OnButtonSi)
        self.btNo.Bind(wx.EVT_BUTTON, self.OnButtonNo)
        
    def OnButtonSi( self, event ) :
        
        btn = event.GetEventObject()
        self.EndModal(wx.ID_OK)
        return
    def OnButtonNo( self, event ) :
                
        btn = event.GetEventObject()
        self.EndModal(wx.ID_NO)
        return           

########################################################################
# do the job related to move the dcps
class TestThread(Thread):
    """Test Worker Thread Class."""
 
    #----------------------------------------------------------------------
    def __init__(self,listDCPSindex,listDCPSincoming,logger):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self.listindex=listDCPSindex
        self.listDCPStocopy=listDCPSincoming
        self.log=logger
        self.done=False
        self.cancelled=False
        self.start()    # start the thread
        
        
        
 
    #----------------------------------------------------------------------
    def run(self):
        """Run Worker Thread."""
        # This is the code executing in the new thread.
        for i in range(len(self.listindex)):
        
                       
            if(self.cancelled):
                return
            #wx.CallAfter(self.postTime, self.listDCPStocopy[self.listindex[i]].title)
            self.title=self.listDCPStocopy[self.listindex[i]].title
            self.log.info('Start copy of:'+self.title)
            self.log.info('Copying '+str(self.listindex[i]))
            try:     
                t0=time.time()
                copiado=False
                
                if platform.system() == 'Windows':
                    copiado=self.listDCPStocopy[self.listindex[i]].cp_dcp(LIB_PATH_INGESTED_WIN)
                else:
                    self.log.info('linux')
                    copiado=self.listDCPStocopy[self.listindex[i]].cp_dcp(LIB_PATH_INGESTED)
                t1=time.time()
                if(copiado==False):
                    self.log.error('Error copying the files :copying')
                    error_msg2=str(sys.exc_info()[0])
                    wx.MessageBox('Ha habido un problema con la copia de ficheros/n del contenido '+self.title+'|'+error_msg2, 'Error', wx.OK | wx.ICON_ERROR)
                    continue                    
            except:
                #error_msg=str(sys.exc_info()[0])
                error_msg='Error copiando contenido'
                self.log.error('Error copying the files :'+error_msg)
                wx.MessageBox('Ha habido un problema con la copia de ficheros del contenido '+self.title+'|'+error_msg, 'Error', wx.OK | wx.ICON_ERROR)
                continue
            
            self.log.info('End copy of'+self.title+' Duration:'+str(t1-t0) )
            aux=len(self.listindex)-1            
            if(i<aux ):
                try:
                    self.title=self.listDCPStocopy[self.listindex[i+1]].title
                                         
                    wx.CallAfter(self.postTime, self.listDCPStocopy[self.listindex[i+1]].title)
                    msg=str(i)+'|'+str(len(self.listindex))
                    self.log.info(msg)
                    wx.CallAfter(self.postCount,msg)
                    self.log.info(msg)             
                    
                except:
                    wx.MessageDialog('Ha habido un problema con la copia de ficheros', 'Error', wx.OK | wx.ICON_ERROR)
                    self.log.error('Error copying the files :'+sys.exc_info()[0])
                    self.done=True
            
        #time.sleep(5)
        #print "now go dead??"
        self.done=True        
        wx.CallAfter(self.postTime,"end")
        
        
 
    #----------------------------------------------------------------------
    def postTime(self, title):
        """
        Send time to GUI
        """
        #amtOfTime = (amt + 1) * 10
        Publisher().sendMessage("Update", title)
        
    def postCount(self, msg):
            """
            Send time to GUI
            """
            #amtOfTime = (amt + 1) * 10
            Publisher().sendMessage("UpdateCount", msg)    
        




class DelThread(Thread):
    """Worker Thread Class To delete DCPS."""
 
    #----------------------------------------------------------------------
    def __init__(self,listDCPSindex,listDCPSingested,logger):
        """Init Worker Thread Class."""
        Thread.__init__(self)
        self.listindexdel=listDCPSindex
        self.listDCPStodelete=listDCPSingested
        self.log=logger
        self.start()    # start the thread
        
        
 
    #----------------------------------------------------------------------
    def run(self):
        """Run Worker Thread."""
        # This is the code executing in the new thread.
        for i in range(len(self.listindexdel)):
        
            
            #wx.CallAfter(self.postTime, self.listDCPStocopy[self.listindex[i]].title)
            title=self.listDCPStodelete[self.listindexdel[i]].title
            self.log.info('Start Deleting:['+title+']')
            self.listDCPStodelete[self.listindexdel[i]].rm_dcp()
            self.log.info('End Deleting:['+title+']')
            aux=len(self.listindexdel)-1            
            #if(i<aux):
                #wx.CallAfter(self.postTime, self.listDCPStodelete[self.listindex[i+1]].title)
            
        #time.sleep(5)
        #wx.CallAfter(Publisher().sendMessage,"Update" , "-1")
 
    #----------------------------------------------------------------------
    def postTime(self, title):
        """
        Send time to GUI
        """
        #amtOfTime = (amt + 1) * 10
        Publisher().sendMessage("Update", title)

'''

def GetMondrianData():
   
 return \
'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00 \x00\x00\x00 \x08\x06\x00\
\x00\x00szf4\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\x00\x00qID\
ATX\x85\xed\xd6;\n\x800\x10E\xd1{\xc5\x8d\xb9r\x97\x16\x0b\xad$\x8a\x82:\x16\
o\xda\x84pB2\x1f\x81Fa\x8c\x9c\x08\x04Z{\xcf\xa72\xbcv\xfa\xc5\x08 \x80r\x80\
\xfc\xa2\x0e\x1c\xe4\xba\xfaX\x1d\xd0\xde]S\x07\x02\xd8>\xe1wa-`\x9fQ\xe9\
\x86\x01\x04\x10\x00\\(Dk\x1b-\x04\xdc\x1d\x07\x14\x98;\x0bS\x7f\x7f\xf9\x13\
\x04\x10@\xf9X\xbe\x00\xc9 \x14K\xc1<={\x00\x00\x00\x00IEND\xaeB`\x82' 

def GetMondrianBitmap():
    return wx.BitmapFromImage(GetMondrianImage())

def GetMondrianImage():
    import cStringIO
    stream = cStringIO.StringIO(GetMondrianData())
    return wx.ImageFromStream(stream)

def GetMondrianIcon():
    icon = wx.EmptyIcon()
    icon.CopyFromBitmap(GetMondrianBitmap())
    return icon

'''


#----------------------------------------------------------------------
# Beginning Of PIECTRL Demo wxPython Code
#----------------------------------------------------------------------

class BristolLibrary(wx.Frame):

    def __init__(self, parent, id=wx.ID_ANY, title="", pos=wx.DefaultPosition,
                 size=(600, 450)):

        
        wx.Frame.__init__(self, parent, id, title, pos)#, size)


        #TODO: maximieze without size
        wx.Frame.Maximize(self,True)
        #command for debugging(extra info)
        self.DEBUG=False
        if (len(sys.argv) > 1):
            if( sys.argv[1] == 'D' ):
                self.DEBUG=True        
        
        # create logger with 'spam_application'
        self.logger = logging.getLogger('libreria')
        self.logger.setLevel(logging.DEBUG)
        # create file handler which logs even debug messages
        now = datetime.now()
        filename='libreria-'+now.strftime("%Y-%m-%d %H-%M")+'.log'
        path_log=os.path.join(os.path.join(application_path,'log'))
        if(os.path.exists(path_log)==False):
            os.makedirs(path_log)
        
        fh = logging.FileHandler(os.path.join(path_log,filename))
        fh.setLevel(logging.DEBUG)
        # create formatter and add it to the handlers
        
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        # add the handlers to the logger
        self.logger.addHandler(fh)
        
        self.msgDebug('DEBUGGING')
        
        self.SetMinSize((600,450))
        # Create Some Maquillage For The Demo: Icon, StatusBar, ToolBar, MenuBar...
        
        #toolbar
        self.toolbar=self.CreateToolBar() 
        
        refresh=self.toolbar.AddLabelTool(wx.NewId(),'',wx.Bitmap(os.path.join(application_path_images, 'refresh.png')),wx.NullBitmap,wx.ITEM_NORMAL,'Refrescar a ingestar','Refrescar contenido a ingestar')
        expand_incoming=self.toolbar.AddLabelTool(wx.NewId(),'',wx.Bitmap(os.path.join(application_path_images, 'expand.gif')),wx.NullBitmap,wx.ITEM_NORMAL,'Expandir','Expandir arbol del contenido a ingresar')
        collapse_incoming=self.toolbar.AddLabelTool(wx.NewId(),'',wx.Bitmap(os.path.join(application_path_images, 'collapse.gif')),wx.NullBitmap,wx.ITEM_NORMAL,'Contraer','Contraer arbol del contenido a ingresar')
        
        
        self.toolbar.AddSeparator()
        selectone=self.toolbar.AddLabelTool(wx.NewId(),'',wx.Bitmap(os.path.join(application_path_images, 'one.png')),wx.NullBitmap,wx.ITEM_NORMAL,'Ingestar contenido seleccionado','Ingesta solamente el contenido seleccionado')
        selectall=self.toolbar.AddLabelTool(wx.NewId(),'',wx.Bitmap(os.path.join(application_path_images, 'all.png')),wx.NullBitmap,wx.ITEM_NORMAL,'Ingestar Todo','Ingestar TODO el contenido')
        self.toolbar.AddSeparator()
        delete=self.toolbar.AddLabelTool(wx.NewId(),'',wx.Bitmap(os.path.join(application_path_images, 'delete.png')),wx.NullBitmap,wx.ITEM_NORMAL,'Eliminar contenido','Eliminar contenido Seleccionado (de lo ya ingestado)')
        refresh2=self.toolbar.AddLabelTool(wx.NewId(),'',wx.Bitmap(os.path.join(application_path_images, 'refresh.png')),wx.NullBitmap,wx.ITEM_NORMAL,'Refrescar ingestado','Refrescar contenido ya ingestado')
        expand_ingested=self.toolbar.AddLabelTool(wx.NewId(),'',wx.Bitmap(os.path.join(application_path_images, 'expand.gif')),wx.NullBitmap,wx.ITEM_NORMAL,'Expandir','Expandir arbol del contenido ingestado')
        collapse_ingested=self.toolbar.AddLabelTool(wx.NewId(),'',wx.Bitmap(os.path.join(application_path_images, 'collapse.gif')),wx.NullBitmap,wx.ITEM_NORMAL,'Contraer','Contraer arbol del contenido ingestado')
        
        self.toolbar.Realize()
        
        
        self.statusbar = self.CreateStatusBar(2, wx.ST_SIZEGRIP)

        self.statusbar.SetStatusWidths([-2, -1])
        
        statusbar_fields = [("DCPLibrary por Proyecson"),
                            ("Proyecson S.A. 2013")]
        
        for i in range(len(statusbar_fields)):
            self.statusbar.SetStatusText(statusbar_fields[i], i)
        
        self.SetMenuBar(self.CreateMenuBar())

        panel = wx.Panel(self, -1)
        self._incr = 1
        self._hiddenlegend = False
        
        panel.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_BTNFACE))
        self.panel2 = wx.Panel(panel, -1)
        self.panel3=wx.Panel(panel,-1)
        #creating the tree
        self.listTREEIngested=wx.TreeCtrl(panel, 1, wx.DefaultPosition, (-1,-1), wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS|wx.TR_MULTIPLE)
        self.rootINGESTED = self.listTREEIngested.AddRoot('ROOT_DCPS_INGESTED')
        self.listTREE=wx.TreeCtrl(panel, 2, wx.DefaultPosition, (-1,-1), wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS|wx.TR_MULTIPLE)
        self.listTREEIngested.SetItemText(self.rootINGESTED,'ROOT_DCPS_INGESTED')
        self.idtreeingested=self.listTREEIngested.GetId()
        self.idtree=self.listTREE.GetId()
        self.listTREEExpanded=False
        self.listTREEIngestedExpanded=False
        # sizer space
        self.h2sizer = wx.BoxSizer(wx.HORIZONTAL)  
        self.labelInfoSpace= wx.StaticText(panel, -1,"Info Espacio",(10,1),style=wx.ALIGN_CENTER_HORIZONTAL)
                
        labelFree= wx.StaticText(self.panel3, -1,"Espacio Libre",(10,2),style=wx.ALIGN_CENTRE)
        labelNonFree= wx.StaticText(self.panel2, -1,"Espacio Ocupado",(10,2),style=wx.ALIGN_CENTRE)
        
        #getting icons for trees
        il = wx.ImageList(16,16)
        il2 = wx.ImageList(16,16)
                
        self.fldcps = il.Add(wx.Bitmap(os.path.join(application_path_images, 'dcp.png')))
        self.flcpls = il.Add(wx.Bitmap(os.path.join(application_path_images, 'cpl.png')))        
        self.listTREE.AssignImageList(il)
        self.fldcps2 = il2.Add(wx.Bitmap(os.path.join(application_path_images, 'dcp.png')))
        self.flcpls2 = il2.Add(wx.Bitmap(os.path.join(application_path_images, 'cpl_in.jpg')))        
        self.listTREEIngested.AssignImageList(il2)
        
        self.busyTransferring=False
        #fill incomingtree
        self.getDCPSIncomingToTree()
        #put the trees collapsed
        self.listTREEIngestedExpanded=False
        self.listTREEIncomingExpanded=False
        #fill ingestedtree
        self.getDCPSIngestedToTree()
        if(self.listTREEIngestedExpanded):
            self.listTREEIngested.ExpandAll()
        else:
            self.collapseChildren(self.listTREEIngested)
        
        labelDCP= wx.StaticText(panel, label="Contenido Encontrado")        
        labelIngested= wx.StaticText(panel, label="Contenido Ingestado Actualmente")
        
        # sizers
        sizer = wx.BoxSizer(wx.VERTICAL)
        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        #the first list (DCP)
        v1sizer=wx.BoxSizer(wx.VERTICAL)
        # the buttons to ingest the dcp's
        v2sizer=wx.BoxSizer(wx.VERTICAL)
        #the second list
        v3sizer=wx.BoxSizer(wx.VERTICAL)
        #buttons at the end
        btnsizer = wx.BoxSizer(wx.HORIZONTAL)
        
        
        panel.SetSizer(sizer)
        
        buttonOne = wx.BitmapButton(panel, -1, wx.Bitmap(os.path.join(application_path_images, 'one.png')))
        buttonOne.Label='Pasar Seleccionado'
        buttonOne.SetToolTipString('Ingestar Seleccionado')# .SetToolTip(wx.ToolTip("click to hide"))
        buttonAll = wx.BitmapButton(panel, -1, wx.Bitmap(os.path.join(application_path_images, 'all.png')))
        buttonAll.SetToolTipString('Ingestar TODO')
        
                
        
        hsizer.AddSizer(v1sizer,1, wx.EXPAND | wx.ALL, 5)
        v1sizer.Add(labelDCP,0,wx.LEFT,5)             
        v1sizer.Add(self.listTREE,1, wx.EXPAND | wx.ALL, 5)
        v1hsizer = wx.BoxSizer(wx.HORIZONTAL)
        btRefresh = wx.BitmapButton(panel, -1, wx.Bitmap(os.path.join(application_path_images, 'refresh.png')))      
        btRefresh.SetToolTipString('Refrescar contenido')
        buttonColInc=wx.BitmapButton(panel, -1, wx.Bitmap(os.path.join(application_path_images, 'collapse.gif')))
        buttonColInc.SetToolTipString('Contraer')
        buttonExpInc=wx.BitmapButton(panel, -1, wx.Bitmap(os.path.join(application_path_images, 'expand.gif')))
        buttonExpInc.SetToolTipString('Expandir')        
        v1hsizer.Add(btRefresh,0,wx.LEFT,5)
        v1hsizer.Add(buttonExpInc,0,wx.LEFT,5)
        v1hsizer.Add(buttonColInc,0,wx.LEFT,5)
        v1sizer.Add(v1hsizer)
        
        hsizer.AddSizer(v2sizer)
        
        v2sizer.Add(buttonOne,0,wx.TOP,100)
        v2sizer.Add(buttonAll,0,wx.BOTTOM,100)
        
        #hsizer.Add(self.listIngested, 1, wx.EXPAND | wx.ALL, 5)
        hsizer.AddSizer(v3sizer,1,wx.EXPAND | wx.ALL, 5);
        v3sizer.Add(labelIngested,0,wx.LEFT,5)
        v3sizer.Add(self.listTREEIngested, 1, wx.EXPAND | wx.ALL, 5)
        # v3hsizer holds the buttons below the right tree
        v3hsizer = wx.BoxSizer(wx.HORIZONTAL)
        btDelete = wx.BitmapButton(panel, -1, wx.Bitmap(os.path.join(application_path_images, 'delete.png')))
        btDelete.SetToolTipString('Eliminar contenido')
        v3hsizer.Add(btDelete,0,wx.LEFT,5)
        btRefresh2 = wx.BitmapButton(panel, -1, wx.Bitmap(os.path.join(application_path_images, 'refresh.png')))        
        btRefresh2.SetToolTipString('Refrescar contenido')
        buttonColIng=wx.BitmapButton(panel, -1, wx.Bitmap(os.path.join(application_path_images, 'collapse.gif')))
        buttonColIng.SetToolTipString('Contraer')
        buttonExpIng=wx.BitmapButton(panel, -1, wx.Bitmap(os.path.join(application_path_images, 'expand.gif')))
        buttonExpIng.SetToolTipString('Expandir')
        v3hsizer.Add(btRefresh2,0,wx.LEFT,5)        
               
        v3hsizer.Add(buttonExpIng,0,wx.LEFT,5)
        v3hsizer.Add(buttonColIng,0,wx.LEFT,5)
        v3sizer.Add(v3hsizer)

        
           
        #sizer.Add(hsizer, 1, wx.EXPAND | wx.ALL, 5)
        #TODO put some info in this sizer??
        #pnl1 = wx.Panel(self, -1)
        #btnsizer.Add(pnl1)
        #a=wx.Frame(self,
        #pnl1 = wx.Panel(self, -1, style=wx.SIMPLE_BORDER)
        #buttonColIng2=wx.BitmapButton(panel, -1, wx.Bitmap('collapse.gif'))
        #btnsizer.Add(buttonColIng2,0,wx.ALL,2)
        #sizer.Add(btnsizer, -1, wx.ALIGN_RIGHT | wx.BOTTOM | wx.LEFT | wx.RIGHT, 5)	


        #btn1 = wx.Button(self,wx.NewId,'a', BitmapButton(panel, -1, wx.Bitmap('expand.gif'))
        '''btn2 = wx.BitmapButton(panel, -1, wx.Bitmap('expand.gif'))
        btn3 = wx.BitmapButton(panel, -1, wx.Bitmap('expand.gif'))
        #self.Image = wx.StaticBitmap(self, bitmap=wx.EmptyBitmap(100,10))
        #btnsizer.Add(self.Image, 0, wx.ALL, 0)
        btnsizer.Add(btn2, 0, wx.ALL, 0)
        btnsizer.Add(btn3, 0, wx.ALL, 0)
    '''
        
        #labelFree.Alignment=wx.ALIGN_CENTER_HORIZONTAL
        self.panel2.SetBackgroundColour(wx.RED)
        self.panel3.SetBackgroundColour(wx.GREEN)
       
        sizer.Add(hsizer, 1, wx.EXPAND | wx.ALL, 5)
        #sizer.Add(self._angleslider, 0, wx.GROW | wx.ALL, 5)
        
        #self.h2sizer.Add(self.labelInfoSpace,0,wx.ALL,5)
        self.FREE=50
        self.NONFREE=50
        #self.h2sizer.Add(self.panel2, self.NONFREE, wx.EXPAND )
        #self.h2sizer.Add(self.panel3, self.FREE, wx.EXPAND )
        sizer.Add(self.h2sizer, 0, wx.EXPAND )
        


        sizer.Layout()        
        sizer.Fit(panel)
        
        self.Centre()

        #binding the buttons
        buttonAll.Bind(wx.EVT_BUTTON, self.buttonAllClick)
        buttonOne.Bind(wx.EVT_BUTTON, self.buttonSelClick)
        btRefresh.Bind(wx.EVT_BUTTON, self.buttonRefClick)
        btRefresh2.Bind(wx.EVT_BUTTON, self.buttonRef2Click)
        btDelete.Bind(wx.EVT_BUTTON, self.buttonDelClick)
        
        self.Bind(wx.EVT_BUTTON,self.buttonCollapseIncoming,buttonColInc) 
        self.Bind(wx.EVT_BUTTON,self.buttonExpandIncoming,buttonExpInc)
        self.Bind(wx.EVT_BUTTON,self.buttonCollapseIngested,buttonColIng) 
        self.Bind(wx.EVT_BUTTON,self.buttonExpandIngested,buttonExpIng)        
        
        
        #binding the toolbar               
        self.Bind(wx.EVT_TOOL,self.buttonRefClick,refresh) 
        self.Bind(wx.EVT_TOOL,self.buttonDelClick,delete)        
        self.Bind(wx.EVT_TOOL,self.buttonAllClick,selectall)
        self.Bind(wx.EVT_TOOL,self.buttonSelClick,selectone)
        self.Bind(wx.EVT_TOOL,self.buttonRef2Click,refresh2)
        self.Bind(wx.EVT_TOOL,self.buttonCollapseIngested,collapse_ingested)
        self.Bind(wx.EVT_TOOL,self.buttonCollapseIncoming,collapse_incoming)
        self.Bind(wx.EVT_TOOL,self.buttonExpandIngested,expand_ingested)
        self.Bind(wx.EVT_TOOL,self.buttonExpandIncoming,expand_incoming)
        
                
        
        
        
        #binding the menu
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
        #Binding for the left tree
        self.listTREE.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectTreeIncoming)
        self.listTREEIngested.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelectTreeIngested)
        
        


        # create a pubsub receiver
        self.currentTitle=''
        Publisher().subscribe(self.updateDisplay, "Update")
        Publisher().subscribe(self.updateCount, "UpdateCount")
        
        
        #check for content
        self.timerCheck = wx.PyTimer(self.CheckForContent)
        self.timerCheck.Start(7000)
        self.CheckForContent()   
        
    def CheckForContent(self):
        if(self.busyTransferring==False):
            self.statusbar.SetStatusText("Chequeando contenido....",0)
            self.getDCPSIncomingToTree()
            self.statusbar.SetStatusText("Contenido chequeado",0)
        else:
            self.timerCheck.Stop()

    def msgDebug(self,msg):
        
        if(self.DEBUG):
            self.logger.debug(msg)
        


    #def refreshToolbar(self,event):
     #   self.getDCPSIncomingToTree()
        
    #def deleteToolbar(self,event):
      #  selectedDCPS=self.listTREEIngested.GetSelections()
      #  self.deleteDCPS(selectedDCPS)            
        
    #get the free space        
    def getfreespace(self,folder): 
        
        # Return folder/drive free space (in bytes) 
        
        if platform.system() == 'Windows': 
            free_bytes = ctypes.c_ulonglong(0) 
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes)) 
            return free_bytes.value 
        else: 
            #os.statvfs(folder).
            return os.statvfs(folder).f_bfree * os.statvfs(folder).f_bsize
    def gettotalespace(self,folder): 
            
            # Return folder/drive free space (in bytes) 
            
            if platform.system() == 'Windows': 
                free_bytes = ctypes.c_ulonglong(0) 
                total = ctypes.c_ulonglong(0)
                ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, ctypes.pointer(total), ctypes.pointer(free_bytes)) 
                                                         
                return total.value 
            else: 
                #os.statvfs(folder).
                return os.statvfs(folder).f_blocks * os.statvfs(folder).f_bsize    

    def getDCPSIncomingToTree(self):
        
        self.listTREE.DeleteAllItems()
        #get dcps to ingest
        self.rootINCOMING = self.listTREE.AddRoot('ROOT_DCPS')
        self.listTREE.SetItemText(self.rootINCOMING,'ROOT_DCPS')
        
        listaux=[]
        self.listDCPSincoming=[]
        
        #
        try:
            if platform.system() == 'Windows':
                listaux=bristol.DCPList(LIB_PATH_INCOMING_WIN,self.logger).dcps
            else:
                listaux=bristol.DCPList(LIB_PATH_INCOMING,self.logger).dcps
            for la in (listaux):
                self.listDCPSincoming.append(la[1])
                
        except:
            error_msg2=str(sys.exc_info()[0])
            wx.MessageBox('Error al intentar conseguir el contenido a ingestar'+error_msg2)
            
            
        i=0
        for dcp in self.listDCPSincoming:
            dcpnode=self.listTREE.AppendItem(self.rootINCOMING,dcp.title)
            self.listTREE.SetItemPyData(dcpnode,i)
            self.listTREE.SetItemImage(dcpnode, self.fldcps,wx.TreeItemIcon_Normal)
            i+=1
            j=0
            for cpl in dcp.cp_f:
                cpl=self.listTREE.AppendItem(dcpnode,cpl[1])
                aux=(i)*10000+j
                self.listTREE.SetItemPyData(cpl,aux)
                self.listTREE.SetItemImage(cpl, self.flcpls,wx.TreeItemIcon_Normal)
                j+=1
                
        if(self.listTREEExpanded):
            self.listTREE.ExpandAll()
        else:
            self.listTREE.CollapseAll()        
        
        
    def getDCPSIngestedToTree(self):
        self.listTREEIngested.DeleteAllItems()
        self.rootINGESTED = self.listTREEIngested.AddRoot('ROOT_DCPS_INGESTED')
        self.listTREEIngested.SetItemText(self.rootINGESTED,'ROOT_DCPS_INGESTED')
        
        #now the dcps already ingested
        listaux=[]
        self.listerrors=[]
        self.listDCPSingested=[]
        try:
            if platform.system() == 'Windows': 
                listaux=bristol.DCPList(LIB_PATH_INGESTED_WIN,self.logger).dcps
                self.listerrors=bristol.DCPList(LIB_PATH_INGESTED_WIN,self.logger).dcps_w_errors
                
            else:
                    
                listaux=bristol.DCPList(LIB_PATH_INGESTED,self.logger).dcps
                self.listerrors=bristol.DCPList(LIB_PATH_INGESTED,self.logger).dcps_w_errors
        except:
            error_msg2=str(sys.exc_info()[0])
            wx.MessageBox('Error al intentar conseguir el contenido ingestado'+error_msg2)
        
        for la in (listaux):
            self.listDCPSingested.append(la[1])
        for dcperror in (self.listerrors):
            
            wx.MessageBox('Error al intentar conseguir el contenido ingestado:\nNombre: '+dcperror[0]+'\nUIID:'+dcperror[1]+'\nCarpeta:'+dcperror[2]+'\nMensaje:\n'+dcperror[3])
               
              
        i=0
        for dcp in self.listDCPSingested:
            dcpnode=self.listTREEIngested.AppendItem(self.rootINGESTED,dcp.title)
            self.listTREEIngested.SetItemPyData(dcpnode,i)
            self.listTREEIngested.SetItemImage(dcpnode, self.fldcps2,wx.TreeItemIcon_Normal)
            i+=1
            j=0
            for cpl in dcp.cp_f:
                cpl=self.listTREEIngested.AppendItem(dcpnode,cpl[1])
                aux=(i)*10000+j
                self.listTREEIngested.SetItemPyData(cpl,aux)
                self.listTREEIngested.SetItemImage(cpl, self.flcpls2,wx.TreeItemIcon_Normal)
                j+=1      
        if(self.listTREEIngestedExpanded):
            self.listTREEIngested.ExpandAll()
            
        else:
            self.collapseChildren(self.listTREEIngested)
            
        

        #self.NONFREE, wx.EXPAND )
        if (platform.system() == 'Windows'):
            self.freespace =self.getfreespace('e:')    
        else:
            self.freespace = self.getfreespace( LIB_PATH_INGESTED)        
        if (platform.system() == 'Windows'):
            self.totalspace =self.gettotalespace('e:')    
        else:
            self.totalspace = self.gettotalespace( LIB_PATH_INGESTED)        
        free=int(round((float(self.freespace)/float(self.totalspace))*100))
        nofree=100-free
        self.h2sizer.Remove(self.labelInfoSpace)
        self.h2sizer.Remove(self.panel2 )
        self.h2sizer.Remove(self.panel3 )      
        self.h2sizer.Add(self.labelInfoSpace,0,wx.LEFT|wx.RIGHT,5)
        self.h2sizer.Add(self.panel2,nofree, wx.EXPAND )
        self.h2sizer.Add(self.panel3,free, wx.EXPAND )
                        

    def buttonAllClick(self,event):       
        
        #get selected items
        selectedDCPS=[]
        
        
        #TODO: Delete this code???
        
        #selectedDCPS=self.listTREE.GetChildren()
        (child, cookie) = self.listTREE.GetFirstChild(self.listTREE.GetRootItem())
        print self.listTREE.GetItemText(child)                    
        while child.IsOk():
            selectedDCPS.append(child)
            print self.listTREE.GetItemText(child)
            child = self.listTREE.GetNextSibling(child)                            
         
        
        
        self.transferDCPS(selectedDCPS)
        
        
    def debugPrint(self,msg):
        if(self.DEBUG):
            print msg
    #Refresing DCPS incoming    
    def buttonRefClick(self,event):
        self.getDCPSIncomingToTree()
    #Refresing DCPS incoming    
    def buttonRef2Click(self,event):
        self.getDCPSIngestedToTree()    
        
    #Deleting DCPS from Library    
    def buttonDelClick(self,event):
        selectedDCPS=self.listTREEIngested.GetSelections()
        self.deleteDCPS(selectedDCPS)

    def buttonSelClick(self,event):       
        
        #get selected items
        selectedDCPS=self.listTREE.GetSelections()
        self.transferDCPS(selectedDCPS)    
        
    def collapseChildren(self,tree):
        
        
        (child, cookie) = tree.GetFirstChild(tree.GetRootItem())
        
        index=tree.GetItemPyData(child)
        self.debugPrint(str(index))
        while child.IsOk():
            tree.CollapseAllChildren(child)
            
            index=tree.GetItemPyData(child)
            self.debugPrint(str(index))            
            child = tree.GetNextSibling(child) 
            
            
        
        
        
    def buttonCollapseIngested(self,event):
        self.collapseChildren(self.listTREEIngested)
        #self.listTREEIngested.CollapseAllChildren(self.listTREEIngested.GetRootItem())
        self.listTREEIngestedExpanded=False
        
    def buttonCollapseIncoming(self,event):
        #self.listTREE.CollapseAll()
        self.collapseChildren(self.listTREE)
        self.listTREEIncomingExpanded=False        
        
    def buttonExpandIngested(self,event):
        self.listTREEIngested.ExpandAll()
        self.listTREEIngestedExpanded=False        
    
    def buttonExpandIncoming(self,event):
        self.listTREE.ExpandAll()
        self.listTREEIncomingExpanded=False               
        
    def deleteDCPS(self, selectedDCPS):
        
               
        #we get indexes of selectedDCPS
        listDCPSindex=[]#index of dcps in listDCPSincoming that had been selected.
        listDCPSnodes=[]
        i=0
        for item in selectedDCPS:
            parentItem = self.listTREEIngested.GetItemParent(item)
            index=self.listTREEIngested.GetItemPyData(item)
            #if(self.listTREE.GetItemText(parentItem)=='ROOT_DCPS'):
            if(self.listTREEIngested.GetRootItem()==parentItem):
                listDCPSindex.append(index)
                listDCPSnodes.append(item)
                i+=1   
        #TODO: from the index delete the dcps
        #get the size of DCPS
        if(len(listDCPSindex)==0):
                    wx.MessageBox('No has seleccionado ningun DCP', 'Info',wx.OK | wx.ICON_INFORMATION)            
                    return        
                
        #check if the user is sure
        if(wx.CANCEL==wx.MessageBox('Estas seguro de eliminar el contenido seleccionado', 'Atencion',wx.OK|wx.CANCEL | wx.ICON_WARNING)):            
            return         
        
        size=0
        for i in listDCPSindex:
            size+=self.listDCPSingested[i].size
        self.thdel=DelThread(listDCPSindex,self.listDCPSingested,self.logger)
        #max is the size to be copied in (10M units)
        self.max = size/100000000
        self.currentTitle=self.listDCPSingested[0].title
        #TODO: Size bigger, time elapsed is in english
        self.dlg = wx.ProgressDialog("Progreso del borrado","Eliminando...",maximum = self.max,
                                       parent=self,style = wx.PD_APP_MODAL | wx.PD_ELAPSED_TIME
                                        #| wx.PD_ESTIMATED_TIME
                                        | wx.PD_REMAINING_TIME)
        self.count1=1
        (self.keepGoing, skip) = self.dlg.Update(self.count1,"Nombre Dcp eliminandose:"+self.currentTitle)
        
        #TODO: Make better the refreshing
        while(self.thdel.is_alive()):
            self.dlg.Update(self.count1,"Nombre Dcp eliminandose:"+self.currentTitle)
            wx.MilliSleep(1000)
            self.count1+=1        
              
        #now we get again the DCPS already ingested
        self.getDCPSIngestedToTree()
            
        if(self.dlg!=None):
            self.dlg.Destroy()
    
    
    def transferDCPS(self, selectedDCPS):
        self.deleteTMP()
        
        if(len(self.listerrors)>0):
            wx.MessageBox('Hay contenido corrupto, a continuacion titulos afectados, borre o renombre las carpetas correspondientes en '+str(LIB_PATH_INGESTED))
            for dcperror in self.listerrors:
                wx.MessageBox('Error al intentar conseguir el contenido ingestado:'+dcperror[0]+' '+dcperror[1])
            return
        #we get indexes of selectedDCPS
        listDCPSindex=[]#index of dcps in listDCPSincoming that had been selected.
        listDCPSnodes=[]
        
        
        
        i=0
        for item in selectedDCPS:
            parentItem = self.listTREE.GetItemParent(item)
            index=self.listTREE.GetItemPyData(item)
            #if(self.listTREE.GetItemText(parentItem)=='ROOT_DCPS'):
            if(self.listTREE.GetRootItem()==parentItem):
                listDCPSindex.append(index)
                listDCPSnodes.append(item)
                i+=1  
        if(len(selectedDCPS)==0):
            wx.MessageBox('No has seleccionado ningun DCP', 'Info',wx.OK | wx.ICON_INFORMATION)            
            return        
        
        listDCPsToRemove=[]#we put in this list the uuid,title and index of listDCPSincoming of "repeated" DCPS        
        for ingestedDCP in self.listDCPSingested:
            for i in listDCPSindex:
                incomingDCP=self.listDCPSincoming[i]
                if (ingestedDCP.uuid==incomingDCP.uuid):
                    listDCPsToRemove.append([ingestedDCP.uuid,ingestedDCP.title,i])
                    #print ingestedDCP.title
        #if listDCPsToRemove is not empty ask the user for overwrite(first delete then copy) the repeated dcp or to leave the already ingested            
        #TODO: Now is all o nothing can't select which dcps to overwrite and which one keep it
        if(len(listDCPsToRemove)>0):
            dia=OverWriteDCPDialog(self, -1, 'buttons')
            for dcpsToRemove in listDCPsToRemove:
                dia.listbox.Append(dcpsToRemove[1])
                
            if dia.ShowModal() == wx.ID_OK:
                for ingestedDCP in self.listDCPSingested:
                    for uuidToDelete in listDCPsToRemove:
                        if (ingestedDCP.uuid==uuidToDelete[0]): 
                            #TODO:Progress of deletion
                            ingestedDCP.rm_dcp()
            else:
                #TODO:delete from listDCPIndex and listDCPSnodes the already ingested TESTED:NO
                None
                self.getDCPSIngestedToTree();
                            
                return                
                #for indextoberemove in listDCPsToRemove:
                #    listDCPSindex.remove(indextoberemove[2])
            dia.Destroy()
            
        
        #get the size of DCPS
        size=0
        usb=False
        for i in listDCPSindex:
            size+=self.listDCPSincoming[i].size
            path_cont_usb=self.listDCPSincoming[i].am_f
            if path_cont_usb.find("usb") > -1:
                usb=True
        
        #get free space
        if platform.system() == 'Windows':
            self.freespace =self.getfreespace('e:')    
        else:
            self.freespace = self.getfreespace( LIB_PATH_INGESTED)
        #TODO: instead of 10G put 2% of disk size
        if(self.freespace<size+1000000000):#check for al least 10G free
            wx.MessageBox('No hay suficiente espacio en disco.\r\nPor favor, elimina algun DCP antes de copiar otro.', 'Atencion: Espacio Insuficiente', 
                            wx.OK | wx.ICON_EXCLAMATION)
            return
        #now if everything is ok we make the copy
        self.busyTransferring=True
        try:
            self.th=TestThread(listDCPSindex,self.listDCPSincoming,self.logger)
        except:
            error_msg2=str(sys.exc_info()[0])
            wx.MessageBox('Error al intentar transferir el contenido'+error_msg2)        
            self.busyTransferring=False
            return
        
        #max is the size to be copied in (130M units)
        if platform.system() == 'Windows':
            self.max = size/10000000
        else:
            if(usb):
                self.max=size/13000000
            else:
                self.max = size/100000000
            
        self.currentTitle=self.listDCPSincoming[0].title
        self.dlg = wx.ProgressDialog("Progreso de la Copia","Copiando... ",maximum = self.max,
                                       parent=self,style = wx.PD_CAN_ABORT | wx.PD_APP_MODAL | wx.PD_ELAPSED_TIME
                                        #| wx.PD_ESTIMATED_TIME
                                        | wx.PD_REMAINING_TIME)
         
        
        self.dlg.SetSize((400,250))    
        self.dlg.Size=(400,250)
            
            #wx.MilliSleep(250)
            #if count >= max / 2:
            #    (keepGoing, skip) = dlg.Update(count, "TODO:Nombre Dcp!")
            #else:
            #get nodes from listTREE and tranfer to listTREEingested
            
            
            #self.displayLbl.SetLabel("Thread started!")
            #btn = event.GetEventObject()
            #btn.Disable()            
            
        self.count1=1
        (self.keepGoing, skip) = self.dlg.Update(self.count1,"Nombre Dcp copiandose: "+self.currentTitle)
        
        
        '''while(self.th.is_alive()):
            self.dlg.Update(self.count1,"Nombre Dcp copiandose:"+self.currentTitle)
            wx.MilliSleep(1000)
            self.count1+=1        
        '''  
            
        '''for count in range(len(listDCPSindex)):
            self.getChildNodesAndTransfer(count, listDCPSnodes,listDCPSindex)            
        '''
        self.timer = wx.PyTimer(self.Notify)
        self.timer.Start(1000)
        self.Notify()        
        
        #self.getDCPSIngestedToTree()
            
        #if(self.dlg!=None):
        #    self.dlg.Destroy()
                       
            
    #TODO: clean this code             
    '''
    def getChildNodesAndTransfer(self, count, listDCPSnodes,listDCPSindex):
        newItem=self.listTREEIngested.AppendItem(self.rootINGESTED,self.listTREEIngested.GetItemText(listDCPSnodes[count]))
        
        childitem, cookie = self.listTREE.GetFirstChild(listDCPSnodes[count])  
    
        while childitem.IsOk():
            
            self.listTREEIngested.AppendItem(newItem,self.listTREEIngested.GetItemText(childitem))
            childitem, cookie = self.listTREE.GetNextChild(listDCPSnodes[count], cookie)            
    '''        
        
    def OnClose(self, event):

        #self._timer.Stop()
        #del self._timer

        self.Destroy()
        

    def OnToggleTransparency(self, event):

        self._pie.GetLegend().SetTransparent(not self._pie.GetLegend().IsTransparent())
        self._pie.Refresh()


    def OnToggleEdges(self, event):

        #self._pie.SetShowEdges(not self._pie.GetShowEdges())
        self._progresspie.SetShowEdges(not self._progresspie.GetShowEdges())

        
    def OnSelectTreeIncoming(self, event):
        #tell to timer that we can check for incoming content
        self.busyTransferring=True
        if(self.timerCheck.IsRunning()):
            self.timerCheck.Stop()        
        
        tree=self.listTREE
        self.selectOnlyParentItem(event,tree)
        
    def OnSelectTreeIngested(self, event):
        
        tree=self.listTREEIngested
        
        self.selectOnlyParentItem(event,tree)
        
    def selectOnlyParentItem(self,event,tree):
        listselected=[]
        listselected=tree.GetSelections() 
        if(len(listselected)<=0):return
        #we get indexes of selectedDCPS
        listDCPSindex=[]#index of dcps in listDCPSincoming that had been selected.
        listDCPSnodes=[]
        i=0
        lisselected_dcps=[]#to contain nodes with dcps selected.
        
        for item in listselected:
            parentItem = tree.GetItemParent(item)
            #self.listTREE.get
            data=tree.GetPyData(item)
            if(data>=10000):
                #it's a child
                #self.listTREE.SelectItem(parentItem)
                (aux,aux1)=divmod(data,10000)
                if(aux>0):aux-=1
                self.debugPrint(aux)
            else:
                #it's a parent
                aux=data
                self.debugPrint(data)
                
            lisselected_dcps.append(aux)
        tree.SetEvtHandlerEnabled(False)    
        #unselect all to select only the parent
        tree.UnselectAll()
        
        #first_child=self.listTREE.GetFirstChild(self.listTREE.GetRootItem())
                
        (child, cookie) = tree.GetFirstChild(tree.GetRootItem())
        while child.IsOk():
            ind_dcp=tree.GetItemPyData(child)
            text=tree.GetItemText(child)
            if(ind_dcp in lisselected_dcps):
                tree.SelectItem(child)
                #self.debugPrint('Seleccionando item ['+str(ind_dcp)+']'+text))
            (child, cookie) = tree.GetNextChild(tree.GetRootItem(),cookie)
            
            #print self.listTREE.GetItemText(item)+' - 3 - child selected'
            #print self.listTREE.GetItemText(parentItem)+' - 3 - parent'
            #if(self.listTREE.GetItemText(parentItem)=='ROOT_DCPS'):
            #if(self.listTREE.GetRootItem()!=parentItem):
            #    print self.listTREE.GetItemText(parentItem)+' - 3 - parent'
            #    self.listTREE.SelectItem(parentItem)
            #    self.listTREE.GetItemText(item)+' - 3 - child selected'
            #    self.listTREE.SelectItem(parentItem)
        tree.SetEvtHandlerEnabled(True)  
        
    def OnSelectTreeIngested2(self, event):
        
        listselected=[]
        listselected=self.listTREE.GetSelections() 
        if(len(listselected)<=0):return
        #we get indexes of selectedDCPS
        listDCPSindex=[]#index of dcps in listDCPSincoming that had been selected.
        listDCPSnodes=[]
        i=0
        lisselected_dcps=[]#to contain nodes with dcps selected.
        self.SetEvtHandlerEnabled(False)
        for item in listselected:
            parentItem = self.listTREE.GetItemParent(item)
            #self.listTREE.get
            data=self.listTREE.GetPyData(item)
            if(data>=10000):
                #it's a child
                #self.listTREE.SelectItem(parentItem)
                (aux,aux1)=divmod(data,10000)
                if(aux>0):aux-=1
                self.debugPrint(aux)
            else:
                #it's a parent
                aux=data
                self.debugPrint(data)
                
            lisselected_dcps.append(aux)
            
        #unselect all to select only the parent
        self.listTREE.UnselectAll()
        
        #first_child=self.listTREE.GetFirstChild(self.listTREE.GetRootItem())
                
        (child, cookie) = self.listTREE.GetFirstChild(self.listTREE.GetRootItem())
        while child.IsOk():
            ind_dcp=self.listTREE.GetItemPyData(child)
            text=self.listTREE.GetItemText(child)
            if(ind_dcp in lisselected_dcps):
                self.listTREE.SelectItem(child)
                #self.debugPrint('Seleccionando item ['+str(ind_dcp)+']'+text))
            (child, cookie) = self.listTREE.GetNextChild(self.listTREE.GetRootItem(),cookie)
            
            #print self.listTREE.GetItemText(item)+' - 3 - child selected'
            #print self.listTREE.GetItemText(parentItem)+' - 3 - parent'
            #if(self.listTREE.GetItemText(parentItem)=='ROOT_DCPS'):
            #if(self.listTREE.GetRootItem()!=parentItem):
            #    print self.listTREE.GetItemText(parentItem)+' - 3 - parent'
            #    self.listTREE.SelectItem(parentItem)
            #    self.listTREE.GetItemText(item)+' - 3 - child selected'
            #    self.listTREE.SelectItem(parentItem)
        self.SetEvtHandlerEnabled(True)      
        
    def OnToggleLegend(self, event):
        self.debugPrint('j')
        #self._hiddenlegend = not self._hiddenlegend
        
        #if self._hiddenlegend:
            #self._pie.GetLegend().Hide()
        #else:
            #self._pie.GetLegend().Show()

        #self._pie.Refresh()
        
        
    def OnSlider(self, event):
        self.debugPrint("helo")
        #self._pie.SetAngle(float(self._slider.GetValue())/180.0*pi)
        #self._progresspie.SetAngle(float(self._slider.GetValue())/180.0*pi)


    def OnAngleSlider(self, event):
        print "d"
        #self._pie.SetRotationAngle(float(self._angleslider.GetValue())/180.0*pi)
        #self._progresspie.SetRotationAngle(float(self._angleslider.GetValue())/180.0*pi)


    def CreateMenuBar(self):

        file_menu = wx.Menu()
        
        AS_EXIT = wx.NewId()        
        file_menu.Append(AS_EXIT, "&Salir")
        self.Bind(wx.EVT_MENU, self.OnClose, id=AS_EXIT)

        corrupt_menu = wx.Menu()
        AS_CORRUPT = wx.NewId()
        corrupt_menu.Append(AS_CORRUPT, "&Corrupto...")
        self.Bind(wx.EVT_MENU, self.OnCorrupt, id=AS_CORRUPT)
        
        help_menu = wx.Menu()
        AS_ABOUT = wx.NewId()
        help_menu.Append(AS_ABOUT, "&Acerca...")
        self.Bind(wx.EVT_MENU, self.OnAbout, id=AS_ABOUT)        

        menu_bar = wx.MenuBar()

        menu_bar.Append(file_menu, "&Fichero")
        menu_bar.Append(corrupt_menu, "&Corrupto")
        menu_bar.Append(help_menu, "&Acerca")        

        return menu_bar
    
    
    def OnCorrupt(self, event):
    
            
                  
            dlg = RemoveCorrruptedDCPDialog(self,-1,"DCPS Corrompidos")
            
            #dlg.SetFont(wx.Font(8, wx.NORMAL, wx.NORMAL, wx.NORMAL, False, "Verdana"))
            for corrupto in self.listerrors:      
                            dlg.listbox.Append(corrupto[0]+' : '+corrupto[1]+' : '+corrupto[2])  
                            
            if(len(self.listerrors)<=0):
                wx.MessageBox('El sistema no ha encontrado ningun dcp corrupto.')
                return
            dlg.ShowModal()
            
                
            if dlg.ReturnCode== wx.ID_OK:
                #do the job
                deleted_ok=True
                for corrupto in self.listerrors:      
                    try:
                        if(os.path.isdir(corrupto[2])):
                            shutil.rmtree(corrupto[2])
                    except IOError as io:
                        wx.MessageBox('Ha ocurrido un error mientras se borraba la carpeta '+corrupto[2]+'\nMensaje:\n'+str(io.message))
                        deleted_ok=False
                if(deleted_ok):
                    wx.MessageBox('Finalizado el borrado de carpetas corruptas')
                else:
                    #TODO: show folders not deleted
                    wx.MessageBox('Repase las carpetas con errores y borrelas manualmente.')
            dlg.Destroy()    
    
          
    def OnAbout(self, event):

        msg = "Esto es el acerca de DCPLibrary\n\n" + \
              "Autor: Proyecson S.A. 2013\n\n" + \
              "Por favor informa the cualquier problema/peticion de mejora\n" + \
              "En la siguiente direccion de correo:\n\n" + \
              "cor@proyecson.com\n" 
              
        dlg = wx.MessageDialog(self, msg, "DCPLibrary",
                               wx.OK | wx.ICON_INFORMATION)
        
        dlg.SetFont(wx.Font(8, wx.NORMAL, wx.NORMAL, wx.NORMAL, False, "Verdana"))
        dlg.ShowModal()
        dlg.Destroy()
        
    #---------------------------------------
    def Notify(self):
        #TODO: make more realistic the time getting size of folder
        if(self.th.isAlive and (self.th.done!=True) and self.keepGoing==False):
            #it is already cancelled
            #if(self.th.cancelled==True):
             #   self.th.done=True
              
                
            #if not we are going to cancel    
            self.debugPrint("cancelando")
            (self.keepGoing,tt)=self.dlg.Update(self.count1,"Cancelando copia. Terminando....\n"+str (self.th.title))
            self.th.cancelled=True
            self.debugPrint("cancelling")
            #if(self.th.cancelled):
            #    self.th.__stop
               
            #stop the thread if not yet
            if(self.th.cancelled and self.th.isAlive):self.th.join() 
            #tell to timer that we can check for incoming content
            self.busyTransferring=False
            
            
            self.timer.Stop()   
            
            if(self.timerCheck.IsRunning()==False):
                self.timerCheck.Start(7000)
            self.getDCPSIngestedToTree()
            self.th.done=True
            self.busyTransferring=False
            (self.keepGoing,tt)=self.dlg.Update(self.max,"Cancelando copia. Terminando\n"+str (self.th.title))            
            self.keepGoing=False
            return
        
        if(self.th.isAlive and (self.th.done!=True) ):
            #alive and kicking
            self.debugPrint("vivo")
             
            if(self.count1<=self.max):
                if(self.count1+1==self.max):
                    self.count1-=1
                else:
                    self.count1+=1
                (self.keepGoing,tt)=self.dlg.Update(self.count1,"Copiando...\n"+str (self.th.title))
            else:
                self.logger.error('Maximun exceed: Max('+str(self.max)+') Value('+str(self.count1)+')')
                (self.keepGoing,tt)=self.dlg.Update(self.count1,"Copiando..... "+str (self.th.title))
                
        else:
            #finish ok
            time.sleep(1500)
            self.timer.Stop()
            self.debugPrint("death and done 1")
            if(self.th.done and self.th.isAlive):self.th.join()
            self.logger.error('Maximun exceed and thread has to be closed ')
            #tell to timer that we can check for incoming content
            self.busyTransferring=False
            if(self.timerCheck.IsRunning()==False):
                self.timerCheck.Start(7000)
            #update ingested content
            self.getDCPSIngestedToTree()

    def deleteTMP(self):
        self.logger.info('Start deleting TMP folder')
        #temp_path=os.path.join(LIB_PATH_INGESTED,'tmp/')
        for root,dirs,files in os.walk(LIB_PATH_INCOMING_TMP):
	#for root,dirs,files in os.walk('/data/tmp'):
	#self.logger.info('temp path: '+str(LIB_PATH_INCOMING_TMP))
            for f in files:
		self.logger.info(' Deleting file'+str(os.path.join(root,f)))
                os.unlink(os.path.join(root,f))
            for d in dirs:
		self.logger.info(' Deleting dir'+str(os.path.join(root,d)))
                shutil.rmtree(os.path.join(root,d))
        self.logger.info('Finish deleting TMP folder')
    
    def updateCount(self,msg):    
        if(msg.data!=''):
            indices=msg.data.split('|')
            if(len(indices)>1):
                si=indices[0]
                sj=indices[1]
                i=0
                j=0
                try:
                    i = int(si)
                    j=int(sj)
                except ValueError:
                    return
                
                
                if(j>1 and i<j):
                    if( (i+1)==j):
                        return
                    step=self.max/j
                    self.count1=(i+1)*step
                    self.debugPrint("count:"+str(i)+'|'+str(self.count1))
            
    
    def updateDisplay(self,msg):
        
        """
        Receives data from thread and updates the display
        """
        
                           
        
        
        self.keepGoing = True
        count = 0
        if(msg.data==''):
            msg.data=self.currentTitle
            
            
        if(msg.data=='end'):
            self.debugPrint('MSG(end):'+msg.data)
            self.timer.Stop()
            if(self.th.isAlive):
                self.th.join()
               
            self.getDCPSIngestedToTree()
            (self.keepGoing,tt)=self.dlg.Update(self.max,"Transferencia Terminada")
            return
            
        if isinstance(msg, str):
            #self.displayLbl.SetLabel("Time since thread started: %s seconds" % t)
            self.debugPrint('MSG(instance1):'+msg.data)
            self.currentTitle=msg.data
            self.count1+=1
            (self.keepGoing,tt)=self.dlg.Update(self.count1,"Copiando... "+str(self.currentTitle))
        else:
            #self.displayLbl.SetLabel("%s" % t)
            #self.btn.Enable()
            self.debugPrint('MSG(instance2):'+msg.data)
            self.currentTitle=msg.data
            (self.keepGoing,tt)=self.dlg.Update(self.count1,"Copiando... "+str (self.currentTitle))
            self.count1+=1
            #if(self.dlg!=None):
                #self.dlg.Destroy()
        
        
        

if __name__ == "__main__":
    app = wx.PySimpleApp()
    frame = BristolLibrary(None, -1, "DCPLibrary")
    app.SetTopWindow(frame)
    frame.Show()
    app.MainLoop()
'''
TODO: button Collapse all and son
TODO: Help and so on.
TODO: check every 5 seconds or similar for changing incoming dcps.
TODO: Proyecson version to copy between CRU or CRU->server->CRU
TODO: Document better everything
TODO: print only when debugging
TODO: auto updates?
TODO: get content from ftp,http, so on.
TODO: send emails,messages, when operation finish

'''
