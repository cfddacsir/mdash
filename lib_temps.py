#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__doc__='''
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
  post_temps.py
[-figsave] generate figures of the monitored values
[-figshow] show figures of the monitored values as they are generated
[-method <int>] select what method for adjusting y-scaling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
@last:   2025-03-24-1025t 

'''
__version__='''
@author: Daniel A. Collins dac@dacdynamics.com, daniel.collins@quest-global.com
@last:   2025-03-24-1025t 
Created  Mon Feb 24 11:06:32 2025
'''
SIGNAL_LIST={
   0:  'K' , 
   1:  'time' , 
   2:  'aoss-0' , 
   3:  'cpu-0-0' , 
   4:  'cpu-0-1' , 
   5:  'cpu-0-2' , 
   6:  'cpu-0-3' , 
   7:  'gpuss-0' , 
   8:  'gpuss-1' , 
   9:  'nspss-0' , 
   10: 'nspss-1' , 
   11: 'nspss-2' , 
   12: 'video' , 
   13: 'ddr' , 
   14: 'camera-0' , 
   15: 'camera-1' , 
   16: 'mdmss-0' , 
   17: 'pm8150_tz' , 
   18: 'therm-soc-usr' , 
   19: 'skin-sensor' , 
   20: 'skin-sensor-o' , 
   21: 'therm-quiet-usr' , 
   22: 'therm-rf-usr' , 
   23: 'therm-in-temp-usr' ,
}   
##############################################################################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# %% Setting Manual Values 
if 1: # MANUAL_PATH
    MANUAL_PATH = r'/Users/dac/qlab/testing/Q0C008';
    # MANUAL_PATH = r'/Users/dac/qlab/testing/Q0D009';
    
    
    finp = "watch_temps.csv";
SKIP_LIST = [  19, 25 ];
OFFSET = [ True, True ] ;
inppath = None; 
#inppath = r'/Users/dac/qlab/testing/' ;
# %% Setting Default values for EXE 
EXE = {
    ## default values for execution, are over-ridden from ArgParse
    'inp'   : None, # default for input path-file 
    #'inp' : r'/Users/dac/qlab/testing/' ,
    'method'  : 6      ,
    'figsave' : False  ,
    'figshow' : True   ,
    'SELGROUPS' : [ 1,2,3,4,5,0 ] ,
    
};
if 1: ## processing in Main
    ProcesGroups = True
    ProcessGroupPlot = True
    PlotNoScaling = True 
    PlotScaling = False 
    ProcessDerivatives = True
if 1: ## more options 
    AddInflections = True    ## inside analyze_derivative()
    OPTS={
       'AddInflections' : True, ## inside analyze_derivative()
       
    }
if 1: ## Calibrating some dials
    EXE['Smooth'] = True  

    AA = 2.00   ## low smoothing
    AA = 4.12  ## medium smooth
    # AA = 12.00  ## high smooth
    SMOOTHER= {
        'Factor1' : (1/ AA) ,   ## orig (1/18)    
        'Factor2' : (AA   ) ,   ## orig (10)    
    }


    # CORRECTORS=[
    # True,
    # True,
    # True,
    # ]
#OPTS['AddInflections']
## initializing some stuff    
PSH =[0 for i in range(0,100)] ; 
DEFPSH =[0 for i in range(0,100)] ; 
PATH_LIB = r'/Users/dac/pylab/lib/';
PATH_SLIDEMASTER = r'/Users/dac/pylab/lib/';

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
COLOURS = {
    
     'max':
     [ 205/255,   10/255,   5/255 ], ## max
     'mean':
     [  25/255,  200/255,   5/255 ], ## mean
     'min':
     [  25/255,   50/255, 210/255 ], ## min
     'reg':
     [ 111/255,  110/255, 112/255 ], ## min
    }
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

##############################################################################

import warnings;warnings.simplefilter(action='ignore', category=FutureWarning);# Suppress FutureWarning
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#import myfavs as my;
#import danpy as dan;
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# basics
import os;
from   os import listdir;
from   pathlib import Path;
import re ;
import argparse ;
## import linecach

import numpy as np;
import pandas as pd;
import matplotlib.pyplot as plt;
import matplotlib as mpl;
import seaborn as sns;
from   scipy import stats;
from   scipy.interpolate import interp1d
from   scipy import interpolate

# %matplotlib inline # uncomment only in jupyter
FSS = os.sep;

###############################################################################
# %% determing OS of host
def host_os( ):   
    '''
    arg:  None
    ret: FSS <str> file-separator based on the operating system.
         SH  <str> shell to use for OS
             SH= sh for shell (bash)
             SH= pw for powershell (windows/others)
    '''
    #import unicode; 
    import platform; p = platform.uname();
    if p.system == 'Windows': 
        FS  =  str('\u005c') ;  ## == "\" #if system is Windows:
        SH  =  str('ps1') ;
    else: 
        FS  =  str('\u002f') ;  ## == "/"  # if NOT windows
        SH  =  str('bsh' ) ;
    FSS =  str( 1*FS ) ;
    return FSS, SH ;


FSS = os.sep; ## osfss();

###############################################################################
# %% Reading Inputs, Files,  
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def searchdir( search_dir, SHOW=False  ):
    import os 
    pw = os.getcwd();
    os.chdir(search_dir);
    files = filter(os.path.isdir, os.listdir(search_dir));
    #files = [os.path.join(search_dir, f) for f in files] # add path to each file
    files = [os.path.join( 0*search_dir, "", f) for f in files] ;# add path to each file
    files.sort(key=lambda x: os.path.getmtime(x));
    #if SHOW: print ( files );
    if '.DS_Store' in files:
        files.remove('.DS_Store')
    os.chdir(pw);
    return files ;

def getArgs( EXE ):
    '''
    EXE = getArgs(EXE) ; 
    ## returns new values for EXE based on parameters specified in argparse
    '''
  ##-----------------------------------------------------------    
    ##INARGS={};
    parser = argparse.ArgumentParser();
    parser.add_argument("-doc", 
            help=" show help info and all doc details " ,
            action='store_true', );

    parser.add_argument("-inp",
            nargs=1, type=str, default='' ,
            help="__<str:>: path of inputh file (use cwd if blank) ",
            action='store',);  
    parser.add_argument("-method", 
            nargs=1, type=int, default=30, 
            help="__<int: 1>: method for adjusting scales",
            action='store',);
    parser.add_argument("-smooth",  
            help="__<true>  : run smoothing operator ",
            action='store_true',);
    parser.add_argument("-nosmooth",  
            help="__<false> : do NOT run smoothing operator ",
            action='store_true',);
    parser.add_argument("-figsave", 
            help=" make Figures of Monitored values" ,
            action='store_true',);
    parser.add_argument("-figshow", 
            help=" show Figures of Monitored values" ,
            action='store_true',);
    # parser.add_argument("-ppt", 
    #         help=" make Slides compiled of Monitored Figures <<!not ready>>" ,
    #         action='store_true',);
    #SET_CASE
    # parser.add_argument("-case",
    #         nargs=1, type=str, default='' ,
    #         help="__<str:>: name of case ",
    #         action='store',);            
    ##-----------------------------------------------------------    
    args   = parser.parse_args();
    if (args.doc)!=None: EXE['doc']  = args.doc  ;# print("will do      {}".format(args.v  ));
    if (args.inp)!=None: EXE['inp']  = args.inp;# print("will do inp: {}".format(args.inp));
    if (args.figsave)!=None: EXE['figsave']  = args.figsave;# print("will do fig: {}".format(args.fig));
    if (args.figshow)!=None: EXE['figshow']  = args.figshow;# print("will do fig: {}".format(args.fig));
    if (args.method)!=None: EXE['method']  = args.method[0];# print("will do fig: {}".format(args.fig));
    # if (args.case)!=None: EXE['case']  = args.case[0]  ;# print("will do      {}".format(args.v  ));
    # if (args.ppt)!=None: EXE['ppt']  = args.ppt;# print("will do ppt: {}".format(args.ppt));
    
    return EXE ;

#  Read File ############################################################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def DictNames( names ):
    colname = dict();
    for k, v in enumerate( names) :
        colname[k] = v;
    
    namecol = dict();
    for k, v in enumerate( names) :
        namecol[v] = k;
    return colname, namecol;

def getFiles(inppath, nfdef = 1,
             LASTFILE=True,
             ALLFILES=False,
             KW_BEG='watch_temp', 
             KW_END='csv', 
             SHOW=True , 
    ):
    inpfile = [];
    for f in listdir(inppath):
        if (KW_BEG in f):
            if (KW_END in f):
              if ('stat' not in f):
                inpfile.append( inppath +FSS + f)
    NFILES  = len(inpfile);
    if SHOW: print ( f'path : {inppath} ')
    ## if SHOW: print ( f'files found: {inpfile} ')
    inpfile = inpfile[NFILES-nfdef:NFILES];
    #if PSH[2]:
    # print(Selectinpfile);
    if SHOW: print ( f'files found: {inpfile} ')
    
    if LASTFILE:    
        if type( inpfile) == list:
              inpfile = inpfile[-1];  ## get last one found
        else: inpfile = str( inpfile) ; 
        if SHOW: print( f' Using Last File in {inppath}: {inpfile} ')

    if ALLFILES:
        infile = list ( inpfile[NFILES-nfdef:NFILES] ); 
        if SHOW: print( f' Using All Files in {inppath} ')
    return inpfile ;

def getdf(inpfile):
    DF = pd.concat(map(pd.read_csv, inpfile));
    return DF

def get_dfread( inpfile=None, inppath=None, 
               SKIP_LIST=SKIP_LIST, 
               SHOW = False, SHOWFILES=True 
    ):
    #if innpfile == None: pass;
        # inpfile = getFiles(inppath, 
        #                          nfdef = 1, 
        #                          KW_BEG='watch_temp', 
        #                          KW_END='csv' ,
        #                          SHOW=SHOWFILES,
        # )
    if type(inpfile ) == str:
        dfread = pd.read_csv( str( inpfile ), index_col=False  
        );
    else:
        dfread = getdf( inpfile );
        
    if SHOW:
        print( dfread.head ) ;
        print( dfread.columns ) ;
        print( dfread.iloc[:,0:2] ) ;
    
    names =  dfread.columns ;

    # More processes for scope of the file
    
    ## removing unnecessary registers ...
    dfread.drop( columns=names[SKIP_LIST], inplace=True ) ;
    dfread.drop( columns=['Unnamed: 26'], inplace=True ) ;
    
    ## renaming 'TIME' --> 'time'
    dfread.rename( columns={'TIME':'time'}, inplace=True );
    
    return dfread, inpfile ;


# names =  dfloc.columns ;
# enames = len(names) ;


# In[] smooth operators ######################################################
#  
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


def fsmoothsignal( smpl, factor1=SMOOTHER['Factor1'], factor2=SMOOTHER['Factor2'] ):
    '''
    fsmoothsignal( smpl, factor1=(1/18), factor2=10 ):

    Parameters
    ----------
    smpl : TYPE
        DESCRIPTION.
    factor1 : TYPE, optional
        DESCRIPTION. The default is (1/18).
    factor2 : TYPE, optional
        DESCRIPTION. The default is 10.

    Returns
    -------
    TYPE
        DESCRIPTION.

    '''
    from   scipy import signal;
    #factor1 = (1/18);
    #factor2 = 10  
    b, a = signal.butter( 1 , factor1, fs=factor2 );
    fsmooth = signal.filtfilt( b, a, smpl );
    return fsmooth;


## %% DF CORRECTION 
def dfcorrection( dfloc, c, 
                  APPLYSMOOTH=False, 
                  ) :
    cn = dfloc.columns[c];
    df1 = dfloc.iloc[:,c] ;
    #if CORRECTION[0]:
    df1 = ( 0.001 ) * df1 ;
    #if CORRECTION[1]:
    #  df1 = df1 - 273.15 ;
    if APPLYSMOOTH:
      df1 = fsmoothsignal( df1 );
    if APPLYSMOOTH == False:
      print('! not using Corrector2, smooth function! ')

    return df1 ;


def dfcorrection1( dfloc, c, 
                 CORRECTION=[True,True,True], 
                  ) :
    cn = dfloc.columns[c];
    df1 = dfloc.iloc[:,c] ;
    if CORRECTION[0]:
      df1 = ( 0.01 ) * df1 ;
    if CORRECTION[1]:
      df1 = df1 - 273.15 ;
    if CORRECTION[2]:
      df1 = fsmoothsignal( df1 );
    if CORRECTION[2]==False:
      print('! not using Corrector2, smooth function! ')

    return df1 ;

def timedur( dftime  ):
    ''' changing TIMESTMP<%H:%M:%S> to Timedur<sec> '''

    Time1 = pd.to_datetime( dftime , format="%H:%M:%S" )
    Timedur = Time1 - Time1[0]
    Timedur = Timedur.to_numpy().astype('<m8[s]')
    Timedur = Timedur.astype('float64')
    dftime = Timedur ;    
    return dftime ;

def build_dfcor( dfloc, APPLYSMOOTH=False  ):
    ''' build_dfcor( dfloc, CORRECTION=[True,True,True], SHOW=True )
