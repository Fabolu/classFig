#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from cycler import cycler
        
class classFig:
    """
    Class for comfortable figure handling with python / matplotlib   
    @author: fstutzki
    """
    def __init__(self, template='PPT', subplot=(1,1), sharex=False, sharey=False, width=0, height=0, fontfamily='', fontsize=0, linewidth=0, figshow=True):
        """ Set default values and create figure: fig = classFig('OL',(2,2)) """
        self.figshow = figshow # show figure after saving
        self.subplot_geo = subplot # subplot geometry, first value Y-axis (above), second value X-axis (besides)
        self.subplot_cnt = subplot[0]*subplot[1] # number of subplots
        self.axeC = 0 # current axis
        
        # color
        colorBlue    = np.array([33,101,146])/255 #iap color "blue"
        colorRed     = np.array([218,4,19])/255   #iap color "red"
        colorGreen   = np.array([70,173,52])/255  #iap color "green"
        colorOrange  = np.array([235,149,0])/255  #iap color "orange"
#        colorYellow  = np.array([255,242,0])/255  #iap color "yellow"
#        colorGrey    = np.array([64,64,64])/255   #iap color "black"
        
        if template.lower() == 'ppt':
            tpl_width = 15
            tpl_height = 10
            tpl_fontfamily = 'sans-serif'
            tpl_fontsize = 12
            tpl_linewidth = 2
        elif template.lower() == 'ppttwo':
            tpl_width = 10
            tpl_height = 8
            tpl_fontfamily = 'sans-serif'
            tpl_fontsize = 12
            tpl_linewidth = 2
        elif template.lower() == 'pptbig':
            tpl_width = 20
            tpl_height = 15
            tpl_fontfamily = 'sans-serif'
            tpl_fontsize = 12
            tpl_linewidth = 3
        elif template.lower() == 'ol':
            tpl_width = 8
            tpl_height = 6
            tpl_fontfamily = 'serif'
            tpl_fontsize = 9
            tpl_linewidth = 1
        elif template.lower() == 'oe':
            tpl_width = 12
            tpl_height = 8
            tpl_fontfamily = 'serif'
            tpl_fontsize = 10
            tpl_linewidth = 1
            
        if width==0:
            width = tpl_width
        if height==0:
            height = tpl_height
        if fontfamily=='':
            fontfamily = tpl_fontfamily
        if fontsize==0:
            fontsize = tpl_fontsize
        if linewidth==0:
            linewidth = tpl_linewidth
        
        mpl.rc('font',size=fontsize)
        mpl.rc('font',family=fontfamily)
        mpl.rc('lines',linewidth=linewidth)
        mpl.rc('axes', prop_cycle=(cycler('color', [colorBlue,colorRed,colorGreen,colorOrange,colorBlue,colorRed,colorGreen,colorOrange,colorBlue,colorRed,colorGreen,colorOrange,colorBlue,colorRed,colorGreen,colorOrange])+
                                   cycler('linestyle', ['-','-','-','-','--','--','--','--',':',':',':',':','-.','-.','-.','-.'])))
        
        self.figH, self.axeH = plt.subplots(self.subplot_geo[0],self.subplot_geo[1],sharex=sharex,sharey=sharey)
        
        self.figH.set_size_inches(width/2.54,height/2.54)
        
    def axis_current(self):
        """ Returns the axis handle for the current axis """
        self.axeC = self.axeC % ( self.subplot_geo[0] * self.subplot_geo[1] )
        if self.subplot_geo == (1,1):
            return self.axeH
        elif self.subplot_geo[0] > 1 and self.subplot_geo[1] > 1:
            isuby = self.axeC // self.subplot_geo[1]
            isubx = self.axeC % self.subplot_geo[1]
            return self.axeH[isuby][isubx]
        else:
            return self.axeH[self.axeC]
            
    def subplot(self,iplot=np.NaN):
        """ Set current subplot: fig.subplot(0) for first subplot or fig.subplot() for next subplot """
        if iplot is np.NaN:
            self.axeC += 1
        else:
            self.axeC = iplot
        self.axeC = self.axeC % ( self.subplot_geo[0] * self.subplot_geo[1] )
    
    def suptitle(self,*args,**kwargs):
        """ Set super title for the whole figure """
        self.figH.suptitle(*args,**kwargs)
    def plot(self,*args,**kwargs):
        """ Plot data """
        axeC = self.axis_current()
        axeC.plot(*args,**kwargs)
#        axeC.set_xlim(np.min(x),np.max(x))
    def pcolor(self,*args,**kwargs):
        """ 2D area plot """
        axeC = self.axis_current()
        if 'cmap' not in kwargs:
            kwargs['cmap'] = 'nipy_spectral'
        axeC.pcolormesh(*args,**kwargs)
    def title(self,*args,**kwargs):
        """ Set title for current axis """
        axeC = self.axis_current()
        axeC.set_title(*args,**kwargs)
    def xlabel(self,*args,**kwargs):
        """ Set xlabel for current axis """
        axeC = self.axis_current()
        axeC.set_xlabel(*args,**kwargs)
    def ylabel(self,*args,**kwargs):
        """ Set ylabel for current axis """
        axeC = self.axis_current()
        axeC.set_ylabel(*args,**kwargs)
    def xlim(self,xmin=np.inf,xmax=-np.inf):
        """ Set limits for current x-axis: fig.xlim(0,1) or fig.xlim() """
        axeC = self.axis_current()
        if xmin==np.inf and xmax==-np.inf:
            for iline in axeC.lines:
                x = iline.get_xdata()
                xmin = np.minimum(xmin,np.min(x))
                xmax = np.maximum(xmax,np.max(x))
        axeC.set_xlim(xmin,xmax)
    def ylim(self,ymin=np.inf,ymax=-np.inf):
        """ Set limits for current y-axis: fig.ylim(0,1) or fig.ylim() """
        axeC = self.axis_current()
        if ymin==np.inf and ymax==-np.inf:
            for iline in axeC.lines:
                y = iline.get_ydata()
                ymin = np.minimum(ymin,np.min(y))
                ymax = np.maximum(ymax,np.max(y))
        axeC.set_ylim(ymin,ymax)
    def save(self,filename,*args,**kwargs):
        """ Save figure to png, pdf: fig.save('test.png',600,'pdf') """
        dpi = 300
        fileparts = filename.split('.')
        fileformat = set()
        fileformat.add(fileparts[-1])
        filename = filename.replace("."+fileparts[-1],"")
        for attribute in args:
            if isinstance(attribute, int):
                dpi = attribute
            else:
                fileformat.add(attribute)
         
        self.figH.tight_layout()
        if 'dpi' not in kwargs:
            kwargs['dpi'] = dpi
        for iformat in fileformat:            
            self.figH.savefig(filename+"."+iformat,**kwargs)
        if self.figshow==True:
            plt.show()
            
if __name__ == '__main__':
    fig = classFig('oe',(3,2))
    fig.subplot()
    fig.plot(np.linspace(0,2,10),np.random.rand(10,3))
    fig.xlim()
    fig.title('Random numbers')
    fig.xlabel('Test')
    fig.subplot(4)
    fig.pcolor(np.random.rand(10,10))
    fig.ylabel('Numbers')
    fig.save('fig_test.png',600,'pdf')
    