# build new dataframe array with corrections in dfcorrection '''
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    cnames = dfloc.columns; 
    ## dfbak = dfloc.copy();
    dfcor = pd.DataFrame( data=None, columns=dfloc.columns ) ;
    dfcor['k'] = dfloc['k'] ;
#    dfcor['time'] = dfloc['time'] ;
    dfcor['time'] = timedur( dfloc['time'] );
    #for c in list(range( 2, len(dfloc.columns) - 1*0 )):
    for c, cn in enumerate( cnames ):
      if cn not in ['k','time']:
        ### assumes col(0) = indices, col(1) = Timestamp
        #s = DictNames(dfloc.columns)[0][c] ;
        #c = DictNames(dfloc.columns)[1][cn] ;
        dfc = dfcorrection( dfloc, c, 
                           #CORRECTION=[True,True,False]
                           #CORRECTION=CORRECTORS,
                           APPLYSMOOTH=EXE['Smooth']
                           ) ; 
        dfcor[cn] = dfc;

    return dfcor;
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# %% INTERPOLATION AND RESAMPLING
def intArr( Arr, x):
    from   scipy.interpolate import interp1d
    from   scipy import interpolate
## interpolate Usoc onto digitalised Soc
    xd   = Arr[:,0];
    yd   = Arr[:,1];
    f    = interpolate.interp1d( xd,yd, kind='cubic', bounds_error=None)
#    yip  = f(Soc)
    return float( f(x) )

## %%
def intnpxy( npx, npy, xask, resampling=True ):
    from   scipy.interpolate import interp1d
    from   scipy import interpolate
    
    xd   = npx; #Arr[:,0];
    yd   = npy; # Arr[:,1];
    
    #if resampling:
    #    nx,ny = resample_xy( xd, yd );
        
    f    = interpolate.interp1d( xd,yd, kind='cubic', bounds_error=None)
    f    = interpolate.interp1d( xd,yd, kind='cubic', bounds_error=False, fill_value=yd.min() )

    yask = f(xask)
    #print( type( yask ))
    #print( yask )
    #if yask.shape[0]>0:
    #    yr = yask[0]
        
    return float( yask )

## %%
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def resample_xy( Sx, Sy, step=0.500 ):
    init_x = Sx[0];
    last_x = Sx[Sx.shape[0]-1] ;
    #delt_x = last_x - init_x   ;
#   NX = np.linspace( init_x, last_x, 10* delt_x);
    NX = np.arange( init_x, last_x, step );
    NY = np.zeros( NX.shape[0] );    
    for j, ex in enumerate( NX ) :
        #NY = np.append( NY, intnpxy( Sx, Sy, ex ) );    
        NY[j] = intnpxy( Sx, Sy, ex )
    return NX, NY

###############################################################################
# %% DERIVATIVES: finding roots of derivatives
###############################################################################

def find_derivatives( Sx, Sy, kgap=2, kinc=2, smoother=False ):
    '''
    find x-inflection (xinf) when 
      slope after xinf >> slope before xinf
    
    dy =find_derivatives( 
        dfcor['time'],dfcor[ fname ] , 
        kgap=2, kinc=1, smoother=True 
    );
    
    '''
    #PARAMETERS:
    #kgap = 5 ; 
    DERV=list();
    ##print( Sx.shape )
    ### compute the first derivative of S: dy = dyy / dx
    #print( type (Sx ))
    #print(      (Sx.shape ))
    init_x = Sx[0];
    last_x = Sx[Sx.shape[0]-1];
    delt_x = last_x - init_x  
#    NX = np.linspace( init_x, last_x, 10* delt_x);
    NX = np.arange( init_x, last_x, 0.50 );
    NY = np.zeros( NX.shape[0] );    
    for j, ex in enumerate( NX ) :
        #NY = np.append( NY, intnpxy( Sx, Sy, ex ) );    
        NY[j] = intnpxy( Sx, Sy, ex )
        
        
    for k in list(range( 0*kgap, NX.shape[0] - 0*kgap -0*1 +0*1, kinc )):
       if k>= NX.shape[0] - 1*kgap:
           dy = 0;# break
       if k<  1*kgap: 
           dy = 0; # 'nan';
       else:
         dy = \
           ( NY[ k + 0*kgap ] - NY[ k - 1*kgap ] )\
          /( NX[ k + 0*kgap ] - NX[ k - 1*kgap ] )  
        
       DERV.append([
            k, NX[k], NY[k], dy, #ddy
        ])
       ##print( k,  dy )
    DERV = pd.DataFrame( data=DERV,
                        columns=['k','x','y','dy']
    );
    DERV.iloc[0,3] = DERV.iloc[1,3] ;
    DERV['dy'] = fsmoothsignal( DERV['dy']) ;
    ### compute the second derivative of S  (ddy = dy/dx)
    sec = list();
    dy = DERV['dy'];
    ##print( DERV.shape )
    for k in list(range( 0+0*kgap, NX.shape[0] , kinc )): # - 1*kgap -0*1 +0*1, 1 )):
      #print(k)
      if k>= NX.shape[0] - 1*kgap: 
          dyS=0; #break
      if k<= 1*kgap: 
          ddy = 0; # 'nan';
      else:
        ddy = \
          ( dy[ k + 0*kgap ] - dy[ k - 1*kgap ] )\
         /( NX[ k + 0*kgap ] - NX[ k - 1*kgap ] )  
        #print(f"""{k}, {Xk}, {Yk}, {ddy} """)
       # print (( dy[ k + 1*kgap ] - dy[ k - 0*kgap ] ))
      ##print( k,  ddy )
      sec.append( [ k, NX[k], NY[k], ddy, ] )
        
    ##print( len(sec) )
    #DERV['ddy'] = sec 
    df_ddy = pd.DataFrame( sec, columns=['k','x','y','ddy'])
    for m in list(range(0,kgap+1)):
        df_ddy.iloc[m,3] = df_ddy.iloc[kgap+1,3] #= df_ddy.iloc[3,3]
    
    DERV['ddy'] = ( df_ddy['ddy'] ) ; 
    if smoother: DERV['ddy'] = fsmoothsignal ( df_ddy['ddy'] ) ; 

    return DERV 

def get_roots( dy, order=1, 
              xinit=3,
              guessjump=1.5, 
              nextjump=5,
     ):
    xroots = find_multiroot(dy, order=order, 
        xinit=3,
        guessjump=0.5, 
        nextjump=30,
        #xupper=800,
        maxtry=12,
    );
    yroots = [ 0 for k in range( len(xroots)) ];
    print( f"found these roots:  {xroots}  ") ;   
    return xroots, yroots
      
def analyze_derivative( dfcor, fname,
        AddInflections=True,
        ShowSecInflections=False,
        
    ):
    #fname = 'cpu-0-0'
    dy =find_derivatives( 
        dfcor['time'],dfcor[ fname ] , 
        kgap=2, kinc=1, smoother=True 
    );
    #print(type (dy ))
    ## plot ax1: y, ax2: dy/dt, ax3: dyy/dt2
    fig, ax1 = plt.subplots(
                1, 1,
                sharex=True,
                dpi=240.0,
                # figsize=[ 8, 8 ],
                tight_layout=True,
     #          figsize=( 1.25 * 4.150, 1.25 * 4.800 ),
                ## https://matplotlib.org/stable/api/figure_api.html
                ## figsize2-tuple of floats, default: rcParams["figure.figsize"] (default: [6.4, 4.8])
                ## Figure dimension (width, height) in inches.
                #margin_top=0.15,
    );
    line1, = ax1.plot(
        dy['x'],
        dy['y'],
        color='r',
        lw=1.0,
        label='y'
    );
    ax1.set_ylabel(f'y(t) = {fname}', color='r')
    ax1.tick_params(axis='y', labelcolor='r')
    
    
    ax2 = ax1.twinx()
    line2, = ax2.plot(
        dy['x'],
        dy['dy'],
        color='g',
        lw=0.7,
        label='first dy',
        alpha=0.25,
    );
    ax2.set_ylabel( 
        r"first dy ", 
        color='g',
        fontsize=7,
        )
    ax2.tick_params(
        axis='y', 
        labelcolor='g', 
        labelsize=6,
        pad=0.05,
        grid_color='g',
        grid_alpha=0.3,
        grid_linewidth=0.3,
    )
    ax2.axhline(
        # 0, 0, 
        # 1,
        # #dfcor.loc[-2,'time'],
        # #dy.loc[-2,'x'],
        color='g',
        linewidth=0.5,
        dashes=(5, 2, 1, 2) , 
    );
    if ShowSecInflections:
        ax3 = ax1.twinx()
        line3, = ax3.plot(
            dy['x'],
            dy['ddy'],
            color='b',
            lw=0.5,
            label='sec ddy'        
        );
        ax3.set_ylabel( 
            r"sec ddy ",
            color='b',
            fontsize=7,
            )
        ax3.tick_params(
            axis='y', 
            labelcolor='b', 
            labelsize=6,
            pad=0.05,
        )
        ax3.axhline(
            # 0, 0, 
            # 1,
            # #dfcor.loc[-2,'time'],
            # #dy.loc[-2,'x'],
            color='b',
            linewidth=0.5,
            dashes=(3, 2, 1, 2) , 
        )
    ax2.set_yticks( [0.00 ])
    ax2.spines['right'].set_position(('axes', 1.000));
    ax2.spines['right'].set_visible(True)
    if ShowSecInflections:
        ax3.set_yticks( [0.00 ])
        ax3.spines['right'].set_position(('axes', 1.065));
        ax3.spines['right'].set_visible(True)
    
    #fig.legend(handles=[line1, line2, line3], 
    #           #loc='best'
    #)
    #plt.tight_layout();
    #plt.show()

    if AddInflections:
        ### find roots for dy/dt
        xr1, yr1 = get_roots( dy, order=1,
                        xinit=3,
                        guessjump=15, 
                        nextjump=15,
                         );
        # ax2.scatter( xr1, yr1, 
        #              color='g', marker='x',
        #              alpha=0.18,
        # )
        ### find roots for dy/dt
    if ShowSecInflections:
        xr2, yr2 = get_roots( dy, order=2,
                         xinit=3,
                         guessjump=15, 
                         nextjump=15,
                         );
        # ax3.scatter( xr2, yr2, 
        #              color='b', marker='+',
        #              alpha=0.18,
        # )
        
    
    ## find the value of f(x) of the ordinal function at those roots xr(n)
    if 1:
        for xr in xr1:
            yr = intArr( dy[['x','y']].to_numpy(), xr ) 
            #print ( xr, yr )
            ax1.scatter( xr, yr, 
                         color='r', marker='x',
                     alpha=0.23,
            );
    if ShowSecInflections:
        for xr in xr2:
            yr = intArr( dy[['x','y']].to_numpy(), xr ) 
            #print ( xr, yr )
            ax1.scatter( xr, yr, 
                         color='r', marker='+',
                     alpha=0.23,
            );
        #if 1:    
    if ShowSecInflections:
        for xr in xr2:
            yr = intArr( dy[['x','dy']].to_numpy(), xr ) 
            #print ( xr, yr )
            ax2.scatter( xr, yr, 
                         color='g', marker='+',
            );
    
    #plt.show()
    #return None
    return fig, ax1

###############################################################################

# %% FUNCTION ROOTS 
def eval_locality( px, dy ):
    '''
    px = point of x
    dy  = [ x, y, dy, ddy ]
    '''
    m1 = intnpxy( dy['x'], dy['dy'], px - 3)
    m2 = intnpxy( dy['x'], dy['dy'], px + 3)
    py = intnpxy( dy['x'], dy['y'],  px + 0)
    lm = 'flc'; lc = 0;
    if m1 > 0 and m2 < 0:
        lm = 'lmx';
        lc  = 1 ;
    if m1 < 0 and m2 > 0:
        lm = 'lmi'
        lc  = 2 ;
    mc = \
         '^'*(lc==1) +\
         'v'*(lc==2) +\
         'o'*(lc==0)    
    return [px, py, lm, lc, mc ];

def get_locality( xroots, dy  ):
    pxx = 0 
    pyy = 0 
    LOCO = list();
    for k, ex in enumerate( xroots ):
        px, py, lo, lc, mc = eval_locality( ex , dy) 
        dex = px - pxx  
        dey = py - pyy
        LOCO.append([ px,py,lo,lc, mc, dex, dey ] )
        pxx = px
        pyy = py       
    return LOCO 

# %% finding roots of derivatives
import numpy as np
from scipy.optimize import fsolve
import scipy as sci

def find_root_from_data(x_data, y_data, initial_guess):
    """
    Findy the root of a function interpolated from data.

    Args:
        x_data (array-like): x-coordinates of the data points.
        y_data (array-like): y-coordinates of the data points.
        initial_guess (float): Initial guess for the root.

    Returns:
        float: The root of the interpolated function.
    cf https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.fsolve.html
    """

    def interpolated_function(x):
      return np.interp(x, x_data, y_data)
    root = fsolve(interpolated_function, initial_guess)
    return root    
def find_derivativesroot( dy, order=1, guessjump=10):
    def interpolated_function(x):
      return np.interp(x, x_data, y_data)
    #if __name__ == '__main__':
    xroot = 0; yroot =0 ;
    initial_guess = 50;
    if order==0: 
        f = 'y'
    if order==1: 
        f = 'dy'
    if order==2: 
        f = 'ddy'        
    x_data = (dy['x']).to_numpy(); 
    y_data = (dy[f]).to_numpy();
    while ( xroot <= 0 ):
        root = find_root_from_data(x_data, y_data, initial_guess)
    #   print(f"The root of the function is: {root}")
        xroot=root[0] ;
        initial_guess += guessjump ;
     
    return xroot , yroot


def find_multiroot( dy, xinit=0, order=1, xupper=None, 
                    guessjump=5, nextjump=5, maxtry=50,
                    DEB=False ):
    xroot = 0; yroot =0 ; ROOTS=list(); seek=0;
    initial_guess = xinit;
    if order==0: 
        f = 'y'
    if order==1: 
        f = 'dy'
    if order==2: 
        f = 'ddy'        
    x_data = (dy['x']).to_numpy(); 
    y_data = (dy[f]).to_numpy();
    if xupper==None: xupper = x_data[-1];
    xupper = x_data[-1] - nextjump ;
    if DEB: print( f' upper limit {xupper}');
    while ( xroot < xupper ):
      while ( xroot <= 0 ):
        #if DEB:  print( f' trying with guess {initial_guess} ')
        root = find_root_from_data(x_data, y_data, initial_guess)
        xroot=root[0] ;
        initial_guess += guessjump ;
      # if DEB: print(f"The root of the function is: {xroot}")

        if initial_guess > xupper:
            break
      if xroot not in ROOTS:
        if (xroot > 0 and xroot < xupper):
          ROOTS.append( float(xroot) )
      xroot=0;
      initial_guess += nextjump ;
      seek += 1;
      if seek > maxtry: 
          # print( " too many seeks, keeping with found root ")
          break
      if initial_guess > xupper or xroot > xupper:
          break
    #ff = sci.interpolate.interp1d( x_data, y_data)
    #yroot = np.interp( xroot, x_data, y_data)
    #yroot = ff(xroot)
    return ROOTS; 
###############################################################################


# %% YADJUSTMENT METHODS
yadjust_method_dict={
   0: 'no adjust',
   1: '(y - ymean)/ ( ymax - ymin)',
   2: '(y - ymin) / ( ymax )',
   3: '(y - yini) / ( ymax )',
   4: '(y - yini) / ( ymax - ymin)',
   6: '(y - yini) ',
  }

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def yadjust( y, METHOD=0, ):
    '''
    yadjust( y, OFFSET, METHOD=0 )
    adjusts the y-values in a Series(y) 
    Method
    1: (y -ymean)/ ( ymax - ymin)
    2: (y -ymin) / ( ymax )
    3: (y -yini) / ( ymax )
    4: (y -yini) / ( ymax - ymin)
    6: (y -yini)  

    OFFSET[0]: translates the y to yini
    OFFSET[1]: scales the y based on ymax
    '''
    if METHOD==0:
        return y;
    if METHOD==1:
        y = ( y - y.mean())/ (y.max() - y.min() );
    if METHOD==2:
        y = ( y - y.min() )/ (y.max() );
    if METHOD==3:
        y = ( y - y[0]    )/ (y.max() );
    if METHOD==4:
        y = ( y - y[0]    )/ (y.max() - y.min() );
    if METHOD==6:
        y = ( y - y[0]    ) ;
        
    return y ;
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def topmode( dfloc , asdf=True, names=None, ):
    '''
    topmode( dfloc,  asdf=True, names=dfloc.columns, )
    determines the most frequent min & max in each row for dfloc 
    '''
    modes = list()
    colname, namecol = DictNames( dfloc.columns );
    for r in range( dfloc.shape[0] ) :
        pass;
        row = dfloc.iloc[r,2:]
        whatmin = row.idxmin() ;
        wmi     = namecol[ whatmin ]  
        whatmax = row.idxmax() # axis = 1);
        wmx     = namecol[ whatmax ]  
        
        # print( whatmin ) 
        Z =  [r, wmi, wmx ]
        modes.append( Z )
        
    if asdf :
        modes = pd.DataFrame( data=modes, columns=['k','wmin','wmax'] ) ;
    return modes; 



# In[]  #######################################################################
## PLOTTING
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# In[]  ###
def cplot ( dfloc, c ):
    name = dfloc.columns [ c ]; 
    t = f'Sig-{c}:  {name}' ;
    if 1 : #SHOW:
        plt.plot( 
            dfloc.iloc[:,c],
            label=f'Sig-{c}: {name}',
            lw=0.35,
            color=COLOURS['reg'],            
        );
        plt.title( t ) ;
        plt.show() ;

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# In[]  ###
def mplot (dfloc, grouping, fig, ax1,
           METHOD=0,
           holdyhow=False , 
           FIGSAVE=True, FIGSHOW=False,
    ):
    '''
    mplot (  dfloc, grouping, 
               holdyhow=False , METHOD=0,
               FIGSAVE=True, FIGSHOW=False,
    
    Parameters
    ----------
    dfloc : dataframe
        DESCRIPTION.
    grouping : list of integers
        what signals to process in plot
    holdyhow : bool, optional
        DESCRIPTION. The default is False.
    METHOD : int, optional
        DESCRIPTION. The default is 0.
    FIGSAVE : bool, optional
        DESCRIPTION. The default is True.
    FIGSHOW : bool, optional
        DESCRIPTION. The default is False.

    Returns
    -------
    None.

    '''

    for c, name in enumerate( dfloc.columns[ grouping ]):
        #name = dfloc.columns[ c ]
        print( c, name )
        ax1.plot( 
            #dfloc.iloc[:,c],
            dfloc.loc[:,'time'],
            yadjust( dfloc.loc[:,name], METHOD=METHOD) ,
            label=f'{name}',
            #label=f'Sig-{c}: {name}',
            lw=0.35,
            color=COLOURS['reg'],            
        );
        t = f'Sig-{c}: {name}' ;
        #t = f'Group {grp}' ;      
    
    return fig, ax1
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# In[]  ###
def plotmodes( dfcor ):
    ''' plotmodes( dfcor )
#  Plot the topmodes for Min and Max for each Set '''
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
    modes = topmode( dfcor, names=dfcor.columns, asdf=True ) ;
    ## print( modes ) ;    
    modes.plot( kind='scatter', x='k', y='wmin' ),
    modes.plot( kind='scatter', x='k', y='wmax' ),
    plt.show() ;
    
    return modes;

# In[]  #######################################################################
def plotexts( dfcor, grouping,
              fig, ax1,
              METHOD=1, 
              showmodes=False , 
              FIGSAVE=True, FIGSHOW=False,
              inpfile=None,
              inppath=None,
):
    '''

    Parameters
    ----------
    dfcor : pd.DataFrame
        DESCRIPTION.
    grouping : list of integers
       what signals to process in plot
    grp : int
        DESCRIPTION. The default is 1.
    METHOD : int, optional
       DESCRIPTION. The default is 0.

    showmodes : bool, optional
        DESCRIPTION. The default is True.
    holdyhow : bool, optional
       DESCRIPTION. The default is False.
    FIGSAVE : bool, optional
       DESCRIPTION. The default is True.
    FIGSHOW : bool, optional
       DESCRIPTION. The default is False.
       
    Returns
    -------
    None.

    '''
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #
    dfloc = dfcor.iloc[:,grouping]
    modes = topmode( dfloc ) ;
 

    if 0:    
        modes.plot( kind='scatter', x='k', y='wmin',
                   label='Min Signal', 
                   color=COLOURS['min'],
                   ),
        modes.plot( kind='scatter', x='k', y='wmax',
                   label='Max Signal' ,
                   color=COLOURS['max'],
                   ),
    if showmodes:        
        ax1.scatter( modes['k'], modes['wmin'],
                   label='Min Signal', 
                   color=COLOURS['min'],
                   s=5,
                   ),
        ax1.scatter( modes['k'], modes['wmax'],
                   label='Max Signal' ,
                   color=COLOURS['max'],
                   s=5,
                   )

    ax1.plot( dfcor.loc[:,'time'],
              yadjust( dfloc.max(  axis=1 ),  METHOD=METHOD )  ,
              label='max' ,
              color=[ 205/255,  10/255,   5/255 ],
              lw=1.5,
    );
    ax1.plot( dfcor.loc[:,'time'],
              yadjust( dfloc.mean( axis=1 ) , METHOD=METHOD ) , 
              label='mean' ,
              color=[ 25/255,  200/255,   5/255 ],
              lw=1.5, 
    );
    ax1.plot( dfcor.loc[:,'time'],
              yadjust( dfloc.min(  axis=1 ) , METHOD=METHOD ) , 
              label='min'  ,
              color=[  25/255,  50/255, 210/255 ],
              lw=1.5,
    );
    return fig, ax1 ;
###############################################################################


#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
###############################################################################
# %% MAIN EXECUTE
# #==============================================================================
# if __name__ == '__main__': 

#   if 0:
#     pass ;
#     EXE = getArgs( EXE );
#     if EXE['doc']: 
#           print( __doc__, end='\n\n');
#           # print( __version__, end='\n\n');
#           # print( __usage__, end='\n\n')
#           exit();
#     # #if PSH[1]: showkeys( EXE );
#     #  PSH = set_verbosity( EXE['psh'] , SHOW=False);
#       #PSH = set_verbosity( EXE['psh'] , SHOW=True);   

#   if 0: #<< input path  >>========================================   
#     pass ;
#     if inppath==None : inppath = os.getcwd();
#     if (EXE['inp'] ) == None: pass;
#     else: 
#      if len( EXE['inp'] ) >0:
#       inppath =EXE['inp'];
#       if type( EXE['inp'])==list: inppath=EXE['inp'][0] 
#   #    inppath = EXE['inp'];  
#       if PSH[1]: print ( os.listdir() )
#       #if PSH[0]:
#       print(' current path is {} '.format(inppath));
#       print(' Inppath: {} '.format(inppath));
      
# #==============================================================================

#   if 1: 
#     inppath = r'/Users/dac/qlab/testing/Q0B006';
#     inppath = MANUAL_PATH
# #   inpfile = getFiles(inppath);

#     dfread, inpfile = get_dfread( inppath, SHOW=False );
#     inpbase = inpfile.rstrip( ".csv")

#     dfmain = dfread.copy();

# # In[]:
#   if 1:  ## *** generate dfcor 
#     # *************************************************************************
#     # Main feature of correcting the registers 
#     #   out = smoothf( inp * 0.01 ) - 273.15 
#     #   note that smoothf is a noise-filtering smooth function 
#     #   cancel the function by changing 
#     #   CORRECTION=[True,True,True] --> CORRECTION=[True,True,False]
#     dfcor   = build_dfcor( 
#                 #dfmain.iloc[:,thisgroup], 
#                 dfmain,
#                 ## <deprecated> CORRECTION=CORRECTORS, 
#                 ## <deprecated> CORRECTION=[True,True,True], 
#                 ## <deprecated> CORRECTION=[True,True,False], ## will cancel the noise-filter
#                 APPLYSMOOTH=EXE['Smooth'],
#                 ## <deprecated> SHOW=False 
#             );    
#     # print( dfcor.head() )
#     # *************************************************************************
    
# #==============================================================================
# ##if __name__ == '__main__': 
#   if ProcesGroups: ## defining the GROUPINGS and SELGROUPS 
#     GROUPINGS = {
#         0 : list(range( 2, 24, 1)) ,
#         1 : list(range( 2, 12, 1)) ,
#         2 : list(range(18, 24, 1)) ,
#         3 : [ 12, 13, 14, 15 ] ,
#         4 : [ 2, 19, 20 ] ,
#         5 : [ 3,4,5,6 ] ,
    
#     }
#     SELGROUPS = [ 1 , 2, 3 ]
#     SELGROUPS = [ 1, 2, 3 ]
#     SELGROUPS = [ 4,5,1,3,2,0 ]
    
#     SELGROUPS = EXE['SELGROUPS']

#   #==============================================================================  
#     for thisgroupsel in SELGROUPS :
#         print( f"- processing Group Set # {thisgroupsel} ")
#         thisgroup = GROUPINGS.get(  thisgroupsel  );
#         print( f"   this groupset includes these signals : ")
        
#         for c in dfmain.columns[thisgroup]:
#             print( f"\t  {c}  " )
     
#         # ***************************************************************************
#         ## In[]: Plotting the Groups 
#         plt.clf();  
#         if ProcessGroupPlot: ## graph with no scaling 
            
#           if PlotNoScaling: ## plot first graph with NO SCALING
#                 selmethod = 0 ;
#                 # if PlotScaling: 
#                     ## plot second graph with scaling method scalingmethod=EXE['method']
#                 plt.clf(); 
#                 fig, ax1  = plt.subplots(
#                             1, 1,
#                             sharex=True,
#                             dpi=240.0,
#                             # figsize=[ 8, 8 ],
#                             tight_layout=True,
#                  #          figsize=( 1.25 * 4.150, 1.25 * 4.800 ),
#                             ## https://matplotlib.org/stable/api/figure_api.html
#                             ## figsize2-tuple of floats, default: rcParams["figure.figsize"] (default: [6.4, 4.8])
#                             ## Figure dimension (width, height) in inches.
#                             #margin_top=0.15,
#                 );
#                 scalingmethod = 0

#                 fig, ax1 = mplot(    dfcor, thisgroup, fig, ax1, METHOD=selmethod,  );
#                 fig, ax1 = plotexts( dfcor, thisgroup, fig, ax1, METHOD=selmethod,  );
#                 #plotexts( dfcor, showmodes=False ,           holdyhow=True, METHOD=0,  );
#                 t = f'Group {thisgroupsel}' ;
#                 #plt.suptitle( f'Group {thisgroupsel}', fontsize=14 )
#                 plt.title( ' No scaling method  (0) ', fontsize=8, fontstyle='italic', ) ;
#                 plt.legend( fontsize=6.5, ncols=3 );
#                 plt.xlabel(' Time (sec) ') ;
#                 plt.ylabel(' Temperature (*C)');
#                 if EXE['figsave']: #if FIGSAVE:
                    
#                     figname = inppath + os.sep + \
#                         f"Gr{thisgroupsel}_Sm{scalingmethod}" +\
#                         ".png";
#                     print( f"saving figure ... {figname}")
#                     plt.savefig( 
#                        figname
#                     );
#                 if EXE['figshow']: #if FIGSHOW:
#                     plt.show() ;
    
   
# ###############################################################################
# # %% In[]:  
# if 1:    
#   SET2PROCESS = [
#                  'cpu-0-0',
#                  'skin-sensor'
#                  ]  
#   if ProcessDerivatives: ##
#     for fname in SET2PROCESS:
        
#         fig, ax1 = analyze_derivative( dfcor, fname , 
#                    AddInflections=OPTS['AddInflections'],
#                    ShowSecInflections=False,
#                    );
          
#         ex = 45;
#         ey = intnpxy( dfcor['time'], dfcor[ fname] , ex )
#         ax1.scatter( ex, ey, s=30, marker='*' , color='b' )
#         plt.show()
    
#     #plt.scatter( dfmain['time'],dfmain[fname ] )
#     #plt.show()
#     #plt.scatter( dfcor ['time'],dfcor [fname ] )
#     #plt.show()



# # %%
# #for k,v in SIGNAL_LIST:
# for k in range( 3, 23 ):
# #if 1:
#     fname = SIGNAL_LIST.get( k )
#     plt.clf();    
#     #fname = 'skin-sensor'
#     dy =find_derivatives( 
#         dfcor['time'],dfcor[ fname ] , 
#         kgap=2, kinc=1, smoother=True 
#     );
#     xr1, yr1 = get_roots( dy, order=1,
#                     xinit=3,
#                     guessjump=3, 
#                     nextjump=20,
#                      );
#     xroots = find_multiroot(dy, order=1, 
#                 xinit=3,
#                 guessjump=0.5, 
#                 nextjump=20,
#                 #xupper=800,
#                 maxtry=15,
#     );
#     xroots.sort(); #xroots = sorted(xroots)
#     pxx = 0 
#     pyy = 0 
#     LOCO = list();
#     for k, ex in enumerate( xroots ):
#         px, py, lo, lc, mc = eval_locality( ex , dy) 
#         dex = px - pxx  
#         dey = py - pyy
#         LOCO.append([ px,py,lo,lc, mc, dex, dey ] )
#         pxx = px
#         pyy = py
#         plt.scatter( px, py, s=30, marker=mc )
        
#     plt.plot( dfcor['time'], dfcor[fname]) ;
#     plt.title( f' {fname} ', fontsize=14, )
    
#     plt.show() ;
#     dLOCO = pd.DataFrame( 
#         data=LOCO, columns=['x','y','lm','lc','mc','dx','dy']
#     );
    

###############################################################################
# In[]  NOTES #################################################################
if 0:

 '''
    SKIP_LIST = [  19, 25 ];
thermal_zone0: type=aoss-0 temp=28200
thermal_zone1: type=cpu-0-0 temp=29400
thermal_zone2: type=cpu-0-1 temp=29000
thermal_zone3: type=cpu-0-2 temp=30200
thermal_zone4: type=cpu-0-3 temp=29800
thermal_zone5: type=gpuss-0 temp=29000
thermal_zone6: type=gpuss-1 temp=28200
thermal_zone7: type=nspss-0 temp=27800
thermal_zone8: type=nspss-1 temp=27800
thermal_zone9: type=nspss-2 temp=27800
thermal_zone10: type=video temp=28600
thermal_zone11: type=ddr temp=29400
thermal_zone12: type=camera-0 temp=28200
thermal_zone13: type=camera-1 temp=27800
thermal_zone14: type=mdmss-0 temp=28600
thermal_zone15: type=pm8150_tz temp=28147
thermal_zone16: type=therm-soc-usr temp=27522
thermal_zone17: type=thermal-power temp=1
thermal_zone18: type=skin-sensor temp=28755
thermal_zone19: type=skin-sensor-o temp=28723
thermal_zone20: type=therm-quiet-usr temp=27339
thermal_zone21: type=therm-rf-usr temp=27614
thermal_zone22: type=therm-in-temp-usr temp=27064
thermal_zone23: type=hw-comparator temp=1
SKIP_LIST = [  19, 25 ];
'''
 figanno='''
fig.text( 0.0500, 0.9500,
                     str( '{:<} {}'.format(
                       str( 'Test:{:<}'.format(
                         tcpro.pcase(ICASE)
                       )),
                       str( 'Seg:{:<}'.format(tcpro.pcase(_IRUN+1))),
                     )),
                     ha='left',
                     fontsize=9,
                     fontweight='bold',
                     font='Verdana',
                     #color=[ 220*(1/255),  15*(1/255),   5*(1/255) ],
                     color=FARBEN[3],
            );
'''

###############################################################################

